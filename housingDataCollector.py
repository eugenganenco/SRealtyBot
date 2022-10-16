from selenium.webdriver import Keys
import time as time_
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime


class housingDataCollector():
    def __init__(self):
        self._PATH = '/Users/eugenganenco/Documents/drivers/chromedriver'
        self._EMAIL = 'ganeugen@gmail.com'
        self._PASSWORD = 'Digol777'
        self.__linksSet = set()

    def __login(self, driver):
        driver.get('https://login.szn.cz/?service=sreality&return_url=https%3A%2F%2Flogin.'
                         'sreality.cz%2FloginDone%3Fservice%3Dsreality%26return_url%3Dhttps%253A%252F%252Fwww.sreality.cz%252F')
        loginUsername = driver.find_element(By.ID, 'login-username')
        loginUsername.send_keys(self._EMAIL)
        loginPassword = driver.find_element(By.ID, 'login-password')
        loginPassword.send_keys(self._PASSWORD)
        loginPassword.send_keys(Keys.RETURN)
        time_.sleep(5)

    def __findHouses(self, driver):
        driver.find_element(By.CLASS_NAME,'dir-hp-signpost__item__link').click()
        time_.sleep(3)
        driver.find_element(By.CLASS_NAME, 'btn-XL').click()
        time_.sleep(3)

    def saveLinks(self):
        with webdriver.Chrome(self._PATH) as driver:
            self.__login(driver)
            self.__findHouses(driver)
            self.collectLinks(driver)

    def collectLinks(self, driver):
        name = self.__makeFileName('links', 'txt')
        with open(name, mode="w") as file:
            while not driver.find_elements(By.CSS_SELECTOR, "a.icon-arr-right.disabled"):
                houseElements = driver.find_elements(By.CSS_SELECTOR, 'a.title')
                for element in houseElements:
                    link = element.get_attribute("href")
                    self.__linksSet.add(link)
                    file.write(link + '\n')
                driver.find_element(By.CSS_SELECTOR, 'a.icon-arr-right.paging-next').click()
                # checks if the next page loaded
                while not driver.find_elements(By.CSS_SELECTOR, 'a.btn-paging-pn'):
                    time_.sleep(0.5)

    def readLinks(self, fileName):
        df = pd.DataFrame()
        csvName = self.__makeFileName('housesDf', 'csv')
        df.to_csv(csvName)
        with open(fileName, mode="r") as file:
            links = file.readlines()
        with webdriver.Chrome(self._PATH) as driver:
            self.__login(driver)
            for index, link in enumerate(links):
                dataPoint = self.__readLink(link, driver)
                print(dataPoint)
                dfElement = pd.DataFrame([dataPoint])
                dfElement['Index'] = [index]
                dfElement.set_index('Index')
                df = pd.concat([df, dfElement], ignore_index=True)
                df.to_csv(csvName)
                print("data frame: \n {dfName}".format(dfName=df))

    def __readLink(self, link, driver):
        listingDictionary = {}
        driver.get(link)
        while not driver.find_element(By.CSS_SELECTOR, 'li.param.ng-scope'):
            time_.sleep(0.5)
        # location
        listingDictionary['location'] = driver.find_element(By.CSS_SELECTOR, 'span.location-text').text
        # list of all the parameters
        parameterElements = driver.find_elements(By.CSS_SELECTOR, 'li.param.ng-scope')
        for parameterElement in parameterElements:
            parameterName = parameterElement.find_element(By.CSS_SELECTOR, 'label.param-label').text
            parameterValue = parameterElement.find_element(By.CSS_SELECTOR, 'strong.param-value').text
            if not parameterValue:
                parameterValue = parameterElement.find_element(By.CSS_SELECTOR, 'strong.param-value')
                if parameterValue.find_elements(By.CSS_SELECTOR, 'span.icof.icon-cross'):
                    parameterValue = '0'
                else:
                    if parameterValue.find_elements(By.CSS_SELECTOR, 'span.icof.icon-ok'):
                        parameterValue = '1'
            listingDictionary[parameterName[:-1]] = parameterValue
        companyName = driver.find_element(By.CSS_SELECTOR, 'li.line.name.ng-binding').text
        listingDictionary['companyName'] = companyName
        listingDictionary['proximityIndex'] = self.__createProximityIndex(driver)
        return listingDictionary

    def __createProximityIndex(self, driver):
        distancesList = []
        parameterElements = driver.find_elements(By.CSS_SELECTOR, 'li._2Yo8Fr1pl-AcHF6yvNuKEU')
        for parameter in parameterElements:
            try:
                distanceString = parameter.find_element(By.CSS_SELECTOR, 'span._156Mz2cYnoShsl5Cid1FT3._2iVzlK9Zg3MpMEOkrQqaoL._1mRLNMhwLQGArIldAHOamF').text
                distancesList.append(int(distanceString[1:-1].split(" ")[0]))
            except: # Develop this when you're done !!!!!!!!!!!!!!!
                pass
        return sum(distancesList)/len(distancesList)

    def __makeFileName(self, name, extension):
        now = datetime.now()
        dateString = now.strftime("%d_%m_%Y_%H_%M_%S")
        name = "{}_{}.{}".format(name, dateString, extension)
        return name







