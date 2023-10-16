import logging

from playwright.sync_api import Locator, expect

from actions.BasePageActions import BasePageActions

logger = logging.getLogger(__name__)


class MainPageActions(BasePageActions):
    """Class contains actions that relates to main home page"""
    SUGGESTION_ITEM_ADDRESS = ("xpath=//div[contains(@class, 'PlacePickerstyled__PlacePickerItemName') and "
                               "contains(text(), '{}')]")
    DATE_INPUT = ("xpath=//div[@data-test='SearchDateInput']//div[contains(@class, "
                  "'SearchFieldstyled__SearchFieldLabel') and text()='{}']")
    CALENDAR_MONTH_PICKER = ("xpath=//div[contains(@class, 'Calendarstyled__Container') and .//div[contains(@class,"
                             "'ButtonPrimitiveContentChildren') and contains(text(),'{}')]]")
    FLIGHT_MODIFICATIONS = "xpath=//div[contains(@class, 'ButtonWrapsstyled__ButtonTabletWrap')]"
    INCREMENT_BUTTON = "xpath=//button[@aria-label='increment']"
    BOOKING_COM_CONTAINER = "xpath=//div[contains(@class, 'BookingcomSwitchstyled__StyledBookingcomSwitch')]"

    def set_address(self, field_locator: Locator, address: str) -> None:
        """
        Method provides adding address to the specific field in search flight widget
        :param field_locator: locator object with target filed to set address for
        :param address: string with address. Should be in the following format "city_name, country_name"
        """
        city_name, country_name = address.split(", ")
        existing_items = field_locator.get_by_test_id("PlacePickerInputPlace")

        # Check whether existing address is already selected in the field and remove it
        for item in existing_items.all():
            if item.is_visible():
                # remove item
                item.get_by_test_id("PlacePickerInputPlace-close").click()
                expect(item, "Address wasn't removed").not_to_be_visible(timeout=10000)

        field_locator.get_by_test_id("SearchField-input").fill(city_name)
        self.page.get_by_test_id("PlacePickerRow-city").locator(self.SUGGESTION_ITEM_ADDRESS.format(address),).click(
            timeout=10000)
        expect(existing_items, f"Address {address} wasn't became set").to_contain_text(city_name, timeout=10000)

    def set_from_address(self, from_address: str) -> None:
        """
        Method provides setting from address in search flight field
        :param from_address: string with address. Should be in the following format "city_name, country_name"
        """
        logger.info(f"Set from: {from_address} in search flight form")
        from_field = self.page.get_by_test_id("SearchFieldItem-origin")
        self.set_address(from_field, from_address)

    def set_to_address(self, to_address: str) -> None:
        """
        Method provides setting from address in search flight field
        :param to_address: string with address. Should be in the following format "city_name, country_name"
        """
        logger.info(f"Set to: {to_address} in search flight form")
        to_field = self.page.get_by_test_id("SearchFieldItem-destination")
        self.set_address(to_field, to_address)

    def set_departure_and_return_dates(self, departure_date: str, return_date: str) -> None:
        """
        Method provides setting departure and return dates in search flight field
        :param departure_date: string with departure date. Should be in the following format "day month year"
        :param return_date: string with return date. Should be in the following format "day month year"
        """
        logger.info(f"Set departure: {departure_date} and return: {return_date} dates in search flight form")
        self.page.locator(self.DATE_INPUT.format('Departure')).click()
        expect(self.page.get_by_test_id("NewDatePickerOpen"), "Date picker windget wasn't opened").to_be_visible()

        for date in [departure_date, return_date]:
            day, month, year = date.split()
            displayed_months = self.page.get_by_test_id("DatepickerMonthButton").all_text_contents()
            # Search expected month calendar
            while f'{month} {year}' not in displayed_months:
                self.page.get_by_test_id("CalendarMoveNextButton").click()
                displayed_months = self.page.get_by_test_id("DatepickerMonthButton").all_text_contents()

            calendar_month_container = self.page.locator(self.CALENDAR_MONTH_PICKER.format(month))
            calendar_dates = calendar_month_container.get_by_test_id("DayDateTypography").all()
            # Click day
            [date_button for date_button in calendar_dates if date_button.text_content() == day][0].click()

        # Confirm dates
        self.page.get_by_test_id("SearchFormDoneButton").click()
        expect(calendar_month_container, "Date picker windget wasn't closed").not_to_be_visible()

    def set_number_of_passengers(self, n_adults: int) -> None:
        """
        Method provides setting number of passengers in search flight field
        :param n_adults: int with expected number of adult passengers
        """
        logger.info(f"Set number of passengers: {n_adults}")
        # Open passengers selector
        self.page.get_by_test_id("PassengersField").locator(
            self.FLIGHT_MODIFICATIONS).get_by_test_id("PassengersField-note-1").click()
        passengers_container = self.page.get_by_test_id("PassengersPopover")
        expect(passengers_container, "Passengers management widget wasn't opened").to_be_visible()

        # Set up number of adult passengers
        adults_container = passengers_container.get_by_test_id("PassengersRow-adults")
        current_number_of_adults = int(adults_container.locator("css=input").input_value())
        while current_number_of_adults < n_adults:
            adults_container.locator(self.INCREMENT_BUTTON).click()
            current_number_of_adults = int(adults_container.locator("css=input").input_value())

        passengers_container.get_by_test_id("PassengersFieldFooter-done").click()
        expect(adults_container, "Passengers management widget wasn't closed").not_to_be_visible()

    def uncheck_booking_com_checkbox(self) -> None:
        """
        Method unchecks "Check accommodation with booking.com" checkbox
        """
        logger.info("Uncheck booking.com checkbox")
        booking_com_container = self.page.locator(self.BOOKING_COM_CONTAINER)
        booking_com_container.get_by_role("checkbox").uncheck(force=True)

    def click_search_button(self) -> None:
        """
        Method clicks "Search" button in search flight field
        """
        logger.info("Click search button")
        self.page.get_by_test_id("LandingSearchButton").click()
        expect(self.page.get_by_test_id("ResultList-results"), "Results wasn't loaded").to_be_visible()
        self.wait_page_loaded()
