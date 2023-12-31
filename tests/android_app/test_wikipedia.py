from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have, be
from conftest import android


@android
def test_search():
    with step('Click on skip button'):
        browser.element((AppiumBy.ID, "org.wikipedia:id/fragment_onboarding_skip_button")).click()

    with step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia:id/search_src_text")).type('Appium')

    with step('Verify content found'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Appium'))


@android
def test_open_article_after_search():
    with step('Click on skip button'):
        browser.element((AppiumBy.ID, "org.wikipedia:id/fragment_onboarding_skip_button")).click()

    with step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia:id/search_src_text")).type('Appium')

    with step('Verify Appium is in the serp'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Appium'))

    with step('Open first article'):
        results.first.click()

    with step('Article should be opened'):
        article_header = browser.element((AppiumBy.CLASS_NAME, "android.widget.TextView"))

        assert article_header.should(have.exact_text('Appium'))

@android
def test_onboarding():
    continue_button = browser.element((AppiumBy.ID,'org.wikipedia:id/fragment_onboarding_forward_button'))
    screen_title = browser.element((AppiumBy.ID, 'org.wikipedia:id/primaryTextView'))

    with step('First onboardign screen is opened'):
        screen_title.should(be.visible)

    with step('Click on continue button to open the second screen'):
        continue_button.click()

    with step('Second onboarding screen is opened'):
        screen_title.should(have.exact_text('New ways to explore'))

    with step('Click on continue button to open the third screen'):
        continue_button.click()

    with step('Third onboarding screen is opened'):
        screen_title.should(have.exact_text('Reading lists with sync'))

    with step('Click on continue button to open the fourth screen'):
        continue_button.click()

    with step('Fourth onboarding screen is opened'):
        screen_title.should(have.exact_text('Send anonymous data'))

    with step('Finish onboarding by clicking on the send anonymous data accept button'):
        browser.element((AppiumBy.ID,'org.wikipedia:id/acceptButton')).click()

    with step('Main tab is opened'):
        browser.element((AppiumBy.ID,'org.wikipedia:id/main_toolbar_wordmark')).should(be.visible)
