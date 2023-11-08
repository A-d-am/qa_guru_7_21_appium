import allure
import pytest
import allure_commons
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selene import browser, support
from appium import webdriver
from qa_guru_7_21_appium.utils.allure_utils import (
    attach_bstack_video,
    attach_screenshot,
    attach_page_source
    )

from config import config

@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    if request.param == 'android':
        options = UiAutomator2Options().load_capabilities(
            {
                # Specify device and os_version for testing
                "platformName": request.param,
                "platformVersion": config.android_platformVersion,
                "deviceName": config.android_deviceName,
                # Set URL of the application under test
                "app": config.android_app_url,
                'appWaitActivity': 'org.wikipedia.*',
                # Set other BrowserStack capabilities
                'bstack:options': {
                    "projectName": "First Python project",
                    "buildName": "browserstack-build-1",
                    "sessionName": "BStack first_test",
                    # Set your access credentials
                    "userName": config.bstack_userName,
                    "accessKey": config.bstack_accessKey,
                },
            }
        )

    elif request.param == 'ios':
        options = XCUITestOptions().load_capabilities(
            {
                # Set URL of the application under test
                "app": config.ios_app_url,
                # Specify device and os_version for testing
                "deviceName": config.ios_deviceName,
                "platformName": request.param,
                "platformVersion": config.ios_platformVersion,
                # Set other BrowserStack capabilities
                "bstack:options": {
                    "userName": config.bstack_userName,
                    "accessKey": config.bstack_accessKey,
                    "projectName": "First Python Local project",
                    "buildName": "browserstack-build-1",
                    "sessionName": "BStack local_test",
                    "local": "false",
                },
            }
        )

    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            'http://hub.browserstack.com/wd/hub', options=options
        )

    browser.config.timeout = config.timeout
    browser.config.driver_options = options
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    session_id = browser.driver.session_id

    attach_screenshot(browser)
    attach_page_source(browser)

    browser.quit()

    attach_bstack_video(session_id)


ios = pytest.mark.parametrize('mobile_management', ['ios'], indirect=True)
android = pytest.mark.parametrize('mobile_management', ['android'], indirect=True)

