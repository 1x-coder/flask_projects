from flask import Flask,render_template,request
app=Flask(__name__)


@app.route("/")
@app.route("/form")
def home():
    import requests
    from bs4 import BeautifulSoup

    page=requests.get('https://weather.com/en-IN/weather/today/l/9b6182fe7982a37d6eb65491b0218d1c7e7ee13e0b60e40bfaa9669973e7e933')
    # print(page)
    soup=BeautifulSoup(page.content,'html.parser')
    item1=soup.find('div',class_="_1A9zV")
    new=item1.find('span',class_="_3KcTQ").get_text()
    return render_template('form.html', item=new)

@app.route('/',methods=['POST'])
def getvalue():
    #new code


    import requests, json,config
    # base URL
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    # City Name

    # API key
    API_KEY = config.api_key
    # upadting the URL
    name=request.form['name']
    URL = BASE_URL + "q=" + name + "&appid=" + API_KEY
    # HTTP request
    response = requests.get(URL)
    # checking the status code of the request
    if response.status_code == 200:
    # getting data in the json format
        data = response.json()
        # getting the main dict block
        main = data['main']
        # getting temperature
        temperature = int(main['temp'] - 273)
         # getting the humidity
        humidity = main['humidity']
        # getting the pressure
        pressure = main['pressure']
        # weather report
        report = data['weather']
        #end of new code
        return render_template('home.html', temp=temperature,name=name,humidity=humidity,
        pressure=pressure,weather=report[0]['description'])









 
# @app.route('/',methods=['POST'])
# def getvalue():
#     name=request.form['name']
#     return render_template('home.html', data=name)
#data=new has to be changed    

if __name__=='__main__':
    app.run( debug = True)