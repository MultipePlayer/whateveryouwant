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
# [수정] 단순 키 집합 대신, 데이터 객체 자체를 매핑하여 업데이트 가능하게 변경
existing_map = {} 

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
    특정 언어(lang_code)의 미디어 정보를 가져와 비디오 URL, 자막, [추가] 제목을 반환합니다.
    """
    target_url = f"{BASE_API_MEDIA}/{lang_code}/{natural_key}?clientType=www"
    try:
        res = http.get(target_url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            media = data.get('media', [{}])[0]
            # [추가] 해당 언어의 제목 추출
            title = media.get('title', '')
            video_url, sub_url = get_video_url_and_sub(media)
            script = parse_vtt(sub_url) if sub_url else []
            return video_url, script, title
    except: pass
    return None, [], ""

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
                
                # [개선된 로직]
                # 1. 이미 존재하는 항목인지 확인
                existing_item = existing_map.get(natural_key)
                
                needs_update = False
                
                if not existing_item:
                    # 아예 없는 항목이면 수집 대상
                    needs_update = True
                else:
                    # 이미 있지만, 다른 언어(영어/중국어) 데이터가 비어있다면 업데이트 대상
                    current_urls = existing_item.get('video_urls', {})
                    # 우리가 원하는 언어들이 모두 video_urls에 있는지 확인 (ko는 있다고 가정)
                    # 하나라도 없으면 재수집 시도
                    if 'en' not in current_urls or 'cn' not in current_urls:
                         needs_update = True
                    # 또는 titles가 없다면 업데이트 (검색 기능 지원 위해)
                    if 'titles' not in existing_item:
                         needs_update = True

                if not needs_update:
                    continue

                # --- 수집 시작 ---
                
                # 한국어 기본 데이터 (없으면 기존 것 사용 시도, 없으면 수집 불가)
                video_url_ko, sub_url_ko = get_video_url_and_sub(media)
                if not video_url_ko and not existing_item: continue

                print(f"   + Processing: {media['title'][:30]}... (Update: {bool(existing_item)})")
                
                # 데이터 컨테이너 초기화 (기존 데이터가 있으면 유지)
                scripts = existing_item['scripts'] if existing_item else {}
                video_urls = existing_item['video_urls'] if existing_item else {}
                titles = existing_item.get('titles', {}) if existing_item else {}

                # 1. 한국어 데이터 업데이트
                if sub_url_ko: 
                    # 이미 있으면 굳이 다시 파싱 안해도 되지만, 정확성을 위해 갱신 가능
                    # 여기서는 없거나 비어있을 때만 채움
                    if 'ko' not in scripts or not scripts['ko']:
                        scripts['ko'] = parse_vtt(sub_url_ko)
                
                if video_url_ko:
                    video_urls['ko'] = video_url_ko
                
                titles['ko'] = media['title']

                # 2. 다른 언어(영어, 중국어) 데이터 처리
                for key, code in LANG_MAP.items():
                    if key == 'ko': continue
                    
                    # 이미 데이터가 빵빵하면 건너뛰기 (API 요청 절약)
                    if key in video_urls and key in scripts and key in titles:
                        continue

                    v_url, script, var_title = fetch_variant_data(code, natural_key)
                    
                    if v_url: video_urls[key] = v_url
                    if script: scripts[key] = script
                    if var_title: titles[key] = var_title

                # 저장 로직
                if existing_item:
                    # 기존 객체 업데이트 (Reference Update)
                    existing_item['video_urls'] = video_urls
                    existing_item['scripts'] = scripts
                    existing_item['titles'] = titles
                    # 날짜나 제목 등도 최신화
                    existing_item['date'] = media.get('firstPublished', existing_item.get('date'))
                else:
                    # 신규 추가
                    new_item = {
                        'category': current_title,
                        'title': media['title'],
                        'natural_key': natural_key,
                        'url': video_url_ko,
                        'video_urls': video_urls, 
                        'titles': titles, # [추가] 다국어 제목 저장
                        'date': media.get('firstPublished', '0000-00-00'),
                        'scripts': scripts
                    }
                    collected_list.append(new_item)
                    existing_map[natural_key] = new_item
                
                time.sleep(0.1) # 매너 딜레이
            
        for sub in cat_info.get('subcategories', []):
            if sub.get('key'): crawl_category(sub.get('key'), collected_list)
    except Exception as e: print(f"Error ({category_key}): {e}")

def load_existing_data():
    total_data = []
    # 마스터 파일 확인
    if os.path.exists(LOCAL_SAVE_FILE):
        try:
            with open(LOCAL_SAVE_FILE, 'r', encoding='utf-8') as f:
                total_data = json.load(f)
            print(f"Loaded {len(total_data)} items from master file.")
        except: pass
    
    # 분할 파일 확인
    if not total_data and glob.glob("jw_multilingual_data_*.json"):
        split_files = sorted(glob.glob("jw_multilingual_data_*.json"), key=lambda x: int(re.findall(r'\d+', x)[0]))
        for file in split_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    chunk = json.load(f)
                    total_data.extend(chunk)
            except: pass
        print(f"Loaded {len(total_data)} items from split files.")

    # [수정] Map 구성 (natural_key -> Item Object)
    for item in total_data:
        if 'natural_key' in item:
            existing_map[item['natural_key']] = item
            
    return total_data

def save_data(data):
    # 날짜순 정렬
    data.sort(key=lambda x: x.get('date', '0000-00-00'), reverse=True)
    
    # 통합 파일 저장
    with open(LOCAL_SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 기존 분할 파일 삭제
    for f in glob.glob("jw_multilingual_data_*.json"): 
        try: os.remove(f)
        except: pass
    
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
    print("--- Start JW Crawler (Smart Update Mode) ---")
    
    # 1. 기존 데이터 로드
    collected_list = load_existing_data()
    # initial_count = len(collected_list) # 이제 업데이트도 하므로 단순 count 비교는 의미가 적음
    
    # 2. 크롤링 (업데이트 필요한 항목은 다시 긁음)
    for category in TARGET_CATEGORIES:
        crawl_category(category, collected_list)
    
    # 3. 무조건 저장 (내용이 업데이트 되었을 수 있으므로)
    save_data(collected_list)

if __name__ == "__main__":
    run()
