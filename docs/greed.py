def greed():
    import requests

    # Alternative.me의 Fear & Greed Index API URL
    url = "https://api.alternative.me/fng/?limit=1"

    # API 호출
    response = requests.get(url)
    data = response.json()

    # 최신 공포와 탐욕 지수 정보 출력
    fear_greed_index = data["data"][0]
    print(f"날짜: {fear_greed_index['timestamp']}")
    print(f"지수 값: {fear_greed_index['value']}")
    print(f"상태: {fear_greed_index['value_classification']}")

    return fear_greed_index