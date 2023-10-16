import logging

from playwright.sync_api import Locator, expect

from utils.constants import PHONE_COUNTRY_CODE_VALUE_MATCH, NATIONALITY_CODE_VALUE_MATCH, GENDER_CODE_VALUE_MATCH
from actions.BasePageActions import BasePageActions

logger = logging.getLogger(__name__)


class PassengerDetailsActions(BasePageActions):
    """Class contains actions for passengers details page"""
    GENDER_FORM_INPUT = "xpath=//div[contains(@class, 'PassengerForm__GenderWrapper')]//select"
    DATE_OF_BIRTH_FORM_INPUT = "xpath=//div[contains(@class,'InputGroup') and .//span[text()='Date of birth']]"
    PASSPORT_OR_ID_FORM_INPUT = "xpath=//div[contains(@class, 'Document__FieldWrapper')]//input[@name='idNumber']"

    ERROR_TOOLTIP = "xpath=//div[contains(@class, 'Tooltip__StyledFormFeedbackTooltip')]"

    @property
    def primary_passenger_form(self) -> Locator:
        """Primary passenger form locator"""
        return self.page.get_by_test_id("ReservationPassenger").first

    def set_email(self, email: str) -> None:
        """
        Method provides setting email for passenger in contact info form
        :param email: email to set in form
        """
        contact_form = self.page.get_by_test_id("contact-account-promotion")
        contact_form.get_by_test_id("contact-email").fill(email)

    def set_phone_number(self, phone: str) -> None:
        """
        Method provides setting phone number for passenger in contact info form
        :param phone: phone number to set in form, expected in following format: "+country_code phone_number"
        """
        contact_form = self.page.get_by_test_id("contact-account-promotion")
        phone_country_code, phone_number = phone.split()
        phone_country_value = PHONE_COUNTRY_CODE_VALUE_MATCH.get(phone_country_code)

        contact_form.get_by_test_id("contact-phone-country").select_option(phone_country_value)
        contact_form.get_by_test_id("contact-phone").fill(phone_number)

    def set_passenger_contact_info(self, email: str, phone_number: str) -> None:
        """
        Method provides setting information in passenger contacts form
        :param email: email to set in form
        :param phone_number: phone number to set in form, expected in following format: "+country_code phone_number"
        """
        logger.info(f"Set passengers contacts info: email: {email}, phone number: {phone_number}")
        self.wait_page_loaded()
        self.set_email(email)
        self.set_phone_number(phone_number)

    def set_passenger_info(self, passenger_from_locator: Locator, first_name: str = None, last_name: str = None,
                           nationality: str = None, gender: str = None, date_of_birth: str = None,
                           passport_or_id: int = None, passport_or_id_exp_date: str = None):
        """
        Method provides setting passenger's personal information. If any of these arguments is None - field is
        left empty
        :param passenger_from_locator: locator to passenger's personal information form
        :param first_name: passenger's first name
        :param last_name: passenger's last name
        :param nationality: passenger's nationality
        :param gender: passenger's gender
        :param date_of_birth: passenger's date of birth, expected in following format: "day month_name year"
        :param passport_or_id: passenger's passport or id number
        :param passport_or_id_exp_date: passenger's passport or id expiration date,
                                        expected in following format: "day month_name year"
        """
        # Set first name and last name
        if first_name is not None:
            passenger_from_locator.get_by_test_id("ReservationPassenger-FirstName"
                                                  ).get_by_placeholder("e.g. Harry James").fill(first_name)
        if last_name is not None:
            passenger_from_locator.get_by_test_id("ReservationPassenger-LastName"
                                                  ).get_by_placeholder("e.g. Brown").fill(last_name)
        # Select nationality
        if nationality is not None:
            nationality_code = NATIONALITY_CODE_VALUE_MATCH.get(nationality)
            passenger_from_locator.get_by_test_id("ReservationPassenger-nationality").select_option(nationality_code)

        # Select gender
        if gender is not None:
            gender_code = GENDER_CODE_VALUE_MATCH.get(gender)
            passenger_from_locator.locator(self.GENDER_FORM_INPUT).select_option(gender_code)

        # Select date of birth
        if date_of_birth is not None:
            date_of_birth_input = passenger_from_locator.locator(self.DATE_OF_BIRTH_FORM_INPUT)
            self.set_date_input(date_of_birth_input, *date_of_birth.split())

        # Enter passport number
        passenger_document = passenger_from_locator.get_by_test_id("ReservationPassengerDocument")
        if passport_or_id is not None:
            passenger_document.locator(self.PASSPORT_OR_ID_FORM_INPUT).fill(str(passport_or_id))

        # Enter passport expiration date
        if passport_or_id_exp_date is not None:
            date_picker = passenger_document.get_by_test_id("DatePickerField-switcher-text")
            self.set_date_input(date_picker, *passport_or_id_exp_date.split())

    def set_primary_passenger_info(self, **kwargs) -> None:
        """
        Method provides setting primary passenger's personal information. If any of these arguments is None - field is
        left empty:
        :param kwargs: following arguments:
            first_name: passenger's first name
            last_name: passenger's last name
            nationality: passenger's nationality
            gender: passenger's gender
            date_of_birth: passenger's date of birth, expected in following format: "day month_name year"
            passport_or_id: passenger's passport or id number
            passport_or_id_exp_date: passenger's passport or id expiration date,
                                     expected in following format: "day month_name year"
        """
        logger.info(f"Set primary passenger info: {kwargs}")
        self.set_passenger_info(self.primary_passenger_form, **kwargs)

    def remove_passenger(self, passenger_number: int) -> None:
        """
        Method provides removing passenger from flight (remove passenger details card from the page)
        :param passenger_number: passenger ordinal number to remove
        """
        logger.info(f"Remove {passenger_number} passenger")
        # From ordinal number to index
        index = passenger_number - 1

        passenger_form = self.page.get_by_test_id("ReservationPassenger").all()[index]
        passenger_form.get_by_test_id("removePassengerButton").click()
        expect(self.page.get_by_test_id("ReservationPassenger"), "Passenger wasn't removed").to_have_count(index)

    def continue_next_page(self) -> None:
        """
        Method clicks continue button to process to the next page of checkout form
        """
        logger.info("Click 'Continue'")
        self.page.get_by_test_id("StepControls-passengers-next").click()
        self.wait_page_loaded()

    def check_error_message_in_primary_passenger_passport_or_id_exp_date(self, expected_error: str) -> None:
        """
        Method verifies that expected error message appeared near passport expiration date form for the
        primary passenger
        """
        logger.info(f"Check expected error message at primary passenger passport or id expiration date: "
                    f"{expected_error}")
        expect(self.primary_passenger_form.get_by_test_id("DatePickerField-switcher-text").locator(
            self.ERROR_TOOLTIP), "Unexpected primary passenger passport or id expiration date"
        ).to_contain_text(expected_error)
