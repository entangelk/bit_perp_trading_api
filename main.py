from docs.get_chart import chart_update
from docs.openai_utils import ai_choise

# 데이터베이스 업데이트
chart_update()

# ai 답변 로드
decision,reason = ai_choise()


print(decision)
print(reason)
