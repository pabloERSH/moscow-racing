from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService


BROWSER = "Edge"

class TestRegister(LiveServerTestCase):
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

    def setUp(self):
        self.driver.get(f"{self.live_server_url}/users/register/")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def wait(self):
        return WebDriverWait(self.driver, 10)

    def test_valid_register(self):
        driver = self.driver

        username_field = self.wait().until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_username"]')))
        username_field.send_keys("test_user")
        email_field = self.wait().until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_email"]')))
        email_field.send_keys("test_email@ya.com")
        first_name_field = self.wait().until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_first_name"]')))
        first_name_field.send_keys("Ivan")
        last_name_field = self.wait().until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_last_name"]')))
        last_name_field.send_keys("Ivanov")
        password_field = self.wait().until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password"]')))
        password_field.send_keys("12345678")
        password2_field = self.wait().until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password2"]')))
        password2_field.send_keys("12345678")
        self.wait().until(EC.element_to_be_clickable((By.ID, "register_button"))).click()

        welcome_message = self.wait().until(
            EC.presence_of_element_located((By.ID, "welcome_message"))
        ).text
        assert "Вы успешно зарегистрировались!!! Теперь вы можете авторизоваться по ссылке!" in welcome_message

    def test_empty_register(self):
        driver = self.driver

        username_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_username"]')))
        username_field.send_keys("")
        email_field = self.wait().until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_email"]')))
        email_field.send_keys("")
        first_name_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_first_name"]')))
        first_name_field.send_keys("")
        last_name_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_last_name"]')))
        last_name_field.send_keys("")
        password_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password"]')))
        password_field.send_keys("")
        password2_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password2"]')))
        password2_field.send_keys("")
        self.wait().until(EC.element_to_be_clickable((By.ID, "register_button"))).click()

        error_message = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error_id_form_username"]/ul/li'))
        ).text
        assert "Введите логин!" in error_message

        error_message = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error_id_form_email"]/ul/li'))
        ).text
        assert "Введите почту!" in error_message

        error_message = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error_id_form_password"]/ul/li'))
        ).text
        assert "Введите пароль!" in error_message

        error_message = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error_id_form_password2"]/ul/li'))
        ).text
        assert "Повторите пароль!" in error_message

    def test_invalid_email_register(self):
        driver = self.driver

        email_field = self.wait().until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_email"]')))
        email_field.send_keys("test_email")
        self.wait().until(EC.element_to_be_clickable((By.ID, "register_button"))).click()

        error_message = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error_id_form_email"]/ul/li'))
        ).text
        assert "Введите правильный адрес электронной почты." in error_message

    def test_non_matching_pass_register(self):
        driver = self.driver

        password_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password"]')))
        password_field.send_keys("456")
        password2_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password2"]')))
        password2_field.send_keys("123")
        self.wait().until(EC.element_to_be_clickable((By.ID, "register_button"))).click()

        error_message = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error_id_form_password2"]/ul/li'))
        ).text
        assert "Пароли не совпадают!" in error_message


    def test_already_registered_data(self):
        driver = self.driver

        username_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_username"]')))
        username_field.send_keys("test_user")
        email_field = self.wait().until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_email"]')))
        email_field.send_keys("test_email@ya.com")
        first_name_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_first_name"]')))
        first_name_field.send_keys("Ivan")
        last_name_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_last_name"]')))
        last_name_field.send_keys("Ivanov")
        password_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password"]')))
        password_field.send_keys("12345678")
        password2_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password2"]')))
        password2_field.send_keys("12345678")
        self.wait().until(EC.element_to_be_clickable((By.ID, "register_button"))).click()

        self.driver.get(f"{self.live_server_url}/users/register/")

        username_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_username"]')))
        username_field.send_keys("test_user")
        email_field = self.wait().until(EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_email"]')))
        email_field.send_keys("test_email@ya.com")
        self.wait().until(EC.element_to_be_clickable((By.ID, "register_button"))).click()

        error_message = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error_id_form_username"]/ul/li'))
        ).text
        assert "Пользователь с таким именем уже существует." in error_message

        error_message = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error_id_form_email"]/ul/li'))
        ).text
        assert "Аккаунт с таким Email уже существует!" in error_message


class TestLogin(LiveServerTestCase):
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

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def test_valid_login(self):
        driver = self.driver

        username_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_username"]')))
        username_field.send_keys("test_user")
        password_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password"]')))
        password_field.send_keys("12345678")
        self.wait().until(EC.element_to_be_clickable((By.ID, "login_button"))).click()

        link = self.driver.find_element(By.LINK_TEXT, 'Аренда')
        link.click()
        # Ждем, пока не загрузится новая страница
        self.wait().until(
            EC.url_to_be(self.live_server_url + '/rent/')
        )

        # Проверяем, что URL соответствует ожидаемому
        self.assertEqual(self.driver.current_url, self.live_server_url + '/rent/')

        login_username = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login_username"]'))
        ).text
        assert "test_user" in login_username


    def test_invalid_login(self):
        driver = self.driver
        username_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_username"]')))
        username_field.send_keys("test_user_12345678")
        password_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password"]')))
        password_field.send_keys("qwerty")
        self.wait().until(EC.element_to_be_clickable((By.ID, "login_button"))).click()

        error_message = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="non_field_error"]/ul/li'))
        ).text
        assert "Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру." in error_message

    def test_empty_login(self):
        driver = self.driver

        username_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_username"]')))
        username_field.send_keys("")
        password_field = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id_form_password"]')))
        password_field.send_keys("")
        self.wait().until(EC.element_to_be_clickable((By.ID, "login_button"))).click()

        error_message = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error_id_form_username"]/ul/li'))
        ).text
        assert "Введите логин!" in error_message

        error_message = self.wait().until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="error_id_form_password"]/ul/li'))
        ).text
        assert "Введите пароль!" in error_message
