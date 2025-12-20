import requests
import json
import re
import time
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# --- 설정 구역 ---
MAIN_LANGUAGE = 'KO' 
ADDITIONAL_LANGS = {'en': 'E', 'cn': 'CHS'} 
CHUNK_SIZE = 500  
BASE_API_CATEGORY = "https://b.jw-cdn.org/apis/mediator/v1/categories/"
BASE_API_MEDIA = "https://b.jw-cdn.org/apis/mediator/v1/media-items/"

# 수집 대상 카테고리
TARGET_CATEGORIES = [
    'VODPgmEvtMorningWorship', 'VODStudio', 'VODChildren', 'VODTeenagers', 
    'VODFamily', 'VODPgmEvt', 'VODOurActivities', 'VODMinistryTools', 
    'VODOrganization', 'VODBible', 'VODMovies', 'VODSeries', 
    'VODIntExp', 'VODNews', 'VideoOnDemand'
]

EXCLUDE_KEYWORDS = ['Music', '음악', 'Audio Description', '화면 해설', 'AudioDescriptions']
LOCAL_SAVE_FILE = "jw_multilingual_data.json"

visited_keys = set()
existing_urls = set()

# --- 네트워크 설정 ---
# GitHub Actions 등 봇 환경 차단을 막기 위한 헤더 설정
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

http = requests.Session()
retry = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
http.mount("https://", HTTPAdapter(max_retries=retry))
http.headers.update(HEADERS)

def time_to_seconds(time_str):
    try:
        parts = time_str.split(':')
        if len(parts) == 3:
            h, m, s = parts
            s, ms = s.split('.')
            return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
        elif len(parts) == 2:
            m, s = parts
            s, ms = s.split('.')
            return int(m) * 60 + int(s) + int(ms) / 1000
        return 0
    except:
        return 0

def parse_vtt(vtt_url):
    if not vtt_url: return []
    try:
        res = http.get(vtt_url, timeout=10)
        res.encoding = 'utf-8-sig'
        if res.status_code != 200: return []
        
        lines = res.text.splitlines()
        script_data = []
        current_start = 0
        current_text = []
        time_pattern = re.compile(r'((?:\d{2}:)?\d{2}:\d{2}\.\d{3})\s*-->')
        
        for line in lines:
            line = line.strip()
            time_match = time_pattern.search(line)
            if time_match:
                if current_text:
                    full_text = " ".join(current_text).strip()
                    if full_text:
                        script_data.append({"start": current_start, "text": full_text})
                current_start = time_to_seconds(time_match.group(1))
                current_text = []
                continue
            if not line or line.isdigit() or line.startswith('WEBVTT') or line.startswith('NOTE') or '-->' in line:
                continue
            clean_line = re.sub(r'<[^>]+>', '', line)
            current_text.append(clean_line)
            
        if current_text:
            script_data.append({"start": current_start, "text": " ".join(current_text).strip()})
        return script_data
    except:
        return []

def get_video_url_and_sub(media_item):
    video_url = ""
    sub_url = ""
    if 'files' in media_item:
        for file in media_item['files']:
            if file.get('label') == '720p': 
                video_url = file.get('progressiveDownloadURL')
            if 'subtitles' in file and not sub_url:
                sub_url = file['subtitles']['url']
        if not video_url and media_item['files']:
            video_url = media_item['files'][0].get('progressiveDownloadURL')
    return video_url, sub_url

def fetch_variant_script(lang_code, natural_key):
    target_url = f"{BASE_API_MEDIA}{lang_code}/{natural_key}?clientType=www"
    try:
        res = http.get(target_url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            media = data.get('media', [{}])[0]
            _, sub_url = get_video_url_and_sub(media)
            if sub_url:
                return parse_vtt(sub_url)
    except Exception:
        pass
    return []

def crawl_category(category_key, collected_list, path_name=""):
    if category_key in visited_keys: return
    visited_keys.add(category_key)
    if any(ex in category_key for ex in EXCLUDE_KEYWORDS): return

    target_url = f"{BASE_API_CATEGORY}{MAIN_LANGUAGE}/{category_key}?detailed=1"
    try:
        res = http.get(target_url, timeout=20)
        if res.status_code != 200: return
        data = res.json()
        cat_info = data.get('category', {})
        current_title = cat_info.get('title', category_key)
        
        if any(ex in current_title for ex in EXCLUDE_KEYWORDS): return
        
        full_path = f"{path_name} > {current_title}" if path_name else current_title
        
        if 'media' in cat_info:
            for media in cat_info['media']:
                natural_key = media.get('languageAgnosticNaturalKey')
                if not natural_key: continue

                video_url, sub_url_ko = get_video_url_and_sub(media)
                
                if not video_url or video_url in existing_urls: 
                    continue

                print(f"   + New: {media['title'][:30]}...")

                script_ko = parse_vtt(sub_url_ko)
                script_en = fetch_variant_script(ADDITIONAL_LANGS['en'], natural_key)
                script_cn = fetch_variant_script(ADDITIONAL_LANGS['cn'], natural_key)

                if script_ko or script_en or script_cn:
                    collected_list.append({
                        'category': current_title,
                        'title': media['title'],
                        'natural_key': natural_key,
                        'url': video_url,
                        'date': media.get('firstPublished', '0000-00-00'),
                        'scripts': {
                            'ko': script_ko,
                            'en': script_en,
                            'cn': script_cn
                        }
                    })
                    existing_urls.add(video_url)
                    time.sleep(0.1) 
            
        if 'subcategories' in cat_info:
            for sub in cat_info['subcategories']:
                if sub.get('key'): crawl_category(sub.get('key'), collected_list, full_path)
        
        time.sleep(0.05)
    except Exception as e:
        print(f"Error ({category_key}): {e}")

def load_existing_data():
    total_data = []
    if os.path.exists(LOCAL_SAVE_FILE):
        try:
            with open(LOCAL_SAVE_FILE, 'r', encoding='utf-8') as f:
                total_data = json.load(f)
            print(f"Loaded existing data: {len(total_data)} items")
            for item in total_data:
                if 'url' in item: existing_urls.add(item['url'])
        except: pass
    return total_data

def save_data(data):
    # 날짜 기준 정렬
    data.sort(key=lambda x: x.get('date', '0000-00-00'), reverse=True)
    
    print(f"\nSaving master file ({LOCAL_SAVE_FILE})...")
    with open(LOCAL_SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    file_list = []
    total_chunks = (len(data) // CHUNK_SIZE) + 1
    print(f"Creating {total_chunks} chunk files...")

    for i in range(total_chunks):
        chunk = data[i * CHUNK_SIZE : (i + 1) * CHUNK_SIZE]
        if not chunk: continue
        filename = f"jw_multilingual_data_{i+1}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, ensure_ascii=False, indent=None) # 용량 절약 위해 indent 제거
        file_list.append(filename)
    
    with open('jw_data_index.json', 'w', encoding='utf-8') as f:
        json.dump(file_list, f, ensure_ascii=False)
    print("All saved.")

def run():
    print("Start crawler...")
    collected_list = load_existing_data()
    initial_count = len(collected_list)
    
    for category in TARGET_CATEGORIES:
        crawl_category(category, collected_list)

    added_count = len(collected_list) - initial_count
    print(f"\nDone! Added: {added_count}")
    
    if len(collected_list) > 0:
        save_data(collected_list)

if __name__ == "__main__":
    run()