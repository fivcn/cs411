from flask import Flask, render_template, request
import urllib.request
import json


app = Flask(__name__)

@app.route('/')
def index():
    return "this is the home page"


#@app.route("/recipesearch", methods= ['POST', 'GET'])
#def recipesearch():
 #   return render_template("recipesearch.html")

@app.route("/recipesearch", methods= ['POST', 'GET'])
def home():
    if request.method == 'POST':
        try:
            searchentry = request.form.get('text')
            print("search entry error" + str(searchentry))
            url = 'http://food2fork.com/api/search?key='
            param = '&q='
            API = ''
            url2 = url + API + param+searchentry
            response = urllib.request.urlopen(url2).read().decode("utf-8")
            r = json.loads(response)

            dataset = []    
            try:
                recipeTitles= [i["title"]for i in r["recipes"]]
                recipeImages = [i["image_url"] for i in r["recipes"]]
                dataset = zip(recipeTitles, recipeImages)       
            except KeyError:
                print()

            return render_template("recipesearch.html", dataset = dataset)
        except:
            print("this is an error")
    return render_template("recipesearch.html")

if __name__ == "__main__":
    app.run()
