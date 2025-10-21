# 1. 공식 Python 3.11 슬림 이미지를 베이스로 사용
FROM python:3.11-slim

# 2. 필수 빌드 도구 설치 (spaCy 등 빌드시 필요)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 3. 작업 폴더 지정 및 소스 복사
WORKDIR /app
COPY . /app

# 4. Python 패키지 설치
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 5. spaCy 한국어 모델 설치
RUN python -m spacy download ko_core_news_lg

# 6. FastAPI(Uvicorn) 앱 실행 명령 (개발용 reload, 운영시 --reload 삭제)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
