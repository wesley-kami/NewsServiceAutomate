import os
from dotenv import load_dotenv
import requests
import subprocess
from datetime import datetime
import json


load_dotenv()

class Data_Call:
    
    def __init__(self):
        self.date = datetime.now().strftime("%d_%m_%Y")
        
        # API URL Weather Map
        self.weather_url= os.getenv('WEATHER_MAP_URL')
        # API URL NEWS
        self.news_url= os.getenv('NEWS_API_URL')
        # API URL Gecko Coin
        self.gecko_url= os.getenv('GECKO_URL')

    def Has_News_Break(self):
        
        try:
        #execute le script pour savoir si le dossier contenant les infos du jour a déjà été créer
            res = subprocess.run('./src/scripts/load.sh',capture_output=True)
            return res.returncode
        
        except Exception:
            print("script not running")
            
    def checkfile(self,file_path):
    
        r = subprocess.run(['./src/scripts/checkFile.sh', file_path],capture_output=True)
        return r.returncode
    
    def API_Call(self,filename,url):
        
        try:
            # Appel API Weather Map
            r = requests.get(url)
            
            with open(f'data/News_{self.date}/{filename}.json',"w") as f:
                f.write(r.text)
                
            return r.text
                
        except Exception as e:
            print(f"Error in API_Call: {e}")
    
    def weather_data_treatment(self):
        try:
            
            self.API_Call('weather',self.weather_url)
            with open(f"data/News_{self.date}/weather.json","r",encoding='utf-8') as f:
                parse = json.load(f)
                icon=parse["weather"][0]["icon"]
                return {
                    "weather": parse["weather"][0]["description"],
                    "icon": f"https://openweathermap.org/img/wn/{icon}@2x.png",
                    "temperature" : round(parse["main"]["temp"] - 273.15),
                    "country" : "Cotonou, Bénin"
                }
        except Exception as e:
            print(f"Error in weather_data_treatment: {e}")
            
    def news_data_treatment(self):
        try:  
            isfile = self.checkfile(f'data/News_{self.date}/actuality.json')
            if isfile == 1:
                self.API_Call('actuality',self.news_url)
            with open(f"data/News_{self.date}/actuality.json",'r') as f:
                parse = json.load(f)
                news = []
                articles = parse["articles"]
                
                for article in articles:
                    news.append({
                        "title" : article['title'],
                        "description": article['description'],
                        "image": article['image'],
                        "url": article['url']
                    })
                
                return news
                    
        except Exception as e:
            print(f"Error in news_data_treatment: {e}")
    
    def gecko_data_treatment(self):
        try:
            isfile = self.checkfile(f'data/News_{self.date}/coin.json')
            if isfile == 1 :
                self.API_Call('coin',self.gecko_url)
            
            coins = []
            
            with open(f'data/News_{self.date}/coin.json', 'r') as f :
                parse = json.load(f)
                
                
                for coin in parse:
                    coins.append({
                        "monnaie" :coin["name"],
                        'image':coin["image"],
                        'symbol':coin["symbol"].upper(),
                        'currency':coin["current_price"]
                    })
                    
            return coins
                
        
        except Exception as e:
            print(f"Error in gecko_data_treatment: {e}")
    

    def treat_all_data(self):
        self.Has_News_Break()
        return [
            self.weather_data_treatment(),
            self.news_data_treatment(),
            self.gecko_data_treatment()
        ]