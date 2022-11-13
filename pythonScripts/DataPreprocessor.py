from geopy.geocoders import Nominatim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import googletrans
import pandas as pd


class DataPreprocessor:
    def __init__(self, dataFrame):
        self.__df = dataFrame

    def setUpData(self):
        #self.translateColumns()
        #self.findCoordinates()
        self.findPrice()

    def translateColumns(self):
        translator = googletrans.Translator()
        self.__df.columns = [translator.translate(colName).text for colName in self.__df.columns]
        self.__df.to_csv('test_translated.csv')
        self.__df = pd.read_csv('/Users/eugenganenco/Desktop/srealtyAnalysis/dataWithCoordTranslated.csv')

    # look at the distribution of coordinates and try to identify any ouutliers
    def findCoordinates(self):
        self.__df['locationLat'] = ""
        self.__df['locationLong'] = ""
        geolocator = Nominatim(user_agent='Srealty')
        for index in self.__df.index:
            try:
                location = geolocator.geocode(self.__df['location'][index])
                if not location:
                    location = self.__findSimplifiedLocationCoordinates(self.__df['location'][index], geolocator)
                self.__df.loc[index, 'locationLat'] = location.latitude
                self.__df.loc[index, 'locationLong'] = location.longitude
            except:
                self.__df.loc[index, 'locationLat'] = "Unknown"
                self.__df.loc[index, 'locationLong'] = "Unknown"
        self.__df.to_csv('dataWithCoordTranslated.csv')

    def findPrice(self):
        self.__df = pd.read_csv('/Users/eugenganenco/Desktop/srealtyAnalysis/DataWithCoordPrice.csv')
        self.__df['price'] = ""
        self.__df['total price'] = self.__df['total price'].fillna(self.__df['Discounted'])
        for index in self.__df.index:
            try:
                self.__df.loc[index, 'price'] = self.extractPrice(self.__df.loc[index, 'total price'])
            except TypeError:
                self.__df.loc[index, 'price'] = 0
        self.__df.to_csv('DataWithCoordPrice.csv')

    def extractPrice(self, priceString):
        charArray = []
        for c in priceString:
            if c == '(':
                break
            if c.isdigit():
                charArray.append(c)
        if charArray:
            return int(''.join(charArray))
        else:
            return 0

    def __findSimplifiedLocationCoordinates(self, locationString, geolocator):
        if ' ' not in locationString:
            return geolocator.geocode(locationString)
        locationList = locationString.split(' ')
        locationString = " ".join([word for word in locationList[1:] if '-' not in word])
        location = geolocator.geocode(locationString)
        if location:
            return location
        else:
            return self.__findSimplifiedLocationCoordinates(locationString, geolocator)

    def divideData(self):
        y = self.__df['price']
        X = self.__df.drop(['price'], axis=1)
        SEED = 10
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=SEED)
        # try minMaxScaler later
        scaler = StandardScaler()
        # Fit only on X_train in order to avoid data leakage
        scaler.fit(X_train)

        # Scale both X_train and X_test
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        # DO dimensionality reduction with SVD AND FEATURE SELECTION

        # Create the model
        # Limit the number of features. Do feature selection
        regressor = KNeighborsRegressor(n_neighbors=5)
        regressor.fit(X_train, y_train)
        y_pred = regressor.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred, squared=False)

        print(f'mae: {mae}')
        print(f'mse: {mse}')
        print(f'rmse: {rmse}')

        print(f'R: {regressor.score(X_test, y_test)}')

        # either go thought then list and find a mapping
        # or work with postal code - does not seem to be feasible and precise
        # do search through the site itself -
