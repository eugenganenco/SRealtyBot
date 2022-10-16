from geopy.geocoders import Nominatim

class DataPreprocessor:
    def __init__(self, dataFrame):
        self.__df = dataFrame

    def findCoordinates(self):
        self.__df['locationLat'] = ""
        self.__df['locationLong'] = ""
        self.__df['locationAddress'] = ""
        geolocator = Nominatim(user_agent='Srealty')
        for index in self.__df.index:
            try:
                location = geolocator.geocode(self.__df['location'][index])
                self.__df.loc[index, 'locationLat'] = location.latitude
                self.__df.loc[index, 'locationLong'] = location.longitude
                self.__df.loc[index, 'locationAddress'] = location.address
            except:
                self.__df.loc[index, 'locationLat'] = ""
                self.__df.loc[index, 'locationLong'] = ""
                self.__df.loc[index, 'locationAddress'] = ""
        self.__df.to_csv('test.csv')


        # either go thorught thel list and find a mapping
        # or work with postal code - does not seem to be feasable and precise
        # do automatic search in google maps - fuck that
        # do search through the site itself -
        # compute the
