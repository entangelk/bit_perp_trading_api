from openai import OpenAI
from cal_chart import cal_chart
from dotenv import load_dotenv
import os
from greed import greed
import json

def ai_choise():

  # 탐욕지수 불러오기
  greed_point = greed()

  load_dotenv()
  OPEN_API_KEY = os.getenv("OPEN_API_KEY")

  client = OpenAI(api_key=OPEN_API_KEY)

  # 지표 계산된 데이터 프레임
  cal_df = cal_chart()

  getjson = cal_df[-200:].to_json()
  pass

  response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {
        "role": "system",
        "content": [
          {
            "type": "text",
            "text": "You are an expert in Bitcoin investing. Tell me whether to sell, hold, or buy based on the data you have available. response in json format.\n\nResponse Example:\n{\"decision\" : \"buy\", \"reason\" : \"Some technical reason\"}\n{\"decision\" : \"sell\", \"reason\" : \"Some technical reason\"}\n{\"decision\" : \"hold\", \"reason\" : \"Some technical reason\"}"
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": getjson + " today FGI, Fear and Greed Index : " + str(greed_point)
          }
        ]
      },
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