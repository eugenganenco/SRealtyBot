from selenium.webdriver import Keys
import time as time_
import pandas as pd
from selenium.webdriver.common.by import By
from DataCollector import DataCollector


class housingDataCollector(DataCollector):
    def __init__(self):
        super().__init__()
        self.__linksSet = set()



    def login(self):
        self._driver.get('https://login.szn.cz/?service=sreality&return_url=https%3A%2F%2Flogin.'
                         'sreality.cz%2FloginDone%3Fservice%3Dsreality%26return_url%3Dhttps%253A%252F%252Fwww.sreality.cz%252F')
        loginUsername = self._driver.find_element(By.ID, 'login-username')
        loginUsername.send_keys(self._EMAIL)
        loginPassword = self._driver.find_element(By.ID, 'login-password')
        loginPassword.send_keys(self._PASSWORD)
        loginPassword.send_keys(Keys.RETURN)
        time_.sleep(5)

    def findHouses(self):
        self._driver.find_element(By.CLASS_NAME,'dir-hp-signpost__item__link').click()
        time_.sleep(3)
        self._driver.find_element(By.CLASS_NAME, 'btn-XL').click()
        time_.sleep(3)

    def collectLinks(self):
        while (len(self._driver.find_elements(By.CSS_SELECTOR, "a.icon-arr-right.disabled"))) == 0:
            houseElements = self._driver.find_elements(By.CSS_SELECTOR, 'a.title')
            for element in houseElements:
                link = element.get_attribute("href")
                self.__linksSet.add(link)
                self._file.write(link + '\n')
            self._driver.find_element(By.CSS_SELECTOR, 'a.icon-arr-right.paging-next').click()
            while (len(self._driver.find_elements(By.CSS_SELECTOR, 'a.btn-paging-pn')) == 0):
                time_.sleep(0.5)
        self._file.close()

    def readLinks(self, fileName):
        df = pd.DataFrame()
        df.to_csv('housesDf.csv')
        file = open(fileName, "r")
        links = file.readlines()
        index = 0
        for link in links:
            dataPoint = self.__readLink(link)
            index = index + 1
            print(dataPoint)
            dfElement = pd.DataFrame([dataPoint])
            dfElement['Index'] = [index]
            dfElement.set_index('Index')
            df = pd.concat([df, dfElement], ignore_index=True)
            df.to_csv('housesDf.csv')
            print("data frame: \n {dfName}".format(dfName=df))

    def __readLink(self, link):
        listingDictionary = {}
        self._driver.get(link)
        time_.sleep(3)
        # location
        listingDictionary['location'] = self._driver.find_element(By.CSS_SELECTOR, 'span.location-text').text
        # list of all the parameters
        parameterElements = self._driver.find_elements(By.CSS_SELECTOR, 'li.param.ng-scope')
        for parameterElement in parameterElements:
            parameterName = parameterElement.find_element(By.CSS_SELECTOR, 'label.param-label').text
            parameterValue = parameterElement.find_element(By.CSS_SELECTOR, 'strong.param-value').text
            if not parameterValue:
                parameterValue = parameterElement.find_element(By.CSS_SELECTOR, 'strong.param-value')
                if (len(parameterValue.find_elements(By.CSS_SELECTOR, 'span.icof.icon-cross')) != 0):
                    parameterValue = '0'
                else:
                    if (len(parameterValue.find_elements(By.CSS_SELECTOR, 'span.icof.icon-ok')) != 0):
                        parameterValue = '1'
            listingDictionary[parameterName[:-1]] = parameterValue
        return listingDictionary

    def stopCollector(self):
        self._driver.quit()









