from housingDataCollector import housingDataCollector
from DataPreprocessor import DataPreprocessor
import pandas as pd

# the bot should be transformed either into a webserver or a constant loop with multi-threading

class Bot:
    def __init__(self):
        self.__dataCollector = housingDataCollector()


    def start(self):
        self.__dataCollector.saveLinks()
        #self.__dataCollector.readLinks('/Users/eugenganenco/Desktop/srealtyAnalysis/data_11_10_2022_20_22_30.txt')
        df = pd.read_csv('/Users/eugenganenco/Desktop/srealtyAnalysis/housesDf_15_10_2022_21_01_03.csv')
        dataPreProcessor = DataPreprocessor(df)
        dataPreProcessor.findCoordinates()


