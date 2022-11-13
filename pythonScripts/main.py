from Bot import Bot
from Playground import  Playground
from URL_helper import URL_helper
if __name__ == '__main__':
    '''
    with open('/Users/eugenganenco/Desktop/srealtyAnalysis/links_23_10_2022_03_45_00.txt', mode="r") as file:
        f = file.readlines()
        print(len(f))
        '''
    #Playground()
    #bot = Bot()
    #bot.start()
    urlHelper = URL_helper()
    print(urlHelper.getLocations())