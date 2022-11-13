class URL_helper:
    def __init__(self):
        self.__HOUSE_TYPES_LIST = ['rodinne-domy', 'vily', 'chalupy', 'chaty', 'projekty-na-klic', 'zemedelske-usedlosti',
                                        'pamatky-jine', 'vicegeneracni-domy']
        self.__HOUSE_LOCATIONS_DICT = {'Karlovarsky': ['cheb', 'karlovy-vary','sokolov'],
                                       'Plzensky': ['tachov', 'rokycany', 'plzen-sever', 'plzen', 'plzen-jih', 'klatovy', 'domazlice'],
                                       'Ustecky': ['usti-nad-labem', 'teplice', 'most', 'louny', 'litomerice', 'decin', 'chomutov'],
                                       'Stredocesky': ['benesov', 'beroun', 'kladno', 'kolin', 'kutna-hora', 'melnik', 'mlada-boleslav', 'nymburk', 'praha-vychod', 'praha-zapad', 'pribram', 'rakovnik'],
                                       'Praha': ['praha-1', 'praha-2', 'praha-3', 'praha-4', 'praha-5', 'praha-6', 'praha-7', 'praha-8', 'praha-9', 'praha-10'],
                                       'Jihocesky': ['ceske-budejovice', 'cesky-krumlov', 'jindrichuv-hradec', 'pisek', 'prachatice', 'strakonice', 'tabor'],
                                       'Vysocine': ['havlickuv-brod', 'jihlava', 'pelhrimov', 'trebic', 'zdar-nad-sazavou'],
                                       'Pardubicky': ['chrudim', 'pardubice', 'svitavy', 'usti-nad-orlici'],
                                       'Kralovehradecky': ['hradec-kralove', 'jicin', 'nachod', 'rychnov-nad-kneznou', 'trutnov'],
                                       'Liberecky': ['ceska-lipa', 'jablonec-nad-nisou', 'liberec', 'semily'],
                                       'Jihomoravsky': ['blansko', 'breclav', 'brno', 'brno-venkov', 'hodonin', 'vyskov', 'znojmo'],
                                       'Olomoucky': ['olomouc', 'prerov', 'jesenik', 'prostejov', 'sumperk'],
                                       'Zlinsky': ['kromeriz', 'uherske-hradiste', 'vsetin', 'zlin'],
                                       'Moravskoslezsky': ['bruntal', 'frydek-mistek', 'karvina', 'novy-jicin', 'opava', 'ostrava']}


    def getHouseTypesList(self):
        return self.__HOUSE_TYPES_LIST

    def getHouseLocationsDict(self):
        return self.__HOUSE_LOCATIONS_DICT

    def getLocationsSet(self):
        regionsSet = set()
        for region in self.__HOUSE_LOCATIONS_DICT:
            if region == 'Praha':
                regionsSet.add('praha')
            else:
                regionsSet = regionsSet.union(set(self.__HOUSE_LOCATIONS_DICT[region]))
        return regionsSet

    # function used to check if the number of regions in the dataset is equal to that in the geojson file.
    def getLen(self):
        return len(self.getLocationsSet())
