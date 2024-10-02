import ccxt
import os
from dotenv import load_dotenv
import json



# 환경 변수 로드
load_dotenv()

# Bybit API 키와 시크릿 가져오기
BYBIT_ACCESS_KEY = os.getenv("BYBIT_ACCESS_KEY")
BYBIT_SECRET_KEY = os.getenv("BYBIT_SECRET_KEY")

# Bybit 거래소 객체 생성
bybit = ccxt.bybit({
    'apiKey': BYBIT_ACCESS_KEY,
    'secret': BYBIT_SECRET_KEY,
    'options': {
        'defaultType': 'swap',  # 무기한 선물 (perpetual swap) 용
    },
    'enableRateLimit': True  # API 호출 속도 제한 관리 활성화
})

def fetch_investment_status():
    try:
        # 현재 잔고 정보 가져오기
        balance = bybit.fetch_balance()
        print("잔고 정보:")
        print(balance)

        # 현재 포지션 정보 가져오기
        positions = bybit.fetch_positions()
        print("\n포지션 정보:")
        for position in positions:
            if float(position['contracts']) > 0:  # 포지션이 있는 경우에만 출력
                print(f"심볼: {position['symbol']}")
                print(f"진입 가격: {position['entryPrice']}")
                print(f"현재 수량: {position['contracts']}")
                print(f"미실현 손익: {position['unrealizedPnl']}")
                print(f"레버리지: {position['leverage']}")
                print(f"현재 가격: {position['markPrice']}")
                print(f"포지션 방향: {position['side']}")
                print("------")

    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")

    positions = json.dumps(positions)
    pass
    return balance, positions