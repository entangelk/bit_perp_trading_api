from docs.get_chart import chart_update
from docs.openai_utils import ai_choise
from docs.making_order import set_leverage,create_order_with_tp_sl,close_position
from docs.cal_order import cal_order
from docs.get_current import fetch_investment_status

# 데이터베이스 업데이트
chart_update()

# ai 답변 로드
decision,reason = ai_choise()


print(decision)
print(reason)


# 주문 적용 계수 설정

symbol="BTC/USDT"

balance, positions = fetch_investment_status()
asset = balance['USDT']['free']

# 포지션이 없을 때 주문
if positions != '[]':
    side, amount, price, leverage = cal_order(asset,decision)


    # 레버리지 설정
    set_leverage(symbol, leverage)

    # 주문
    create_order_with_tp_sl(symbol, side, amount, price=None, tp_price=None, sl_price=None)
else:
    # 포지션이 있을 경우 종료 주문 인데 이건 잠시 보류 - 포지션 종료에 대한 로직이 아직 안짜져있음
    close_position()



# 예시: BTC/USDT 무기한 선물에 0.01 BTC 매수 지정가 주문 (가격 30000 USDT)
# create_order(symbol="BTC/USDT", order_type="limit", side="buy", amount=0.01, price=30000)