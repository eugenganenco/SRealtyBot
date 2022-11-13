from geopy.geocoders import Nominatim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import googletrans
import pandas as pd


class Playground:
    def __init__(self):
        geolocator = Nominatim(user_agent='Srealty')
        location = geolocator.geocode('Teplá - Babice, okres Cheb')
        if not location:
            location = self.__findSimplifiedLocationCoordinates('Teplá - Babice, okres Cheb', geolocator)
        print(location.latitude)

    def __findSimplifiedLocationCoordinates(self, locationString, geolocator):
        if ' ' not in locationString:
            return geolocator.geocode(locationString)
        locationList = locationString.split(' ')
        locationString = " ".join([word for word in locationList[1:] if '-' not in word])
        print(locationString)
        location = geolocator.geocode(locationString)
        if location:
            return location
        else:
            return self.__findSimplifiedLocationCoordinates(locationString, geolocator)
