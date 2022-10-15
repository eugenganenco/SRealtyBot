'''
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By




class DataCollector:
    def __init__(self):
        self._PATH = '/Users/eugenganenco/Documents/drivers/chromedriver'
        self._EMAIL = 'ganeugen@gmail.com'
        self._PASSWORD = 'Digol777'
        self._driver = webdriver.Chrome(self._PATH)
        self.__linksSet = set()
        self._file = self._createFileForData('links')





    def login(self):
        self._driver.get(
            'https://login.szn.cz/?service=sauto&return_url=https%3A%2F%2Fwww.sauto.cz%2Finzerce%2Fosobni')
        loginUsername = self._driver.find_element(By.ID, 'login-username')
        loginUsername.send_keys(self._EMAIL)
        loginPassword = self._driver.find_element(By.ID, 'login-password')
        loginPassword.send_keys(self._PASSWORD)
        loginPassword.send_keys(Keys.RETURN)
        time_.sleep(5)

    def collectData(self):

        while (len(self._driver.find_elements(By.CLASS_NAME, 'c-paging__btn-next')) != 0):
            carElements = self._driver.find_elements(By.CLASS_NAME, 'c-item__link')
            for element in carElements:
                link = element.get_attribute("href")
                self._file.write(link + '\n')
                self.__linksSet.add(link)

            self._driver.find_element(By.CLASS_NAME, 'c-paging__btn-next').click()
            while (len(self._driver.find_elements(By.CLASS_NAME, 'c-paging__btn-next')) == 0
                   or len(self._driver.find_elements(By.CLASS_NAME, 'c-paging__btn-prev')) == 0):
                time_.sleep(0.5)

        print(self.__linksSet)
        self._file.close()
        self._driver.quit()

    def _createFileForData(self, type):
        now = datetime.now()
        dateString = now.strftime("%d_%m_%Y_%H_%M_%S")
        name = "data" + type + "_{}.txt".format(dateString)
        file = open(name, "w")
        return file

    def __fileClose(self):
        self._file.close() '''