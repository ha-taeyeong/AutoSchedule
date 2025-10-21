import datetime
from zoneinfo import ZoneInfo  # Python 3.9 이상에서 타임존 처리용
from google.oauth2 import service_account  # 서비스 계정 인증용
from googleapiclient.discovery import build  # Google API 클라이언트 빌드용
import traceback


# Google Calendar API 접근에 사용할 서비스 계정 JSON 파일 경로
SERVICE_ACCOUNT_FILE = 'service_account.json'  # 실제 파일 경로 확인 필수

# 캘린더 이벤트 권한 범위
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# 이벤트를 추가할 캘린더 ID (보통 본인 구글 계정 이메일)
CALENDAR_ID = 'electro0218@gmail.com'


# 서비스 계정 자격 증명(credentials) 생성
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Google Calendar API 서비스 객체 생성 (calendar v3)
service = build('calendar', 'v3', credentials=credentials)


def create_event(schedule):
    """
    schedule: dict 형태의 일정 정보.
      - schedule['time']: 시간 관련 dict, 중첩 구조 존재 가능
      - schedule['event']: 일정 제목(요약)
      - schedule['location']: 장소 정보

    Google Calendar에 일정을 생성 후, 생성된 이벤트 ID를 반환합니다.
    실패 시 None 반환.
    """

    try:
        time_obj = schedule.get("time")
        iso_value = None

        # 시간 정보 추출: time 값 내부에 'value'로 날짜시간 ISO 문자열 존재 예상
        if isinstance(time_obj, dict):
            value_obj = time_obj.get("value")
            if isinstance(value_obj, dict):
                iso_value = value_obj.get("value")  # 중첩 dict인 경우
            elif isinstance(value_obj, str):
                iso_value = value_obj  # 바로 문자열인 경우

        # iso_value가 없으면 시간 정보 없음으로 처리
        if not iso_value:
            print("시간 정보 없음")
            return None

        # ISO 8601 문자열을 datetime 객체로 변환
        dt = datetime.datetime.fromisoformat(iso_value)

        # 시간대(타임존) 할당: tzinfo가 없으면 Asia/Seoul 지정, 있으면 해당 시간대로 변환
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("Asia/Seoul"))
        else:
            dt = dt.astimezone(ZoneInfo("Asia/Seoul"))

        start_dt = dt
        end_dt = start_dt + datetime.timedelta(hours=1)  # 기본 1시간 일정, 필요시 자유롭게 변경 가능

        # 실제 이벤트 본문(body) 생성
        event_body = {
            'summary': schedule.get("event") or "일정",  # 제목, 없으면 "일정" 기본값
            'location': schedule.get("location") or "",  # 장소, 없으면 빈 문자열
            'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'Asia/Seoul'},
            'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'Asia/Seoul'}
        }

        # DEBUG 출력
        print(f"[DEBUG] iso_value: {iso_value}")
        print(f"[DEBUG] start_dt: {start_dt.isoformat()}")
        print(f"[DEBUG] end_dt: {end_dt.isoformat()}")
        print(f"[DEBUG] event_body: {event_body}")

        # Google Calendar API 호출로 이벤트 생성
        event = service.events().insert(calendarId=CALENDAR_ID, body=event_body).execute()

        print("Event created:", event.get("htmlLink"))  # 생성된 이벤트 링크 출력
        return event.get("id")  # 생성된 이벤트의 고유 ID 반환

    except Exception as e:
        print(f"이벤트 생성 실패: {e}")
        traceback.print_exc()
        return None
