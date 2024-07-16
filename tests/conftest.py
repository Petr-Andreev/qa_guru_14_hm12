import os
import allure
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selene import browser
from selenium.webdriver.chrome.options import Options

from utils import attach


DEFAULT_BROWSER_VERSION = "121.0"


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='100.0'
    )


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')

    driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
        options=options
    )

    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.base_url = 'https://demoqa.com'
    browser.config.driver = driver
    # options.add_argument("--headless")

    yield
    with allure.step('Создаём скриншот по завершению теста'):
        attach.add_screenshot(browser)

    with allure.step('Добавляем логи по завершению теста'):
        attach.add_logs(browser)

    with allure.step('Создаём скриншот по завершению теста'):
        attach.add_html(browser)

    with allure.step('Добавляем видео к отчету'):
        attach.add_video(browser, video_url="https://selenoid.autotests.cloud/video/")

    with allure.step('Закрываем браузер'):
        browser.quit()
