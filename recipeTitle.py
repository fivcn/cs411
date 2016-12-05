import urllib.request
import json
import auth
import app


def recipeTitleIm (searchentry):
    item = searchentry
    url = 'http://food2fork.com/api/search?key='
    param = '&q='
    API = auth.F2F_API
    url2 = url + API + param+item
    response = urllib.request.urlopen(url2).read().decode("utf-8")
    r = json.loads(response)

#print (json.dumps(r, indent=4, sort_keys=True))

    dataset = []    

    try:
        recipeTitles= [i["title"]for i in r["recipes"]]
        recipeImages = [i["image_url"] for i in r["recipes"]]
        dataset = zip(recipeTitles, recipeImages)
 #   dataset = [j for i in zip(recipeTitles,recipeImages) for j in i]
       
    except KeyError:
        print()

    return dataset

