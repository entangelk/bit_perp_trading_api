from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
api_key = os.getenv("OPEN_API_KEY")

# 올바른 API 키 출력 (보안상의 이유로 실제 코드에서는 출력하지 않도록 주의)
print(f"API 키: {api_key}")  # sk-로 시작하는지 확인

# OpenAI 클라이언트 생성
client = OpenAI(api_key=api_key)

# 예시: chat.completions.create 호출
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello! How can I use OpenAI API?"}
        ]
    )
    print(response)
except OpenAI.AuthenticationError as e:
    print(f"Authentication Error: {e}")
except Exception as e:
    print(f"다른 오류 발생: {e}")
