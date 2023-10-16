import logging

import pytest
from playwright.sync_api import expect

from utils.constants import BASE_URL
from actions.MainPageActions import MainPageActions
from actions.PassengerDetailsActions import PassengerDetailsActions
from actions.SearchResultsActions import SearchResultsActions

logger = logging.getLogger(__name__)


class BaseTest:

    @classmethod
    def init_actions(cls, page):
        cls.main_page_actions = MainPageActions(page)
        cls.search_results_actions = SearchResultsActions(page)
        cls.passenger_details_actions = PassengerDetailsActions(page)

    @pytest.fixture(autouse=True)
    def home_page(self, browser):
        logger.info(f'Launch browser and open: {BASE_URL}')
        page = browser.new_page()
        page.goto(BASE_URL)

        expected_title = page.title()
        expect(page).to_have_title(expected_title)
        self.init_actions(page)

        yield page
