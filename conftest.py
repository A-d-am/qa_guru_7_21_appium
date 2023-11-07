import allure
import pytest
import allure_commons
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selene import browser, support

from qa_guru_7_21_appium.utils import allure_utils
import project


@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    if request.param == 'android':
        options = UiAutomator2Options().load_capabilities({
            # Specify device and os_version for testing
            "platformName": request.param,
            "platformVersion": project.config.android_platformVersion,
            "deviceName": project.config.android_deviceName,

            # Set URL of the application under test
            "app": project.config.android_app_url,

            # Set other BrowserStack capabilities
            'bstack:options': {
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test",

                # Set your access credentials
                "userName": project.config.userName,
                "accessKey": project.config.accessKey
            }
        })
    elif request.param == 'ios':
        options = XCUITestOptions().load_capabilities({
            # Set URL of the application under test
            "app": project.config.ios_app_url,

            # Specify device and os_version for testing
            "deviceName": project.config.ios_deviceName,
            "platformName": request.param,
            "platformVersion": project.config.ios_platformVersion,

            # Set other BrowserStack capabilities
            "bstack:options": {
                "userName": project.config.userName,
                "accessKey": project.config.accessKey,
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test"
            }
        })

    with allure.step('init app session'):
        browser.config.driver_remote_url = project.config.driver_remote_url
        browser.config.driver_options = options

    browser.config.timeout = project.config.timeout

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    allure_utils.attach_screenshot()
    allure_utils.attach_xml()

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    allure_utils.attach_bstack_video(session_id)


ios = pytest.mark.parametrize('mobile_management', ['ios'], indirect=True)
android = pytest.mark.parametrize('mobile_management', ['android'], indirect=True)
