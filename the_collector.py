import requests
import json
import re
import time
import os
import glob
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- 설정 구역 ---
MAIN_LANGUAGE = 'KO' 
# 추가 언어 설정 (JW 언어 코드)
# E: 영어, CHS: 중국어(간체)
LANG_MAP = {'ko': 'KO', 'en': 'E', 'cn': 'CHS'} 

CHUNK_SIZE = 500  
BASE_API_CATEGORY = "https://b.jw-cdn.org/apis/mediator/v1/categories"
BASE_API_MEDIA = "https://b.jw-cdn.org/apis/mediator/v1/media-items"

TARGET_CATEGORIES = [
    'VODNewestEvents', 'VODPgmEvtMorningWorship', 'VODStudio', 'VODChildren', 
    'VODTeenagers', 'VODFamily', 'VODPgmEvt', 'VODOurActivities', 
    'VODMinistryTools', 'VODOrganization', 'VODBible', 'VODMovies', 
    'VODSeries', 'VODIntExp', 'VODNews', 'VideoOnDemand'
]

EXCLUDE_KEYWORDS = ['Music', '음악', 'Audio Description', '화면 해설', 'AudioDescriptions']
LOCAL_SAVE_FILE = "jw_multilingual_data.json"

visited_keys = set()
existing_urls = set()

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
    except: return 0

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
                    if full_text: script_data.append({"start": current_start, "text": full_text})
                current_start = time_to_seconds(time_match.group(1))
                current_text = []
                continue
            if not line or line.isdigit() or line.startswith('WEBVTT') or line.startswith('NOTE') or '-->' in line: continue
            clean_line = re.sub(r'<[^>]+>', '', line)
            current_text.append(clean_line)
        if current_text: script_data.append({"start": current_start, "text": " ".join(current_text).strip()})
        return script_data
    except: return []

def get_video_url_and_sub(media_item):
    video_url = ""
    sub_url = ""
    if 'files' in media_item:
        for file in media_item['files']:
            # 720p 우선, 없으면 다른 것
            if file.get('label') == '720p': video_url = file.get('progressiveDownloadURL')
            if 'subtitles' in file and not sub_url: sub_url = file['subtitles']['url']
        if not video_url and media_item['files']: 
            video_url = media_item['files'][0].get('progressiveDownloadURL')
    return video_url, sub_url

def fetch_variant_data(lang_code, natural_key):
    """
    특정 언어(lang_code)의 미디어 정보를 가져와 비디오 URL과 자막 데이터를 반환합니다.
    """
    target_url = f"{BASE_API_MEDIA}/{lang_code}/{natural_key}?clientType=www"
    try:
        res = http.get(target_url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            media = data.get('media', [{}])[0]
            video_url, sub_url = get_video_url_and_sub(media)
            script = parse_vtt(sub_url) if sub_url else []
            return video_url, script
    except: pass
    return None, []

def crawl_category(category_key, collected_list):
    if category_key in visited_keys: return
    visited_keys.add(category_key)
    if any(ex in category_key for ex in EXCLUDE_KEYWORDS): return

    target_url = f"{BASE_API_CATEGORY}/{MAIN_LANGUAGE}/{category_key}?detailed=1"
    try:
        res = http.get(target_url, timeout=20)
        if res.status_code != 200: return
        data = res.json()
        cat_info = data.get('category', {})
        current_title = cat_info.get('title', category_key)
        
        if 'media' in cat_info:
            for media in cat_info['media']:
                natural_key = media.get('languageAgnosticNaturalKey')
                if not natural_key: continue
                
                # 한국어 기본 데이터
                video_url_ko, sub_url_ko = get_video_url_and_sub(media)
                if not video_url_ko or video_url_ko in existing_urls: continue

                print(f"   + Processing: {media['title'][:30]}...")
                
                # 스크립트 및 비디오 URL 수집 컨테이너
                scripts = {}
                video_urls = {}

                # 1. 한국어 데이터 처리
                scripts['ko'] = parse_vtt(sub_url_ko)
                video_urls['ko'] = video_url_ko

                # 2. 다른 언어(영어, 중국어) 데이터 처리
                # LANG_MAP에서 'ko'는 이미 처리했으므로 제외하고 순회
                for key, code in LANG_MAP.items():
                    if key == 'ko': continue
                    v_url, script = fetch_variant_data(code, natural_key)
                    if v_url: video_urls[key] = v_url
                    if script: scripts[key] = script

                # 유효한 데이터가 하나라도 있으면 추가
                if any(scripts.values()):
                    collected_list.append({
                        'category': current_title,
                        'title': media['title'],
                        'natural_key': natural_key,
                        'url': video_url_ko, # 기본 URL (하위 호환성)
                        'video_urls': video_urls, # [NEW] 언어별 비디오 URL
                        'date': media.get('firstPublished', '0000-00-00'),
                        'scripts': scripts
                    })
                    existing_urls.add(video_url_ko)
                    time.sleep(0.1)
            
        for sub in cat_info.get('subcategories', []):
            if sub.get('key'): crawl_category(sub.get('key'), collected_list)
    except Exception as e: print(f"Error ({category_key}): {e}")

def load_existing_data():
    total_data = []
    if os.path.exists(LOCAL_SAVE_FILE):
        try:
            with open(LOCAL_SAVE_FILE, 'r', encoding='utf-8') as f:
                total_data = json.load(f)
            print(f"Loaded {len(total_data)} items.")
        except: pass
    elif glob.glob("jw_multilingual_data_*.json"):
        split_files = sorted(glob.glob("jw_multilingual_data_*.json"), key=lambda x: int(re.findall(r'\d+', x)[0]))
        for file in split_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    total_data.extend(json.load(f))
            except: pass
    for item in total_data:
        if 'url' in item: existing_urls.add(item['url'])
    return total_data

def save_data(data):
    # 날짜순 정렬
    data.sort(key=lambda x: x.get('date', '0000-00-00'), reverse=True)
    
    # 통합 파일 저장 (백업용)
    with open(LOCAL_SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 기존 분할 파일 삭제
    for f in glob.glob("jw_multilingual_data_*.json"): os.remove(f)
    
    # 분할 저장
    file_list = []
    total_chunks = (len(data) // CHUNK_SIZE) + 1
    for i in range(total_chunks):
        chunk = data[i * CHUNK_SIZE : (i + 1) * CHUNK_SIZE]
        if not chunk: continue
        filename = f"jw_multilingual_data_{i+1}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, ensure_ascii=False, separators=(',', ':'))
        file_list.append(filename)
    
    # 인덱스 파일 생성
    with open('jw_data_index.json', 'w', encoding='utf-8') as f:
        json.dump(file_list, f, ensure_ascii=False)
    
    print(f"Saved {len(data)} total items.")

def run():
    print("--- Start JW Crawler (Multi-Language Video) ---")
    collected_list = load_existing_data()
    initial_count = len(collected_list)
    
    for category in TARGET_CATEGORIES:
        crawl_category(category, collected_list)
    
    added_count = len(collected_list) - initial_count
    if added_count > 0 or not os.path.exists(LOCAL_SAVE_FILE):
        save_data(collected_list)
    else:
        print("No new data.")

if __name__ == "__main__":
    run()

