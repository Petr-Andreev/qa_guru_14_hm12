import allure
import pytest
from selenium import webdriver
from selene import browser
from selenium.webdriver.chrome.options import Options

from utils import attach


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    with allure.step(f'Открываем браузер на главной странице: "https://demoqa.com"'):
        browser.config.base_url = 'https://demoqa.com'
        browser.config.window_width = 1920
        browser.config.window_height = 1080
        options = Options()
        options.page_load_strategy = 'eager'
        #options.add_argument("--headless")

        selenoid_capabilities = {
            "browserName": "chrome",
            "browserVersion": "121.0",
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True
            }
        }

        options.capabilities.update(selenoid_capabilities)
        driver = webdriver.Remote(
            command_executor="https://user1:1234@selenoid.autotests.cloud/wd/hub",
            options=options)
        browser.config.driver = driver

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
