import os
from dotenv import load_dotenv
import requests
from pymongo import MongoClient
from datetime import datetime, timedelta

load_dotenv()

def get_bitcoin_news():
    # MongoDB에 접속
    mongoClient = MongoClient("mongodb://localhost:27017")
    # 'bitcoin' 데이터베이스 연결
    database = mongoClient["bitcoin"]
    # 'news' 컬렉션 작업
    news_collection = database['news']

    # 마지막 저장 시간 가져오기
    last_entry = news_collection.find_one(sort=[("saved_at", -1)])
    if last_entry:
        last_saved_time = last_entry["saved_at"]
        current_time = datetime.utcnow()

        # 8시간이 지났는지 확인
        if current_time - last_saved_time < timedelta(hours=8):
            print("8시간이 지나지 않았습니다. 데이터 저장을 건너뜁니다.")
            return

    # SERP API에서 데이터 가져오기
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_news",
        "q": "btc",
        "api_key": serpapi_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        news_results = data.get("news_results", [])
        headlines = []
        for item in news_results:
            headlines.append({
                "title": item.get("title", ""),
                "date": item.get("date", "")
            })

        # 최신 5개의 뉴스 저장
        if headlines:
            news_collection.insert_one({
                "headlines": headlines[:5],
                "saved_at": datetime.utcnow()  # 저장 시간 기록
            })
            print("새로운 뉴스가 저장되었습니다.")
        else:
            print("뉴스 데이터가 없습니다.")

    except requests.RequestException as e:
        print(f"뉴스 데이터를 가져오는 중 오류 발생: {e}")
