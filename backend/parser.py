import stanza
import re
import json
import os

# Stanza 한국어 파이프라인 초기화 객체(전역 재사용용)
_nlp = None

def get_nlp():
    """
    Stanza 한국어 파이프라인 초기화 및 반환.
    최초 호출 시에만 Pipeline 객체를 생성, 이후 재사용.
    토크나이징, 품사태깅, 표제어 추출 포함.
    """
    global _nlp
    if _nlp is None:
        _nlp = stanza.Pipeline(lang="ko", processors="tokenize,pos,lemma")
    return _nlp


def load_location_keywords(filepath="locations.json"):
    """
    지정한 JSON 파일에서 위치 키워드 리스트를 로드.
    - 파일이 존재하고 리스트 형태면 반환
    - 실패하거나 형식이 맞지 않으면 빈 리스트 반환
    """
    if os.path.exists(filepath):
        with open(filepath, encoding="utf-8") as f:
            lst = json.load(f)
            if isinstance(lst, list):
                return lst
    return []

def load_location_keywords_extended(filepath="locations_extended.json"):
    """
    확장 위치 키워드 리스트 JSON 파일에서 로드
    """
    if os.path.exists(filepath):
        with open(filepath, encoding="utf-8") as f:
            lst = json.load(f)
            if isinstance(lst, list):
                return lst
    return []


# 기본 위치 키워드 로드
location_keywords = load_location_keywords()
# 기본 + 확장 위치 키워드 합치기
location_keywords_extended = location_keywords + load_location_keywords_extended()



def extract_locations(text: str):
    """
    입력 텍스트에서 위치명 후보 추출 함수.
    - Stanza NLP 파이프라인으로 문장 분석 (현재 결과는 미활용)
    - 정규식으로 위치 키워드+번호+장소명 형태 패턴 탐색
    - 숫자만 있거나 길이 1 이하, 중복 후보는 제외
    - 정규식 매칭 없으면 키워드 포함 단순 탐색

    반환: 위치 후보 리스트
    """

    nlp = get_nlp()
    _ = nlp(text)  # 형태소 분석 수행 (향후 확장 가능)

    entities = []

    # 정규식 패턴: 위치 키워드 + (숫자+층/호/번/출구) + (장소명 한글/영문 포함)
    pattern = re.compile(
        r'((?:' + '|'.join(map(re.escape, location_keywords_extended)) + r')'  # 위치 키워드 중 하나
        r'(?:[\s\d]{0,7}(?:층|호|번|출구)?)?'  # (예: 3층, 201호) 숫자+장소 단위 0~7자리
        r'(?:\s*[가-힣A-Za-z]+)?'              # (예: 세미나실, Café) 뒤이어 한글/영문 단어 가능
        r')'
    )

    # 정규식과 매칭되는 모든 위치 후보 추가
    for match in pattern.finditer(text):
        value = match.group(0).strip()
        if not value.isdigit() and len(value) > 1 and value not in entities:
            entities.append(value)

    # 패턴 탐색 실패 시, 단순 포함 여부 기반 후보 추가
    if not entities:
        for kw in location_keywords_extended:
            if kw in text and kw not in entities:
                entities.append(kw)

    return entities




def safe_parse_datetime(time_obj):
    """
    한글 시간 표현 포함 자유로운 datetime 변환 함수
    - 상대 날짜 (내일, 모레, 다음주 월요일 등) 치환
    - 연도 미표기시 현재 연도 자동 부여
    - 날짜 표현 정리 (년, 월, 일 텍스트 제거 및 포맷 통일)
    - dateparser 라이브러리로 최종 파싱
    - timezone Asia/Seoul 적용
    - 실패시 None 반환
    """

    import datetime
    import re
    from zoneinfo import ZoneInfo
    import dateparser

    now = datetime.datetime.now()

    # 상대 날짜 텍스트 치환 함수 (내일, 모레, 다음주 월요일)
    def replace_relative_dates(text):
        text = re.sub(r'내일', (now + datetime.timedelta(days=1)).strftime("%Y년 %m월 %d일"), text)
        text = re.sub(r'모레', (now + datetime.timedelta(days=2)).strftime("%Y년 %m월 %d일"), text)
        # 복잡한 '다음주 월요일' 형식 간단 처리 (필요시 상세 구현)
        match = re.search(r'다음주\s*(월요일|화요일|수요일|목요일|금요일|토요일|일요일)', text)
        if match:
            weekdays = {
                "월요일": 0, "화요일": 1, "수요일": 2,
                "목요일": 3, "금요일": 4, "토요일": 5, "일요일": 6,
            }
            target_wd = weekdays[match.group(1)]
            today_wd = now.weekday()
            days_until_target = (target_wd - today_wd) % 7 + 7
            target_date = now + datetime.timedelta(days=days_until_target)
            target_str = target_date.strftime("%Y년 %m월 %d일")
            text = re.sub(r'다음주\s*(월요일|화요일|수요일|목요일|금요일|토요일|일요일)', target_str, text)
        return text

    # 연도 표기 없으면 현재 연도 추가
    def ensure_year_prefix(time_str):
        if re.search(r'\b\d{4}년\b', time_str) or re.search(r'\b\d{4}[-/]', time_str):
            return time_str.strip()
        else:
            return f"{now.year}년 {time_str.strip()}"

    # 날짜 형식 정리 (다수 공백, 년/월 문자 제거, 중복 하이픈 제거 등)
    def clean_date_format(time_str):
        time_str = re.sub(r'\s+', ' ', time_str).strip()
        time_str = re.sub(r'(\d{4})년', r'\1-', time_str)
        time_str = re.sub(r'(\d{1,2})월', r'\1-', time_str)
        time_str = re.sub(r'(\d{1,2})일', '', time_str)
        time_str = re.sub(r'-{2,}', '-', time_str)
        return time_str.strip('- ')

    # 입력 time_obj에서 시간 문자열 추출
    iso_value = None
    if isinstance(time_obj, dict):
        v = time_obj.get("value")
        if isinstance(v, dict):
            iso_value = v.get("value")
        elif isinstance(v, str):
            iso_value = v
    elif isinstance(time_obj, str):
        iso_value = time_obj

    if not iso_value:
        return None

    # 전처리 순차 수행
    iso_value = replace_relative_dates(iso_value)
    iso_value = ensure_year_prefix(iso_value)
    iso_value = clean_date_format(iso_value)

    # dateparser를 사용해 파싱 시도
    parsed = dateparser.parse(
        iso_value,
        languages=['ko'],
        settings={'RELATIVE_BASE': now, 'PREFER_DATES_FROM': 'future'}
    )
    if not parsed:
        print("[WARN] dateparser 파싱 실패 (전처리 후):", iso_value)
        return None

    dt = parsed
    # timezone 적용 (Asia/Seoul)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("Asia/Seoul"))
    else:
        dt = dt.astimezone(ZoneInfo("Asia/Seoul"))

    return dt
