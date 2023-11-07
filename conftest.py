import pytest
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selene import browser
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

    browser.config.driver_remote_url = project.config.driver_remote_url
    browser.config.driver_options = options

    browser.config.timeout = project.config.timeout

    yield

    browser.quit()


ios = pytest.mark.parametrize('mobile_management', ['ios'], indirect=True)
android = pytest.mark.parametrize('mobile_management', ['android'], indirect=True)
