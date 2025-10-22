import os
import re
import json
import requests
import datetime
import traceback
from zoneinfo import ZoneInfo

import stanza
import dateparser
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# 사용자 정의 모듈 (예: 장소 추출)
from parser import extract_locations, location_keywords_extended

# --------------------
# NLP 및 환경설정
# --------------------
# stanza.download("ko", verbose=False)  # 스탠자 한글 모델 다운로드(최초 1회만 필요)
# nlp = stanza.Pipeline(lang="ko", processors="tokenize,pos,lemma")

# 환경변수(.env) 로드 (Google OAuth)
load_dotenv()
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
CLIENT_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://13.210.90.100.nip.io/auth/callback")

# 사용자 토큰 저장소(실제 서비스시 DB 활용)
user_tokens = {}

# 전역 변수로 선언
_nlp_pipeline = None

# 정적파일 경로 마운트
app = FastAPI()

# 서버 시작 이벤트에 모델 로딩 로직 추가
@app.on_event("startup")
def load_nlp_pipeline():
    # 이 부분을 임시로 주석 처리하거나, stanza 관련 코드를 제거하고 서버 시작을 시도해 보세요.
    pass # 일단 아무것도 하지 않고 함수를 통과시키기

# NLP 파이프라인 객체 접근 함수 정의
def get_nlp_pipeline():
    if _nlp_pipeline is None:
        raise HTTPException(status_code=503, detail="NLP 서비스 준비 안됨")
    return _nlp_pipeline

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

assets_path = os.path.join(BASE_DIR, "frontend", "dist", "assets")
images_path = os.path.join(BASE_DIR, "frontend", "dist", "images")  # 변경

app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
app.mount("/images", StaticFiles(directory=images_path), name="images")
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend", "dist", "static")), name="static")

index_path = os.path.join(BASE_DIR, "frontend", "dist", "index.html")
# 기본 경로 index.html 제공
@app.get("/")
async def root():
    return FileResponse(index_path)

# 2. CORS 미들웨어 설정 추가
origins = [
    "http://localhost",
    "http://localhost:5173",  # Front-end 개발 서버 주소
]

# CORS 설정 (배포시 보안 항상 확인)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# 데이터 모델 정의
# --------------------
class ScheduleItem(BaseModel):
    time: dict = None  # 시간정보(예: {'value': '2023년 8월 1일 10시'})
    location: Optional[str]  # 장소명(문자열)
    event: Optional[str]  # 이벤트명(문자열)

class TextRequest(BaseModel):
    text: str  # 사용자 입력 텍스트

# --------------------
# 일정 파싱 보조 함수
# --------------------
def split_schedule_parts(text: str):
    """
    문장 내 '시'까지는 시간, '시'부터 '에서'까지는 장소, 그 뒤는 이벤트로 분리.
    '시' 미존재시 전체를 이벤트로 반환.
    """
    si_pos = text.find('시')
    if si_pos == -1:
        return None, None, text.strip()
    eseo_pos = text.find('에서', si_pos)
    time_part = text[:si_pos + 1].strip()
    if eseo_pos == -1:
        place_part = text[si_pos + 1:].strip(); event_part = ""
    else:
        place_part = text[si_pos + 1:eseo_pos].strip()
        event_part = text[eseo_pos + 2:].strip()
    return time_part, place_part, event_part

def pick_valid_location(locations: List[str]) -> str:
    """
    숫자에서 끝나거나 짧은 후보는 제외하고, 유효한 장소명 반환
    """
    candidates = [loc for loc in locations if not loc.isdigit() and len(loc) > 1]
    return candidates[0] if candidates else "위치 없음"

# --------------------
# 기본 페이지/인증 엔드포인트
# --------------------
@app.get("/home")
def home():
    """홈 페이지 (frontend/index.html) 반환"""
    # frontend/index.html 경로를 정확하게 지정합니다.
    # 파일 구조상 index.html이 dist 안에 있는지, 바로 frontend 아래에 있는지 확인해야 합니다.
    # 제공해주신 이미지에서는 frontend 바로 아래에 index.html이 있습니다.
    # 따라서 경로는 /home/ubuntu/frontend/index.html 이 됩니다.
    index_path = os.path.join(BASE_DIR, "frontend", "index.html") 
    
    try:
        return FileResponse(index_path) 
    except Exception as e:
        return HTMLResponse(f"<h2>홈페이지 로딩 실패: 파일 경로 확인 필요: {index_path}</h2>")

@app.get("/login")
def login():
    # Google OAuth 인증 URL 생성 및 리다이렉트
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": CLIENT_REDIRECT_URI,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/calendar",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = "https://accounts.google.com/o/oauth2/v2/auth"
    req_url = requests.Request('GET', url, params=params).prepare().url
    return RedirectResponse(req_url)

@app.get("/auth/callback")
def auth_callback(code: str):
    # 🚨 CLIENT_REDIRECT_URI에서 포트 번호와 HTTP 프로토콜을 강제 제거
    # Nginx 리버스 프록시 환경에서 포트를 제거하기 위해 추가합니다.
    correct_uri = CLIENT_REDIRECT_URI.replace(":8001", "").replace("http:", "https:")
    
    # 받은 code로 access token 요청(구글 인증 완료 처리)
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": correct_uri, # <--- 수정된 URI 사용
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()
    if "access_token" in token_data:
        user_tokens['default'] = token_data
        return RedirectResponse(url="/schedule")
    else:
        raise HTTPException(status_code=400, detail="토큰 요청 실패")

@app.get("/schedule")
def schedule():
    """일정 등록(입력) 페이지 반환"""
    # 🚩 경로를 frontend/dist/schedule.html 에서 backend/static/schedule.html 로 수정합니다.
    # BASE_DIR은 /home/ubuntu 이므로, os.path.join(BASE_DIR, "backend", "static", "schedule.html") 로 수정합니다.
    schedule_path = os.path.join(BASE_DIR, "backend", "static", "schedule.html") 
    
    try:
        # FileResponse를 사용하여 파일을 안전하게 제공
        return FileResponse(schedule_path)
        
    except Exception as e:
        # 파일이 없을 경우 디버깅을 위해 파일 경로를 포함하여 에러 메시지 반환
        return HTMLResponse(f"<h2>일정 페이지 로딩 실패: 파일 경로 확인 필요: {schedule_path}</h2>")

# --------------------
# 이벤트 키워드 로드
# --------------------
def load_event_keywords(filepath="event_keywords.json"):
    """
    일정 이벤트 키워드를 JSON 파일에서 불러와 리스트 형식으로 반환
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            keywords = json.load(f)
            if isinstance(keywords, list): return keywords
    except Exception: pass
    return []

event_keywords = load_event_keywords()

# --------------------
# 일정 문장 파싱 엔드포인트
# --------------------
@app.post("/parse-multi-schedule/")
def parse_multi_schedule(req: TextRequest):
    """
    한글 여러 일정문장을 시간, 장소, 이벤트로 분해(콤마 구분)
    """
    if not req.text or not isinstance(req.text, str):
        raise HTTPException(status_code=400, detail="텍스트 입력 필드 필요")
    parts = [s.strip() for s in req.text.split(",") if s.strip()]
    schedules = []
    for part in parts:
        time_part, location_part, event_part = split_schedule_parts(part)
        time = {"value": time_part} if time_part else None
        location_candidates = [location_part] if location_part else []
        try:
            locs = extract_locations(part)
            for loc in locs:
                if loc not in location_candidates: location_candidates.append(loc)
        except Exception:
            pass
        location = pick_valid_location(location_candidates)
        # 이벤트 추출 (event_part → 명사 순서)
        event = event_part if event_part else None
        if not event:
            # # doc = nlp(part)
            # doc = get_nlp_pipeline()(part) # 👈 이 부분을 주석 처리
            # nouns = [word.text for sent in doc.sentences for word in sent.words if word.upos == "NOUN"]
            
            event = next((kw for kw in event_keywords if kw in part), None)
            # event = event or (nouns[-1] if nouns else "일정") # 👈 이 부분도 주석 처리
            event = event or "일정" # 👈 NLP 없이 기본값 '일정' 사용
            
        schedules.append({"time": time, "location": location, "event": event})
    return {"schedules": schedules}

# --------------------
# Google Calendar 인증, 이벤트 저장/중복체크
# --------------------
def get_authenticated_service(user_key: str = "default"):
    """
    저장된 토큰을 이용해 Google Calendar API 인증 세션 반환
    """
    tokens = user_tokens.get(user_key)
    if not tokens:
        raise HTTPException(status_code=401, detail="인증된 토큰이 없습니다. 로그인 필요.")
    creds = Credentials(
        token=tokens.get("access_token"), refresh_token=tokens.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    )
    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except Exception as e:
        print("Google Calendar 서비스 빌드 실패:", e)
        raise HTTPException(status_code=500, detail="Google 서비스 생성 실패")

@app.post("/check_duplicates/")
def check_duplicates(items: List[ScheduleItem], user_key: str = "default"):
    """
    일정 리스트에서 Google Calendar에 겹치는 일정이 있는지 확인
    """
    try:
        service = get_authenticated_service(user_key)
    except HTTPException as e:
        raise e
    duplicates = []
    for i, schedule in enumerate(items):
        if schedule.time and schedule.time.get("value"):
            dt = safe_parse_datetime(schedule.time)
            if not dt: continue
            start_dt = dt; end_dt = start_dt + datetime.timedelta(hours=1)
            existing_events_res = service.events().list(
                calendarId="primary",
                timeMin=start_dt.isoformat(), timeMax=end_dt.isoformat(),
                singleEvents=True, orderBy="startTime"
            ).execute()
            existing_events = existing_events_res.get("items", [])
            for ev in existing_events:
                duplicates.append({
                    "schedule": {
                        "summary": schedule.event or "일정",
                        "location": schedule.location or "",
                        "start": start_dt.isoformat(),
                        "end": end_dt.isoformat(),
                    },
                    "existing_event": ev
                })
                break
    return {"has_duplicates": len(duplicates) > 0, "duplicates": duplicates}

@app.post("/register-google-calendar/")
def register_google_calendar(items: List[ScheduleItem], user_key: str = "default"):
    """
    리스트로 전달받은 일정을 Google Calendar에 등록 (중복은 업데이트)
    """
    created_ids = []; failed_items = []
    try:
        service = get_authenticated_service(user_key)
    except HTTPException as e:
        raise e
    for i, schedule in enumerate(items):
        try:
            dt = safe_parse_datetime(schedule.time)
            if not dt: continue
            start_dt = dt; end_dt = start_dt + datetime.timedelta(hours=1)
            # 기존 일정 확인 및 insert/update 분기
            existing_events = service.events().list(
                calendarId="primary",
                timeMin=start_dt.isoformat(), timeMax=end_dt.isoformat(),
                singleEvents=True, orderBy="startTime"
            ).execute()["items"]
            duplicate_event_id = existing_events[0]["id"] if existing_events else None
            event_body = {
                "summary": schedule.event or "일정",
                "location": schedule.location or "",
                "start": {"dateTime": start_dt.isoformat(), "timeZone": "Asia/Seoul"},
                "end": {"dateTime": end_dt.isoformat(), "timeZone": "Asia/Seoul"},
            }
            if duplicate_event_id:
                event = service.events().update(
                    calendarId="primary", eventId=duplicate_event_id, body=event_body
                ).execute()
            else:
                event = service.events().insert(
                    calendarId="primary", body=event_body
                ).execute()
            created_ids.append(event.get("id"))
        except Exception as e:
            failed_items.append({"schedule": schedule, "error": str(e)})
            continue
    return {"created_event_ids": created_ids, "failed_items": failed_items}

# --------------------
# 한글 시간 파싱 전처리 및 변환
# --------------------
def safe_parse_datetime(time_obj):
    """
    시간 문자열/객체를 datetime으로 변환 (상대표현, 오전/오후 등 한글 지원)
    """
    now = datetime.datetime.now()
    # 시간 문자열 추출
    iso_value = None
    if isinstance(time_obj, dict):
        val = time_obj.get("value")
        iso_value = val.get("value") if isinstance(val, dict) else val
    elif isinstance(time_obj, str):
        iso_value = time_obj
    if not iso_value: return None
    # 상대 날짜 및 형식 변환 등 전처리 함수
    def replace_relative_dates(text):
        weekdays = {"월요일": 0, "화요일": 1, "수요일": 2, "목요일": 3, "금요일": 4, "토요일": 5, "일요일": 6}
        text = re.sub(r'오늘', now.strftime("%Y년 %m월 %d일"), text)
        text = re.sub(r'내일', (now + datetime.timedelta(days=1)).strftime("%Y년 %m월 %d일"), text)
        text = re.sub(r'모레', (now + datetime.timedelta(days=2)).strftime("%Y년 %m월 %d일"), text)
        match = re.search(r'다음주\s*(월요일|화요일|수요일|목요일|금요일|토요일|일요일)', text)
        if match:
            target_wd = weekdays[match.group(1)]
            today_wd = now.weekday()
            days_until_target = (target_wd - today_wd) % 7 + 7
            target_date = now + datetime.timedelta(days=days_until_target)
            target_str = target_date.strftime("%Y년 %m월 %d일")
            text = re.sub(r'다음주\s*(월요일|화요일|수요일|목요일|금요일|토요일|일요일)', target_str, text)
        return text
    def ensure_year_prefix(time_str):
        if re.search(r'\b\d{4}년\b', time_str) or re.search(r'\b\d{4}[-/]', time_str):
            return time_str.strip()
        else:
            return f"{now.year}년 {time_str.strip()}"
    def convert_am_pm(time_str):  # 오전/오후 2시 표현 지원
        def conv(m):
            ampm, hour = m.group(1), int(m.group(2))
            if ampm == "오후" and hour < 12: hour += 12
            elif ampm == "오전" and hour == 12: hour = 0
            return f"{hour:02d}:00"
        return re.sub(r'(오전|오후)\s*(\d{1,2})시', conv, time_str)
    def clean_date_format(time_str):
        time_str = re.sub(r'\s+', ' ', time_str).strip()
        time_str = re.sub(r'(\d{4})년', r'\1-', time_str)
        time_str = re.sub(r'(\d{1,2})월', r'\1-', time_str)
        time_str = re.sub(r'\s*(\d{1,2})일\s*', r'\1 ', time_str)
        time_str = re.sub(r'-{2,}', '-', time_str)
        return time_str.strip('- ')
    # 전처리 적용 및 파싱
    iso_value = replace_relative_dates(iso_value)
    iso_value = ensure_year_prefix(iso_value)
    iso_value = convert_am_pm(iso_value)
    iso_value = clean_date_format(iso_value)
    parsed = dateparser.parse(iso_value, languages=['ko'], settings={'RELATIVE_BASE': now, 'PREFER_DATES_FROM': 'future'})
    if not parsed: return None
    dt = parsed
    if dt.tzinfo is None: dt = dt.replace(tzinfo=ZoneInfo("Asia/Seoul"))
    else: dt = dt.astimezone(ZoneInfo("Asia/Seoul"))
    return dt

# --------------------
# 장소 추출 보조 함수
# --------------------
def is_place_like(s: str) -> bool:
    """
    입력 문자열이 장소 형태명사나 장소키워드 포함 여부 반환
    """
    place_words = ['회의실', '카페', '도서관', '라운지', '세미나실', '출구', '동', '호', '층']
    return any(w in s for w in location_keywords_extended + place_words)

def pick_final_location(candidates: list[str]) -> str:
    """
    후보 장소를 길이/키워드 포함 빈도 기준으로 정렬하여 최적 후보 반환
    """
    filtered = [
        c for c in candidates
        if len(c) > 1 and not c.isdigit() and is_place_like(c)
    ]
    if filtered:
        filtered.sort(key=lambda x: (len(x), sum([x.count(w) for w in location_keywords_extended])), reverse=True)
        return filtered[0]
    normal_filtered = [c for c in candidates if len(c) > 1 and not c.isdigit()]
    if normal_filtered:
        normal_filtered.sort(key=len, reverse=True)
        return normal_filtered[0]
    return "위치 정보 없음"
