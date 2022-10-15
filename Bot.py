from housingDataCollector import housingDataCollector


# the bot should be transformed either into a webserver or a constant loop with multi-threading

class Bot:
    def __init__(self):
        self.__dataCollector = housingDataCollector()

    def start(self):
        self.__dataCollector.login()
        self.__dataCollector.findHouses()
        self.__dataCollector.collectLinks()
        self.__dataCollector.readLinks('/Users/eugenganenco/Desktop/srealtyAnalysis/data_11_10_2022_20_22_30.txt')
        self.__dataCollector.stopCollector()



