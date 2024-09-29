import ccxt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pymongo import MongoClient

def chart_update():
    # 환경 변수 로드
    load_dotenv()

    # Bybit API 키와 시크릿 가져오기
    BYBIT_ACCESS_KEY = os.getenv("BYBIT_ACCESS_KEY")
    BYBIT_SECRET_KEY = os.getenv("BYBIT_SECRET_KEY")

    # MongoDB에 접속
    mongoClient = MongoClient("mongodb://localhost:27017")
    # 'bitcoin' 데이터베이스 연결
    database = mongoClient["bitcoin"]
    # 'chart_15m' 컬렉션 작업
    chart_collection = database['chart_15m']

    # Bybit 거래소 객체 생성
    bybit = ccxt.bybit({
        'apiKey': BYBIT_ACCESS_KEY,
        'secret': BYBIT_SECRET_KEY,
        'options': {
            'recvWindow': 10000,  # 기본값을 10초로 증가
        },
        'enableRateLimit': True  # API 호출 속도 제한 관리 활성화
    })

    # 서버 시간 가져오기
    server_time = bybit.fetch_time() / 1000
    server_datetime = datetime.utcfromtimestamp(server_time)

    print(f"서버 시간 (UTC): {server_datetime}")

    # MongoDB에서 마지막으로 저장된 데이터의 타임스탬프 찾기
    last_saved_data = chart_collection.find_one(sort=[("timestamp", -1)])
    if last_saved_data:
        # 마지막 저장된 데이터 이후부터 데이터를 가져오기
        last_timestamp = last_saved_data["timestamp"]
        print(f"마지막으로 저장된 데이터 시점: {last_timestamp}")
    else:
        # 저장된 데이터가 없으면 기본 값을 200틱 전 시점으로 설정
        last_timestamp = server_datetime - timedelta(minutes=15 * 3500)
        print("저장된 데이터가 없습니다. 200틱 전 시점부터 데이터를 가져옵니다.")

    # 데이터 수집 시작 시간 설정 (마지막 저장된 데이터 이후)
    since_timestamp = int(last_timestamp.timestamp() * 1000)  # 밀리초 단위 타임스탬프 변환

    # 심볼 및 타임프레임 설정
    symbol = 'BTC/USDT'  # Bybit의 거래 쌍 심볼
    timeframe = '15m'  # 15분봉 데이터

    # 최대 200틱의 데이터 가져오기
    ohlcv = bybit.fetch_ohlcv(symbol, timeframe, since=since_timestamp, limit=3500)

    # MongoDB에 데이터 저장
    for data in ohlcv:
        timestamp = data[0]  # 타임스탬프 (밀리초)
        dt_object = datetime.utcfromtimestamp(timestamp / 1000)  # UTC 시간으로 변환
        open_price = data[1]
        high_price = data[2]
        low_price = data[3]
        close_price = data[4]
        volume = data[5]
        
        # 데이터 포맷
        data_dict = {
            "timestamp": dt_object,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "volume": volume
        }

        # 중복 방지를 위한 타임스탬프 기준으로 업데이트하거나 삽입
        chart_collection.update_one({"timestamp": dt_object}, {"$set": data_dict}, upsert=True)

        # 출력
        print(f"저장된 데이터: {dt_object} - O: {open_price}, H: {high_price}, L: {low_price}, C: {close_price}, V: {volume}")

    # 최신 데이터까지 가져오기
    latest_data_timestamp = max([data[0] for data in ohlcv])  # 현재 가져온 데이터의 최신 타임스탬프
    latest_ohlcv = bybit.fetch_ohlcv(symbol, timeframe, since=latest_data_timestamp + 1, limit=3500)

    for data in latest_ohlcv:
        timestamp = data[0]
        dt_object = datetime.utcfromtimestamp(timestamp / 1000)
        open_price = data[1]
        high_price = data[2]
        low_price = data[3]
        close_price = data[4]
        volume = data[5]
        
        # 데이터 포맷
        data_dict = {
            "timestamp": dt_object,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "volume": volume
        }

        # 중복 방지를 위한 타임스탬프 기준으로 업데이트하거나 삽입
        chart_collection.update_one({"timestamp": dt_object}, {"$set": data_dict}, upsert=True)

        # 출력
        # print(f"추가 저장된 최신 데이터: {dt_object} - O: {open_price}, H: {high_price}, L: {low_price}, C: {close_price}, V: {volume}")

    # print(f"총 {len(ohlcv) + len(latest_ohlcv)}개의 데이터가 MongoDB에 저장되었습니다.")
