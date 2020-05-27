from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By
from robot.api.deco import keyword
import time
import os

from selenium.webdriver.support.wait import WebDriverWait


class Error(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True


class facilenewbusinesslib(object):

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"

    """
        workaround sticazzi
    """
    _locator_dictionary = {
        "facile_logo": (By.ID, 'id:ZZ_logo'),
        "password": (By.ID, 'passwd'),
        "signin_button": (By.ID, 'SubmitLogin')
    }

    _locators = {
        "facile_logo": "id:ZZ_logo",
        "add_basket_element": "id=addToCart",
        "my_basket_element": "id=shoppingCart",
        "submit_basket_items_button": "xpath=//*[@id='short-summary']/div[1]/div[2]/button",
        "submit_delivery_button": "xpath=//*[@id='short-summary']/div[1]/div[2]/button",
    }

    # Buildin Locators
    facile_logo = "id:ZZ_logo"
    facile_spinner = "id: loading"
    facile_first_vai = "css:li.col4 > a"
    personalization_tool_tip = "id: AS_price_cloud"
    facile_offerte_sponsor= "css:div.ZZ_cols_container_skin.nu - style offerta_sponsor"
    # WebDriver Locators
    facile_footer = "ZZ_footer"
    facile_footer_mobile = "ZZ_footer_body"
    facile_first_vai_web = "li.col4 > a"
    facile_position_zero = "ZZ_icon ZZ_icon_fw.ZZ_icon_star"
    facile_sponsor_label = "sponsor-label"

    @keyword
    def switch_test(self):
        """
            Switch workaround
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        time.sleep(1.0)
        driver.switch_to.window(driver.window_handles[-1])
        driver.find_elements(By.CSS_SELECTOR, "abc")

    @keyword
    def wait(self, key_word, args):
        """
            Switch workaround
        """
        BuiltIn().wait_until_keyword_succeeds(30, 2, key_word, args, '200ms')

    @keyword
    def test(name="test"):
        """
            Switch workaround
        """
        logger.info(name)

    @keyword
    def append_to_url(self, string_to_append):
        """
            Switch workaround
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        url = driver.current_url
        url = url + string_to_append
        driver.get(url)

    @keyword
    def i_close_symphony_toolbar(self):
        """
            Switch workaround
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        driver.execute_script("sf-toolbarreset clear-fix")[0].style = "display: none;";

    @keyword
    def i_land_on_facile_home_page(self):
        """
            Switch workaround
        """
        self.wait("element_should_be_visible", self.facile_logo)

    @keyword
    def i_click_on_submenu_label(self, navbar_label, submenu_label):
        """
            Switch workaround
        """

        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        navbar_label = driver.find_element_by_xpath("//*[@id='ZZ_upper_menu']//span[text()={}]".format(navbar_label))
        hover = ActionChains(driver).move_to_element(navbar_label)

        hover.perform()
        label_vertical = driver.find_element_by_xpath("//*[@id='ZZ_upper_menu']//span[text()={}]".format(submenu_label))
        label_vertical.click()

    @keyword
    def i_scroll_to_the_footer(self):
        """
            Switch workaround
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        element = driver.find_element_by_id(self.facile_footer)
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()


    @keyword
    def i_scroll_to_the_footer_mobile(self):
        """
            Switch workaround
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        element = driver.find_element_by_id(self.facile_footer)
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()

    @keyword
    def i_click_first_result_vai_button(self):
        """
            Switch workaround
        """
        self.wait("Element Should Not Be Visible", self.facile_spinner)
        self.wait("Element Should Be Visible", self.facile_logo)

        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        driver.find_element_by_css_selector(self.facile_first_vai_web).click()
        driver.switch_to.window(driver.window_handles[-1])

    @keyword
    def option_is_selected(self, element):
        """
            Switch workaround
        """
        element = element.replace("id:", "")
        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        org = driver.find_element_by_id(element)
        val = org.get_attribute("class")
        BuiltIn().should_contain(val, "checked")

    @keyword
    def option_is_not_selected(self, element):
        """
            Switch workaround
        """
        element = element.replace("id:", "")
        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        org = driver.find_element_by_id(element)
        val = org.get_attribute("class")
        BuiltIn().should_not_contain(val, "checked")

    @keyword
    def i_enter_facile_url(self, start_url):
        """
            Switch workaround
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        driver.get(start_url)

    @keyword
    def i_land_on_the_selected_partner_webpage(self):
        """
            Switch workaround
        """

        BuiltIn().run_keyword("page_should_not_contain", self.facile_logo)

    @keyword
    def personalization_tooltip_is_visible(self):
        """
            Switch workaround
        """
        self.wait("element_should_be_visible", self.personalization_tool_tip)

    @keyword
    def i_close_Personalization_tooltip(self):
        """
            Switch workaround
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        driver.execute_script("document.getElementById('#tooltip-close').click()")

    @keyword
    def personalization_tooltip_is_not_visible(self):
        """
            Switch workaround
        """
        self.wait("element_should_not_be_visible", self.personalization_tool_tip)

    @keyword
    def check_option_value(self, element, expected_value):
        """
            Switch workaround
        """
        element = element.replace("id:", "")
        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        org = driver.find_element_by_id(element)
        value = org.get_attribute("value")
        BuiltIn().should_be_equal(value, expected_value)

    @keyword
    def check_label(self):
        """
            Switch workaround
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        WebDriverWait(driver, 10).until(

            EC.presence_of_element_located((By.CSS_SELECTOR, "{}".format(self.facile_position_zero))))
        element = driver.find_element_by_xpath("*//[@id='AS_price_table_content']/div[1]/h2/text()").text
        assert element.text == 'IN EVIDENZA'

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "{}".format(self.facile_sponsor_label))))

    @keyword
    def i_check_label_is_present_if_posizione_zero_is_set(self):
        """
            Switch workaround
        """
        position_zero = BuiltIn().run_keyword_and_return_status("element_should_be_visible", self.facile_offerte_sponsor)
        BuiltIn().run_keyword_if(position_zero, self.check_label)

    @keyword
    def i_land_on_facile_home_page(self):
        """
            Switch workaround
        """
        self.wait("element_should_be_visible", self.facile_logo)
