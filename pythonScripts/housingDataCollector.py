import traceback
import selenium.common
import time as time_
import pandas as pd
import logging
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from URL_helper import URL_helper


class housingDataCollector():
    def __init__(self):
        self._PATH = '/Users/eugenganenco/Documents/drivers/chromedriver'
        self._EMAIL = 'ganeugen@gmail.com'
        self._PASSWORD = 'Digol777'
        self.__linksSet = set()
        logging.basicConfig(filename='file.log',
                            format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
        self.url__helper = URL_helper()

    def __login(self, driver):
        driver.get('https://login.szn.cz/?service=sreality&return_url=https%3A%2F%2Flogin.'
                         'sreality.cz%2FloginDone%3Fservice%3Dsreality%26return_url%3Dhttps%253A%252F%252Fwww.sreality.cz%252F')
        loginUsername = driver.find_element(By.ID, 'login-username')
        loginUsername.send_keys(self._EMAIL)
        loginPassword = driver.find_element(By.ID, 'login-password')
        loginPassword.send_keys(self._PASSWORD)
        loginPassword.send_keys(Keys.RETURN)
        time_.sleep(5)

    def __setUp(self, driver):
        driver.find_element(By.CLASS_NAME,'dir-hp-signpost__item__link').click()
        time_.sleep(3)
        driver.find_element(By.CLASS_NAME, 'btn-XL').click()
        time_.sleep(3)
        driver.find_element(By.CSS_SELECTOR,'span.sort.per-page-select.right-arrow').click()
        time_.sleep(3)
        options = driver.find_elements(By.CSS_SELECTOR, 'span.options')
        buttons = options[1].find_elements(By.CSS_SELECTOR, 'button.item.ng-binding')
        buttons[1].click()
        time_.sleep(3)

    def saveLinks(self):
        with webdriver.Chrome(self._PATH) as driver:
            self.__login(driver)
            self.__setUp(driver)
            self.__browse(driver)

    def __browse(self, driver):
        name = self.__makeFileName('links', 'txt')
        with open(name, mode="w") as file:
            locationsDict = self.url__helper.getHouseLocationsDict()
            houseTypesList = self.url__helper.getHouseTypesList()
            for key in locationsDict:
                for location in locationsDict.get(key):
                    for houseType in houseTypesList:
                        driver.get(f'https://www.sreality.cz/hledani/prodej/domy/{houseType}/{location}')
                        self.__collectLinks(driver, file, location, houseType)

    def __collectLinks(self, driver, file, location, buildingType):
        while not driver.find_elements(By.CSS_SELECTOR, 'footer'):
            time_.sleep(0.5)
        houseElements = driver.find_elements(By.CSS_SELECTOR, 'div.property.ng-scope')
        for element in houseElements:
            try:
                elementInfo = element.find_element(By.CSS_SELECTOR, 'a.title')
                link = elementInfo.get_attribute("href")
            except selenium.common.StaleElementReferenceException:
                logging.error('StaleElementReferenceException')
            else:
                try:
                    if not self.__isTip(element):
                        self.__linksSet.add(link)
                        file.write(f'{link}, {location}, {buildingType}\n')
                except selenium.common.StaleElementReferenceException:
                    logging.error('StaleElementReferenceException')
        nextButtonIsActive, nextButton = self.__nextButtonActive(driver)
        if nextButtonIsActive:
            nextButton.click()
            time_.sleep(2)
            self.__collectLinks(driver, file, location, buildingType)

    def __nextButtonActive(self, driver):
        paging = driver.find_elements(By.CSS_SELECTOR, 'ul.paging-full')
        if paging:
            if paging[0].find_elements(By.CSS_SELECTOR, 'a.btn-paging-pn.icof.icon-arr-right.paging-next.disabled'):
                return False, None
            else:
                return True, paging[0].find_element(By.CSS_SELECTOR, 'a.btn-paging-pn.icof.icon-arr-right.paging-next')
        return False, None

    def __isTip(self, element):
        if element.find_elements(By.CSS_SELECTOR, 'span._3K9oup83sXawmTePCMtIUp'):
            return True
        else:
            return False

    '''
    def __collectLinks(self, driver):
        name = self.__makeFileName('links', 'txt')
        with open(name, mode="w") as file:
            while not driver.find_elements(By.CSS_SELECTOR, "a.icon-arr-right.disabled"):
                houseElements = driver.find_elements(By.CSS_SELECTOR, 'a.title')
                for element in houseElements:
                    try:
                        link = element.get_attribute("href")
                    except selenium.common.StaleElementReferenceException:
                        logging.error('StaleElementReferenceException')
                    else:
                        self.__linksSet.add(link)
                        file.write(link + '\n')
                driver.find_element(By.CSS_SELECTOR, 'a.icon-arr-right.paging-next').click()
                # checks if the next page loaded
                while not driver.find_elements(By.CSS_SELECTOR, 'a.btn-paging-pn'):
                    time_.sleep(0.5)
    '''

    def readLinks(self, fileName):
        df = pd.DataFrame()
        csvName = self.__makeFileName('housesDf', 'csv')
        df.to_csv(csvName)
        dataDict = self.__readTextFile(fileName)
        with webdriver.Chrome(self._PATH) as driver:
            self.__login(driver)
            for index, link in enumerate(dataDict):
                try:
                    dataPoint = self.__readLink(link, dataDict, driver)
                except selenium.common.exceptions.NoSuchElementException:
                    logging.error('NoSuchElementException {}'.format(link))
                except Exception:
                    logging.error(traceback.format_exc())
                    time_.sleep(300)
                else:
                    print(dataPoint)
                    dfElement = pd.DataFrame([dataPoint])
                    dfElement['Index'] = [index]
                    dfElement.set_index('Index')
                    df = pd.concat([df, dfElement], ignore_index=True)
                    df.to_csv(csvName)
                    print("data frame: \n {dfName}".format(dfName=df))

    def __readTextFile(self, fileName):
        d = {}
        with open(fileName) as file:
            for line in file:
                line = line.split(', ')
                d[line[0]] = line[1:]
        return d

    def __readLink(self, link, datadict, driver):
        listingDictionary = {}
        driver.get(link)
        while not driver.find_element(By.CSS_SELECTOR, 'li.param.ng-scope'):
            time_.sleep(0.5)
        listingDictionary['link'] = link
        listingDictionary['location'] = driver.find_element(By.CSS_SELECTOR, 'span.location-text').text
        listingDictionary['district'] = datadict[link][0]
        listingDictionary['HouseType'] = datadict[link][1]
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
            distanceString = parameter.find_element(By.CSS_SELECTOR, 'span._156Mz2cYnoShsl5Cid1FT3._2iVzlK9Zg3MpMEOkrQqaoL._1mRLNMhwLQGArIldAHOamF').text
            distancesList.append(int(distanceString[1:-1].split(" ")[0]))
        if not len(distancesList): return 0
        else:
            return sum(distancesList)/len(distancesList)

    def __makeFileName(self, name, extension):
        now = datetime.now()
        dateString = now.strftime("%d_%m_%Y_%H_%M_%S")
        name = "{}_{}.{}".format(name, dateString, extension)
        return name