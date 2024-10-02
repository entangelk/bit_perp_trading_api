from openai import OpenAI
from docs.cal_chart import cal_chart
from docs.get_news import get_bitcoin_news
from docs.get_orderbook import fetch_order_book_bybit
from dotenv import load_dotenv
import os
from docs.get_current import fetch_investment_status
from docs.greed import greed
import json

def read_base64_screenshot(file_path):
    """
    Base64로 인코딩된 스크린샷 파일을 읽어오는 함수
    :param file_path: Base64 텍스트 파일 경로
    :return: Base64 문자열
    """
    try:
        with open(file_path, "r") as file:
            base64_data = file.read()
            return base64_data
    except Exception as e:
        print(f"파일 읽기 중 오류 발생: {e}")
        return None

def ai_choise():
    load_dotenv()
    OPEN_API_KEY = os.getenv("OPEN_API_KEY")

    client = OpenAI(api_key=OPEN_API_KEY)

    # 탐욕지수 불러오기
    greed_point = greed()

    # 뉴스 헤드라인 가져오기
    news_headlines = get_bitcoin_news()

    # 오더북 데이터 가져오기
    orderbook = fetch_order_book_bybit(symbol="BTCUSDT", category="linear", limit=500)

    # 지표 계산값 로드
    df_15m, df_1h, df_30d = cal_chart()

    df_15m = df_15m[-50:].to_json()
    df_1h = df_1h[-12:].to_json()
    df_30d = df_30d[-30:].to_json()

    # 현재 내 상태 로드
    balance, positions = fetch_investment_status()

    # Base64로 인코딩된 스크린샷 읽기
    screenshot_base64 = read_base64_screenshot("screenshot_base64.txt")

    # AI에게 제공할 데이터에 스크린샷(Base64)을 추가
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are an expert in Bitcoin perpetual investing. Analyze the provided data including technical indicators, market data, recent news headlines, and the Fear and Greed Index. Tell me whether to buy, sell, or hold at the moment. Consider the following in your analysis:
                - Technical indicators and market data
                - Recent news headlines and their potential impact on Bitcoin price
                - The Fear and Greed Index and its implications
                - Overall market sentiment
                - Recent visual chart data (Base64 screenshot)
                
                Response in json format.

                Response Example:
                {"decision": "superbuy", "reason": "some technical, fundamental, and sentiment-based reason"}
                {"decision": "buy", "reason": "some technical, fundamental, and sentiment-based reason"}
                {"decision": "supersell", "reason": "some technical, fundamental, and sentiment-based reason"}
                {"decision": "sell", "reason": "some technical, fundamental, and sentiment-based reason"}
                {"decision": "hold", "reason": "some technical, fundamental, and sentiment-based reason"}"""
            },
            {
                "role": "user",
                "content": f"""Current investment status: {json.dumps(positions)}
Orderbook: {json.dumps(orderbook)}
15m OHLCV with indicators (15 minute): {df_15m}
Daily OHLCV with indicators (30 days): {df_30d}
Hourly OHLCV with indicators (24 hours): {df_1h}
Recent news headlines: {json.dumps(news_headlines)}
Fear and Greed Index: {json.dumps(greed_point)}
Recent chart screenshot (Base64): {screenshot_base64}"""
            }
        ],
        response_format={
            "type": "json_object"
        }
    )

    # 응답의 텍스트를 JSON 형식으로 변환
    response_content = response.choices[0].message.content
    response_json = json.loads(response_content)

    decision = response_json['decision']
    reason = response_json['reason']
    print(response_json['decision']) 
    print(response_json['reason'])    

    return decision, reason

if __name__ == "__main__":
    ai_choise()
