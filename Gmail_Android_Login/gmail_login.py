import os
import unittest
from appium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException

# "Virtual Device: Pixel XL API 28, Android 9.0, x86"
# "Requires Appium Server and Android Emulator (Android Studio) to be running"
# "Place email as first line of IDpassword.txt, and password as second line"
 
class GmailAndroidTests(unittest.TestCase):
    "Class to run tests against the Gmail Android app"
    def setUp(self):
        "Setup for the test"
        desired_caps = {}
        desired_caps['platformName'] = "Android"
        desired_caps['platformVersion'] = "9"
        desired_caps['deviceName'] = "Android Emulator"
        desired_caps['appPackage'] = "com.google.android.gm"
        desired_caps['appActivity'] = "com.google.android.gm.ui.MailActivityGmail"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
 
    def tearDown(self):
        "Tear down the test"
        self.driver.quit()
 
    def test_login(self):

        login_file = open("IDpassword.txt", "r")
        email_id_password = login_file.readlines()
        email_id = email_id_password[0]
        password = email_id_password[1]
        element_id = ""
        try:
            # self.driver.implicitly_wait(5)

            # element_id = "com.google.android.gm:id/welcome_tour_skip"
            # element = self.driver.find_element_by_id(element_id)
            # if len(element) > 0:
            #     element.click()
            # else:

            self.driver.implicitly_wait(90)
            element_id = "com.google.android.gm:id/welcome_tour_got_it"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            element_id = "com.google.android.gm:id/setup_addresses_add_another"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            element_id = "com.google.android.gm:id/account_setup_item"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            element_id = "identifierId"
            element = self.driver.find_element_by_id(element_id)
            element.click()
            element.send_keys(email_id)
            
            # element_id = "identifierNext"
            # element = self.driver.find_element_by_id(element_id)
            # element.click()

            element_id = "password"
            element = self.driver.find_element_by_id(element_id)
            element.click()
            element.send_keys(password)

            element_id = "passwordNext"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            # elements = self.driver.find_elements_by_class_name("android:id/button1")
            # for element in elements:
            #     if element.text == "Skip":
            #         element.click()

            element_id = "signinconsentNext"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            element_id = "com.google.android.gms:id/next_button"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            element_id = "com.google.android.gms:id/next_button"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            element_id = "com.google.android.gm:id/account_address"
            element = self.driver.find_element_by_id(element_id)

            element_id = "com.google.android.gm:id/action_done"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            element_id = "com.google.android.gm:id/folder_textView"
            element = self.driver.find_element_by_id(element_id)

            login_file.close()

            sleep(1)

        except NoSuchElementException:
            login_file.close()
            print("NoSuchElementException: Could not find element ID: " + element_id)
            raise NoSuchElementException("NoSuchElementException: Could not find element ID: " + element_id)

    def test_logout(self):

        element_id = ""
        try:
            self.driver.implicitly_wait(60)

            element_id = "com.google.android.gm:id/welcome_tour_got_it"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            element_id = "com.google.android.gm:id/account_address"
            element = self.driver.find_element_by_id(element_id)

            element_id = "com.google.android.gm:id/action_done"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            element_id = "Open navigation drawer"
            element = self.driver.find_element_by_accessibility_id(element_id)
            element.click()

            element_id = "com.google.android.gm:id/account_list_button"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            element_id = "com.google.android.gm:id/manage_accounts_text"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            element_id = "com.android.settings:id/icon_frame"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            element_id = "com.android.settings:id/button"
            element = self.driver.find_element_by_id(element_id)
            element.click()

            element_id = "android:id/button1"
            element = self.driver.find_element_by_id(element_id)
            element.click()

        except NoSuchElementException:
            print("NoSuchElementException: Could not find element ID: " + element_id)
            raise NoSuchElementException("NoSuchElementException: Could not find element ID: " + element_id)
 
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GmailAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)