import allure
import pytest
import allure_commons
from selene import browser, support
from appium import webdriver
from qa_guru_7_21_appium import utils
from qa_guru_7_21_appium.utils.allure_utils import (
    attach_bstack_video,
    attach_screenshot,
    attach_page_source
)
import project


config = project.Config(_env_file=utils.file.relative_from_root(f'.env.{project.Config().context}'))

@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            config.driver_remote_url, options=config.driver_options(request.param)
        )

    browser.config.timeout = config.timeout
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    session_id = browser.driver.session_id

    attach_screenshot(browser)
    attach_page_source(browser)

    with allure.step('tear down app session with id: ' + session_id):
        browser.quit()

    if config.is_bstack_run(request.param):
        attach_bstack_video(session_id, config.bstack_userName, config.bstack_accessKey)


ios = pytest.mark.parametrize('mobile_management', ['ios'], indirect=True)
android = pytest.mark.parametrize('mobile_management', ['android'], indirect=True)
