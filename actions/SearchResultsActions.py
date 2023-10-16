import logging

from playwright.sync_api import Locator, expect

from utils.constants import StopsFilterValues, ExcludeCountriesFilterValues
from actions.BasePageActions import BasePageActions, BaseModalActions

logger = logging.getLogger(__name__)


class LogInModalActions(BaseModalActions):
    """Class contains actions for log in modal card"""

    def continue_as_guest(self):
        """
        Method provides clicking "Continue as guest" button at log in modal
        """
        logger.info("Click 'Continue as guest'")
        self.modal_window.get_by_test_id("MagicLogin-GuestTextLink").click()
        self.wait_modal_closed()


class FlightDetailsModalActions(BaseModalActions):
    """Class contains actions for flight details modal card"""
    LAYOVER_DETAILS_CONTAINER = "xpath=//div[contains(@class, 'SectorStopstyled__SectorFlightLayover')]"

    def check_number_of_transfers(self, expected_number: int) -> None:
        """
        Method verifies actual number of transfers for each part of the trip matches with expected one
        :param expected_number: expected number of transfers
        """
        logger.info(f"Check number of transfers is {expected_number}")
        full_trip_parts = self.modal_window.get_by_test_id("TripPopupWrapper").all()
        for trip_part_name, trip_part_data in zip(["Trip from", "Trip to"], full_trip_parts):
            expect(trip_part_data.locator(self.LAYOVER_DETAILS_CONTAINER),
                   f'Unexpected number of layovers for {trip_part_name}').to_have_count(expected_number)

    def click_select_button(self) -> LogInModalActions:
        """
        Method provides clicking "Select" button on flight details modal card
        """
        logger.info("Click select button")
        self.modal_window.get_by_test_id("DetailBookingButton").click()
        expect(self.modal_window, "Flight details modal window wasn't closed").not_to_be_visible()
        login_modal_locator = self.base_page.get_by_test_id("MagicLogin")
        log_in_modal = LogInModalActions(login_modal_locator)
        log_in_modal.wait_modal_opened()
        return log_in_modal


class SearchResultsActions(BasePageActions):
    """Class contains actions for search flight results page"""
    FILTER_TITLE = "xpath=//div[contains(@class, 'Slide__StyledSlide')]"

    def open_filter(self, filter_locator: Locator) -> None:
        """
        Method provides opening filter on the search result page if it is closed
        :param filter_locator: locator object with expected filter to be opened
        """
        is_hidden = filter_locator.locator(self.FILTER_TITLE).is_hidden()
        if is_hidden:
            # If filter is closed it is needed to be opened
            filter_locator.get_by_role('button').first.click()
            expect(filter_locator.locator(self.FILTER_TITLE), "Filter wasn't opened").not_to_be_hidden()

    def set_stops_filter(self, filter_value: StopsFilterValues) -> None:
        """
        Method provides setting stops filter values on search results page
        :param filter_value: expected value to set
        """
        logger.info(f"Set stops filter value: {filter_value}")
        stops_filter = self.page.get_by_test_id("FilterHeader-stops")
        self.open_filter(stops_filter)
        stops_filter.locator(f"xpath=//span[text()='{filter_value.value}']").click()
        self.wait_page_loaded()

    def set_exclude_country_filter(self, filter_value: ExcludeCountriesFilterValues, with_search: bool = True) -> None:
        """
        Method provides setting exclude countries for transition filter values on search results page
        :param filter_value: expected value to set
        :param with_search: True - to search filter value before selecting
        """
        logger.info(f"Set exclude country filter value: {filter_value}")
        exclude_countries_filter = self.page.get_by_test_id("FilterHeader-countries")
        self.open_filter(exclude_countries_filter)
        if with_search:
            # click search country
            exclude_countries_filter.get_by_test_id("Multiselect-SelectSearchButton").click()
            exclude_countries_filter.get_by_placeholder("Search countries").fill(filter_value.value)
            exclude_countries_filter.get_by_test_id("CountriesFilterChoiceGroup-inResults"
                                                    ).get_by_role("checkbox").check(force=True)
        else:
            exclude_countries_filter.locator("xpath=//label").filter(has_text=filter_value.value).click()

        self.wait_page_loaded()

    def select_first_flight(self) -> FlightDetailsModalActions:
        """
        Method provides selecting first flight (open flight details modal) on search results page
        :return: opened modal available actions
        """
        logger.info("Select first flight")
        self.page.get_by_test_id("ResultCardWrapper").first.click()
        flight_details_modal = self.page.get_by_test_id("ResultCardModal")
        opened_modal = FlightDetailsModalActions(self.page, flight_details_modal)
        opened_modal.wait_modal_opened()
        return opened_modal
