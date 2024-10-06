import time
import base64
import os
import io
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
from PIL import Image  # 추가
from datetime import datetime  # 추가

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage')
    return chrome_options

def create_driver():
    logger.info("ChromeDriver 설정 중...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=setup_chrome_options())
    return driver

def capture_and_encode_screenshot(driver, url):
    try:
        logger.info(f"{url} 로딩 중...")
        driver.get(url)
        
        # 페이지 로딩 대기
        time.sleep(5)  # 필요에 따라 조정
        
        # 스크린샷 캡처
        png = driver.get_screenshot_as_png()
        
        # PIL Image로 변환
        img = Image.open(io.BytesIO(png))
        
        # 이미지 리사이즈 (필요에 따라 조정)
        img.thumbnail((2000, 2000))
        
        # 현재 시간을 파일명에 포함
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bybit_chart_{current_time}.png"
        
        # 현재 스크립트의 경로를 가져옴
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 파일 저장 경로 설정
        file_path = os.path.join(script_dir, filename)
        
        # 이미지 파일로 저장
        img.save(file_path)
        logger.info(f"스크린샷이 저장되었습니다: {file_path}")
        
        # 이미지를 바이트로 변환
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        
        # base64로 인코딩
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return base64_image, file_path
    except Exception as e:
        logger.error(f"스크린샷 캡처 및 인코딩 중 오류 발생: {e}")
        return None, None

def save_screenshot_as_base64():
    driver = create_driver()
    url = "https://www.bybit.com/trade/usdt/BTCUSDT"  # 스크린샷을 찍을 URL

    try:
        # Base64로 인코딩된 파일 저장 경로 (최상위 폴더)
        base64_output_file = "screenshot_base64.txt"
        
        # 스크린샷을 찍고 Base64로 인코딩하여 파일로 저장
        base64_image, screenshot_path = capture_and_encode_screenshot(driver, url)
        
        if base64_image:
            # Base64로 인코딩된 데이터를 텍스트 파일로 저장
            with open(base64_output_file, "w") as base64_file:
                base64_file.write(base64_image)
            logger.info(f"Base64로 인코딩된 스크린샷이 성공적으로 저장되었습니다: {base64_output_file}")

        return base64_image, screenshot_path
        
    except Exception as e:
        logger.error(f"오류 발생: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    save_screenshot_as_base64()

