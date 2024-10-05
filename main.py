from docs.get_chart import chart_update
from docs.openai_utils import ai_choise,ai_choise_run
from docs.making_order import set_leverage,create_order_with_tp_sl,close_position
from docs.get_current import fetch_investment_status
from docs.get_chart_img import save_screenshot_as_base64



# 데이터베이스 업데이트, 현재 비트코인 가격 호출
current_price = chart_update()

# 차트 이미지 저장
save_screenshot_as_base64()


# 현재 내 상태 로드
balance, positions_json = fetch_investment_status()


# asset = balance['USDT']['free']
asset = 5

symbol="BTC/USDT"

# 포지션 상태 저장 (포지션이 open 상태일경우 True)
positions_flag = True
if positions_json == '[]' or positions_json == None:
    positions_flag = False

pass
if positions_flag:
    # 포지션이 있을 때 답변 로드
    decision, reason = ai_choise_run(current_price)
else:
    # 포지션이 없을 때 답변 로드
    position, tp, sl, leverage, entry_price_percentage, decision = ai_choise(current_price)

    pass

    if entry_price_percentage > 0.1:
        entry_price_percentage = 0.1

    pass
    # 진입할 자본 크기 설정
    amount = asset*entry_price_percentage

    pass
    # ai의 선택이 '기다림(stay)' 신호가 아닐 경우 포지션 오픈
    if position != 'stay':
        side = position  # AI가 이미 'Buy' 또는 'Sell' 반환
        pass
        # 계산된 tp가 5%가 넘을 경우 5%로 고정
        if side == 'Buy':
            # 롱 포지션: TP가 현재 가격 + 5% 이상이면, TP를 현재 가격 + 5%로 고정
            if tp > current_price + current_price * 0.05:
                tp = current_price + current_price * 0.05
        else:
            # 숏 포지션: TP가 현재 가격 - 5% 이하이면, TP를 현재 가격 - 5%로 고정
            if tp < current_price - current_price * 0.05:
                tp = current_price - current_price * 0.05
        pass
        # 레버리지 설정
        leverage_response = set_leverage(symbol, leverage)
        if leverage_response is None:
            print("레버리지 설정 실패. 주문 생성을 중단합니다.")
        else:
            # 주문
            order_response = create_order_with_tp_sl(
                symbol=symbol, 
                side=side, 
                amount=amount, 
                price=None, 
                tp_price=tp, 
                sl_price=sl
            )
            if order_response is None:
                print("주문 생성 실패.")
            else:
                print(f"주문 성공: {order_response}")




print(decision)
print(reason)

'''
# 포지션이 없을 때 주문
if positions != '[]':


    # 레버리지 설정
    set_leverage(symbol, leverage)

    # 주문
    create_order_with_tp_sl(symbol, side, amount, price=None, tp_price=None, sl_price=None)
else:
    # 포지션이 있을 경우 종료 주문 인데 이건 잠시 보류 - 포지션 종료에 대한 로직이 아직 안짜져있음
    close_position()



# 예시: BTC/USDT 무기한 선물에 0.01 BTC 매수 지정가 주문 (가격 30000 USDT)
# create_order(symbol="BTC/USDT", order_type="limit", side="buy", amount=0.01, price=30000)
'''