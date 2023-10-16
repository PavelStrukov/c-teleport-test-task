from BaseTest import BaseTest
from utils.constants import StopsFilterValues, ExcludeCountriesFilterValues
from definitions import PASSENGER_PERSONAL_INFO_FILE
from utils.utils import get_json_file_content

PASSENGER_CONTACT_INFO = ("some.email@gmail.com", "+7 9643993553")


class TestGuestCheckoutPassengersData(BaseTest):

    def test_fail_checkout_without_setting_passport_expiration_date_for_guest_single_transition_flight(self):

        # Close cookies modal
        self.main_page_actions.close_modal()

        # Input from
        self.main_page_actions.set_from_address(from_address="New York, United States")

        # Input to
        self.main_page_actions.set_to_address(to_address="Barcelona, Spain")

        # Select from-to dates
        self.main_page_actions.set_departure_and_return_dates(departure_date="1 July 2023", return_date="15 July 2023")

        # Set 2 passengers
        self.main_page_actions.set_number_of_passengers(n_adults=2)

        # Uncheck booking com container
        self.main_page_actions.uncheck_booking_com_checkbox()

        # Click search button
        self.main_page_actions.click_search_button()

        # Select filters: 1 stop and exclude UK
        self.search_results_actions.set_stops_filter(StopsFilterValues.ONE_STOP)
        self.search_results_actions.set_exclude_country_filter(ExcludeCountriesFilterValues.UK, with_search=True)

        # Select first flight
        flight_details_modal = self.search_results_actions.select_first_flight()

        # Check number of transfers is 1 for each part of the trip
        flight_details_modal.check_number_of_transfers(expected_number=1)

        # Click select button
        log_in_modal = flight_details_modal.click_select_button()

        # Click continue as guest
        log_in_modal.continue_as_guest()

        # Set passenger contact and personal data
        self.passenger_details_actions.set_passenger_contact_info(*PASSENGER_CONTACT_INFO)
        passenger_info = get_json_file_content(PASSENGER_PERSONAL_INFO_FILE)
        self.passenger_details_actions.set_primary_passenger_info(**passenger_info)

        # Remove second passenger
        self.passenger_details_actions.remove_passenger(passenger_number=2)

        # Click continue
        self.passenger_details_actions.continue_next_page()

        # Check passport date expiration required field error message appear
        self.passenger_details_actions.check_error_message_in_primary_passenger_passport_or_id_exp_date(
            "Required field")
