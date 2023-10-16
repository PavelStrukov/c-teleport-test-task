import os

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def browser():
    with sync_playwright() as playwright:
        playwright.selectors.set_test_id_attribute("data-test")
        # By default run in headed mode
        is_headless = bool(int(os.getenv('HEADLESS', 0)))
        browser = playwright.chromium.launch(headless=is_headless)

        yield browser
