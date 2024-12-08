from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import Select


BROWSER = "Edge"

class RentFormTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if BROWSER == "Chrome":
            binary_chrome_driver_file = "C:\\Users\\pave1\\Downloads\\chromedriver.exe"
            service = ChromeService(binary_chrome_driver_file)
            cls.driver = webdriver.Chrome(service=service)
        elif BROWSER == "Edge":
            binary_chrome_driver_file = "C:\\Users\\pave1\\Downloads\\msedgedriver.exe"
            service = EdgeService(binary_chrome_driver_file)
            cls.driver = webdriver.Edge(service=service)
        else:
            raise ValueError("Unsupported browser")
        cls.driver.maximize_window()

    def wait(self):
        return WebDriverWait(self.driver, 10)

    def setUp(self):
        self.driver.get(f"{self.live_server_url}/users/register/")
        username_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_username"]')))
        username_field.send_keys("test_user")
        email_field = self.wait().until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_email"]')))
        email_field.send_keys("test_email@ya.com")
        password_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password"]')))
        password_field.send_keys("12345678")
        password2_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password2"]')))
        password2_field.send_keys("12345678")
        self.wait().until(EC.element_to_be_clickable((By.ID, "register_button"))).click()
        self.driver.get(f"{self.live_server_url}/users/login/")
        username_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_username"]')))
        username_field.send_keys("test_user")
        password_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password"]')))
        password_field.send_keys("12345678")
        self.wait().until(EC.element_to_be_clickable((By.ID, "login_button"))).click()
        self.driver.get(f"{self.live_server_url}/rent/")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_valid_rent(self):
        driver = self.driver

        name_field = self.wait().until(EC.presence_of_element_located((By.XPATH, '//input[@id="name"]')))
        name_field.send_keys("Test")
        email_field = self.wait().until(EC.presence_of_element_located((By.XPATH, '//input[@id="email"]')))
        email_field.send_keys("test_email@ya.com")

        select_rent_date = self.wait().until(EC.presence_of_element_located((By.NAME, 'RentDate')))
        select = Select(select_rent_date)
        today = date.today().strftime("%d.%m.%Y")
        select.select_by_value(today)

        select_rent_time = self.wait().until(EC.presence_of_element_located((By.NAME, 'RentTime')))
        select = Select(select_rent_time)
        select.select_by_index(1)

        select_rent_car = self.wait().until(EC.presence_of_element_located((By.NAME, 'Car')))
        select = Select(select_rent_car)
        select.select_by_index(1)

        self.wait().until(EC.element_to_be_clickable((By.ID, "rent-button"))).click()

        message = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rent_success"]'))
        ).text
        assert "Test, вы успешно забронировали трек!" in message

