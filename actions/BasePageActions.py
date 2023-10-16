import logging

from playwright.sync_api import expect, Locator

from utils.constants import SEARCH_RESULTS_TIMEOUT

logger = logging.getLogger(__name__)


class BaseModalActions:
    def __init__(self, base_page, card_locator: Locator = None):
        self.base_page = base_page

        if card_locator is None:
            card_locator = self.base_page.locator("xpath=//div[contains(@class, 'Modal__ModalWrapperContent')]")

        self.modal_window = card_locator

    def click_close_modal(self) -> None:
        self.modal_window.get_by_test_id("ModalCloseButton").click()
        self.wait_modal_closed()

    def is_opened(self) -> bool:
        """Method verifies whether modal card is opened or not"""
        return self.modal_window.count() > 0

    def wait_modal_opened(self) -> None:
        """Method waits while modal card appears"""
        expect(self.modal_window, "Modal wasn't opened").to_be_visible()

    def wait_modal_closed(self) -> None:
        """Method waits while modal card disappears"""
        expect(self.modal_window, "Modal wasn't closed").not_to_be_visible()


class BasePageActions:
    """Class contains common actions for all pages"""

    def __init__(self, page):
        self.page = page

    def close_modal(self):
        """Method provides closing current opened modal on the page if it is opened"""
        logger.info("Close modal")
        modal = BaseModalActions(self.page)
        if modal.is_opened():
            modal.click_close_modal()

    def wait_page_loaded(self):
        """Method provides waiting while page become loaded (loader line disappears)"""
        expect(self.page.get_by_test_id("LoadingLine"), "Page wasn't loaded"
               ).not_to_be_visible(timeout=SEARCH_RESULTS_TIMEOUT)

    @staticmethod
    def set_date_input(date_container: Locator, day: str, month: str, year: str) -> None:
        """
        Method provides setting date info input on the page
        """
        date_container.get_by_test_id("day").fill(day)
        date_container.get_by_test_id("month").select_option(label=month)
        date_container.get_by_test_id("year").fill(year)
