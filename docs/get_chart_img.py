import time
import base64
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging

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

def capture_full_page_screenshot(driver, url, screenshot_filename):
    logger.info(f"{url} 로딩 중...")
    driver.get(url)
    
    logger.info("페이지가 로드될 때까지 대기 중...")
    try:
        time.sleep(10)
        logger.info("전체 페이지 스크린샷 촬영 중...")
        driver.save_screenshot(screenshot_filename)
        logger.info(f"스크린샷이 성공적으로 저장되었습니다: {screenshot_filename}")
    except Exception as e:
        logger.error(f"오류 발생: {e}")

def convert_image_to_base64(image_path, output_file):
    """
    이미지 파일을 Base64로 인코딩하고 이를 텍스트 파일에 저장하는 함수
    :param image_path: 스크린샷 파일 경로
    :param output_file: Base64 텍스트 파일 저장 경로
    """
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            # Base64로 인코딩된 데이터를 텍스트 파일로 저장
            with open(output_file, "w") as base64_file:
                base64_file.write(base64_image)
            
            logger.info(f"이미지가 Base64로 성공적으로 인코딩되고 저장되었습니다: {output_file}")
    except Exception as e:
        logger.error(f"이미지 인코딩 중 오류 발생: {e}")

def save_screenshot_as_base64():
    driver = create_driver()

    try:
        # 스크린샷 저장 경로 및 파일명
        screenshot_filename = "bybit_btc_full_page_screenshot.png"
        
        # Base64로 인코딩된 파일 저장 경로 (최상위 폴더)
        base64_output_file = "screenshot_base64.txt"
        
        # 스크린샷을 찍고 Base64로 인코딩하여 파일로 저장
        capture_full_page_screenshot(driver, "https://www.bybit.com/trade/usdt/BTCUSDT", screenshot_filename)
        convert_image_to_base64(screenshot_filename, base64_output_file)
        
    except Exception as e:
        logger.error(f"오류 발생: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    save_screenshot_as_base64()
