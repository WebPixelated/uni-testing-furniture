import pytest
import allure
from playwright.sync_api import Page

# Browser configuration


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Launch Chrome in non-headless mode by default; set headless=True for CI."""
    return {
        **browser_type_launch_args,
        "headless": False,
        "args": ["--start-maximized"],
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Set default viewport to full HD."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "ru-RU",
    }


# Screenshot on failure


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a full-page screenshot to the Allure report on test failure."""
    # wrapper=True (pytest 8+): yield returns the TestReport directly
    report = yield

    if report.when == "call" and report.failed:
        page: Page | None = item.funcargs.get("page")
        if page:
            try:
                screenshot_bytes = page.screenshot(full_page=True)
                allure.attach(
                    screenshot_bytes,
                    name="Screenshot on failure",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as exc:
                print(f"[conftest] Could not take screenshot: {exc}")

    return report
