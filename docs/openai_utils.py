from openai import OpenAI
from docs.cal_chart import cal_chart
from docs.get_news import get_bitcoin_news
from docs.get_orderbook import fetch_order_book_bybit
from dotenv import load_dotenv
from docs.get_current import fetch_investment_status
import os
from docs.greed import greed
import json

def ai_choise():


  load_dotenv()
  OPEN_API_KEY = os.getenv("OPEN_API_KEY")

  client = OpenAI(api_key=OPEN_API_KEY)


  # 탐욕지수 불러오기
  greed_point = greed()

  # 뉴스 헤드라인 가져오기
  news_headlines = get_bitcoin_news()

  # 오더북 데이터 가져오기
  # Bybit USDT 무기한 선물 오더북 데이터를 호출하고, 가격을 1단위로 묶어 비드와 애스크 각각 50개씩 출력
  orderbook = fetch_order_book_bybit(symbol="BTCUSDT", category="linear", limit=500)

  # 지표 계산값 로드
  df_15m, df_1h, df_30d = cal_chart()

  df_15m = df_15m[-50:].to_json()
  df_1h = df_1h[-24:].to_json()
  df_30d = df_30d[-30:].to_json()

  # 현재 내 상태 로드
  filtered_balances = fetch_investment_status()
  
  pass

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
        "content": f"""Current investment status: {json.dumps(filtered_balances)}
Orderbook: {json.dumps(orderbook)}
15m OHLCV with indicators (15 minute): {df_15m}
Daily OHLCV with indicators (30 days): {df_30d}
Hourly OHLCV with indicators (24 hours): {df_1h}
Recent news headlines: {json.dumps(news_headlines)}
Fear and Greed Index: {json.dumps(greed_point)}"""
        }
    ],

    response_format={
      "type": "json_object"
    }
  )

  # 응답의 텍스트를 JSON 형식으로 변환
  response_content = response.choices[0].message.content

  # 텍스트를 JSON으로 변환
  response_json = json.loads(response_content)

  decision = response_json['decision']
  reason = response_json['reason']
  # 'decision'과 'reason' 값 출력
  print(response_json['decision'])  # 예: "hold"
  print(response_json['reason'])    # 예: "Technical indicators are mixed. ..."

  return decision,reason