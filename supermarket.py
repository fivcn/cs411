import requests
from xml.etree import ElementTree as ET

url = 'http://www.SupermarketAPI.com/api.asmx/StoresByCityState?APIKEY='
API = '&d8b357715b'
param1 = '&SelectedCity=Long%20Beach'
param2 = '&SelectedState=CA'



url2 = url + API + param1 + param2

response = requests.get(url2)

root = ET.parse(urllib.request.urlopen(url2)).getroot()

for item in root.findall('{http://www.SupermarketAPI.com}ArrayOfStore'):
    print(item)
    storeName = item.get('Storename').text
    storeId = item.get('StoreId').text
    print (storeName, storeId)
