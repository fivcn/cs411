import urllib
import auth
import app
from xml.etree import ElementTree as ET

user_input = input("enter city:    ")
user_state = input("enter state:   ")

city1, city2 = user_input.split()

city = city1+'%20'+city2


def findStores(city,state):
    url = 'http://www.SupermarketAPI.com/api.asmx/StoresByCityState?APIKEY='
    API = auth.Super_API
    param1 = '&SelectedCity='
    param2 = '&SelectedState='
    state = str(state)
    

    url2 = url + API + param1 + city + param2 + state
    root = ET.parse(urllib.urlopen(requestURL)).getroot()
    r = json.loads(response)

    print (json.dumps(r, indent=4, sort_keys=True))

    dataset = []

    try:
        storeID= [i["title"]for i in r["recipes"]]
        recipeImages = [i["image_url"] for i in r["recipes"]]
        dataset = zip(recipeTitles, recipeImages)
 #   dataset = [j for i in zip(recipeTitles,recipeImages) for j in i]
       
    except KeyError:
        print()

    return dataset
    

    


def searchProdName (item):
    url = 'http://www.SupermarketAPI.com/api.asmx/SearchForItem?APIKEY='
    storeID = '&StoreId='
    itemName = '&ItemName='

    
    url2 = url + API + storeID 

    response = urllib.request.urlopen(url2).read().decode("utf-8")
    r = json.loads(response)
    return r
    





#

'''   
url = 'http://food2fork.com/api/get?key='

receipeID = '35120'
url2 = url+API + search + receipeID



    
    storeID = '&StoreId='
    itemName = '&ItemName='
    API = auth.Super_API
    url2 = url+API + storeID + itemName

'''


        


