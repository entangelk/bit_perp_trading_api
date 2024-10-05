from openai import OpenAI

from docs.cal_chart import cal_chart
from docs.get_news import get_bitcoin_news
from docs.get_orderbook import fetch_order_book_bybit
from dotenv import load_dotenv
import os
from docs.get_current import fetch_investment_status
from docs.greed import greed
import json

# 현재 내 상태 로드
balance, positions_json = fetch_investment_status()

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

# 포지션이 없을 때
def ai_choise(current_price):

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

    # Base64로 인코딩된 스크린샷 읽기
    screenshot_base64 = read_base64_screenshot("screenshot_base64.txt")

    # AI에게 제공할 데이터에 스크린샷(Base64)을 추가
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are an expert in Bitcoin perpetual investing. Analyze the provided data including technical indicators, market data, recent news headlines, and the Fear and Greed Index. Based on the analysis, provide the following investment decisions:
                - Entry position (buy, stay, sell)
                - Take profit (TP) and Stop loss (SL) values
                - Leverage ratio (ensure it does not exceed 10x)
                - Entry price as a percentage of the capital

                Here is the data for your analysis:
                - Technical indicators and market data
                - Recent news headlines and their potential impact on Bitcoin price
                - The Fear and Greed Index and its implications
                - Overall market sentiment
                - Recent visual chart data (Base64 screenshot)
                """
            },
#             {
#                 "role": "user",
#                 "content": f"""
#                 current_price : {current_price} USDT
# Orderbook: {json.dumps(orderbook)}
# 15m OHLCV with indicators (15 minute): {df_15m}
# Daily OHLCV with indicators (30 days): {df_30d}
# Hourly OHLCV with indicators (24 hours): {df_1h}
# Recent news headlines: {json.dumps(news_headlines)}
# Fear and Greed Index: {json.dumps(greed_point)}
# Recent chart screenshot (Base64): {screenshot_base64}"""
#             },
                        {
                "role": "user",
                "content": f"""
                current_price : {current_price} USDT
Orderbook: {json.dumps(orderbook)}
15m OHLCV with indicators (15 minute): {df_15m}
Daily OHLCV with indicators (30 days): {df_30d}
Hourly OHLCV with indicators (24 hours): {df_1h}
Recent news headlines: {json.dumps(news_headlines)}
Fear and Greed Index: {json.dumps(greed_point)}
"""
            }
        ],
            max_tokens=4095,  # 최대 토큰 수 제한
            temperature=0.5,  # 응답의 다양성 제어
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "trading_decision",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "position": {"type": "string", "enum": ["buy", "stay", "sell"]},
                            "tp": {"type": "number"},
                            "sl": {"type": "number"},
                            "leverage": {"type": "integer", "maximum": 10},
                            "entry_price_percentage": {"type": "number"},
                            "decision": {"type": "string"}
                        },
                        "required": ["position", "tp", "sl", "leverage", "entry_price_percentage", "decision"],
                        "additionalProperties": False
                    }
                }
            }
        )

    # 응답의 텍스트를 JSON 형식으로 변환
    response_content = response['choices'][0]['message']['content']
    response_json = json.loads(response_content)

    position = response_json['position']
    tp = response_json['tp']
    sl = response_json['sl']
    leverage = response_json['leverage']
    entry_price_percentage = response_json['entry_price_percentage']
    decision = response_json['decision']

    print(f"Position: {position}") 
    print(f"TP: {tp}") 
    print(f"SL: {sl}") 
    print(f"Leverage: {leverage} (Max 10x)")
    print(f"Entry Price (% of capital): {entry_price_percentage}")
    print(f"Decision: {decision}")

    return position, tp, sl, leverage, entry_price_percentage, decision







# 포지션이 있을 때
def ai_choise_run(current_price):

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

    # Base64로 인코딩된 스크린샷 읽기
    screenshot_base64 = read_base64_screenshot("screenshot_base64.txt")

    # AI에게 제공할 데이터에 스크린샷(Base64)을 추가
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are an expert in Bitcoin perpetual trading. Analyze the provided data including technical indicators, market data, recent news headlines, and the Fear and Greed Index. Based on my open position, choose between holding and closing. Consider the following in your analysis:
                - Technical indicators and market data
                - Recent news headlines and their potential impact on Bitcoin price
                - The Fear and Greed Index and its implications
                - Overall market sentiment
                - Recent visual chart data (Base64 screenshot)
                """
            },
            {
                "role": "user",
                "content": f"""Current investment status: {json.dumps(positions_json)}
                current_price : {current_price} USDT
Orderbook: {json.dumps(orderbook)}
15m OHLCV with indicators (15 minute): {df_15m}
Daily OHLCV with indicators (30 days): {df_30d}
Hourly OHLCV with indicators (24 hours): {df_1h}
Recent news headlines: {json.dumps(news_headlines)}
Fear and Greed Index: {json.dumps(greed_point)}
Recent chart screenshot (Base64): {screenshot_base64}"""
            }
        ],
        functions=[
            {
                "name": "ai_decision",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "decision": {
                            "type": "string",
                            "enum": ["close", "hold"]
                        },
                        "reason": {
                            "type": "string"
                        }
                    },
                    "required": ["decision", "reason"]
                }
            }
        ]
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
