from typing import List, Dict, Optional
import time

from selenium_firefox.firefox import Firefox
from kov_utils import kjson

AMAZON_URL = 'https://affiliate-program.amazon.com/'

class AmazonAssociates:
    def __init__(
        self,
        cookies_folder_path: str,
        extensions_folder_path: str,
        cache_path: str,
        host: Optional[str] = None,
        port: Optional[int] = None
    ):
        self.cache_path = cache_path
        self.cache = kjson.load(cache_path, default_value={}, save_if_not_exists=True)
        self.browser = Firefox(cookies_folder_path, extensions_folder_path, host=host, port=port)

        self.browser.get(AMAZON_URL)
        time.sleep(1.5)

        if self.browser.has_cookies_for_current_website():
            self.browser.load_cookies()
            time.sleep(1.5)
            self.browser.driver.refresh()
        else:
            input('Log in then press enter')
            self.browser.get(AMAZON_URL)
            time.sleep(1.5)
            self.browser.save_cookies()
    
    def generate_affiliate_link(self, asin: str) -> Optional[str]:
        if asin in self.cache:
            return self.cache[asin]

        if self.__optionally_load_base_url():
            time.sleep(1.5)

        try:
            asin_box = self.browser.driver.find_element_by_id("ac-quicklink-search-product-field")
            asin_box.click()
            asin_box.send_keys(asin)
            time.sleep(1)

            go_button = self.browser.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div/div/form/div[2]/span/span/span/input")
            go_button.click()
            time.sleep(3.5)

            get_link_button = self.browser.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div/div/div[2]/table/tbody/tr/td[3]/div/span[1]/span/a")
            get_link_button.click()
            time.sleep(3)

            text_only_button = self.browser.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div/div[1]/ul/span[2]/li/a")
            text_only_button.click()
            time.sleep(2)

            affiliate_link_element = self.browser.driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div/a")
            affiliate_link = affiliate_link_element.get_attribute('href')

            if self.__optionally_load_base_url():
                time.sleep(1.5)
            
            self.cache[asin] = affiliate_link
            kjson.save(self.cache_path, self.cache)

            return affiliate_link
        except:
            if self.__optionally_load_base_url():
                time.sleep(1.5)

            return None
    
    def check_analytics(self) -> None:
        self.__optionally_load_base_url()
    
    def quit(self):
        self.browser.driver.quit()
    
    def __optionally_load_base_url(self) -> bool:
        if self.browser.driver.current_url != AMAZON_URL:
            return False

        self.browser.driver.get(AMAZON_URL)

        return True