from docs.get_chart import chart_update
from docs.openai_utils import ai_choise

# 데이터베이스 업데이트
chart_update()

# ai 답변 로드
decision,reason = ai_choise()

print(decision)
print(reason)
'''
5개? 7개?
최종 레버리지는 전체로 한다면 max 3 5 10배정도로
나눠서 넣는다면 10~30배
이거는 좀 고민해보자 기획해봐야겠어
'''