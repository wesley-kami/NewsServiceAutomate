import os
import textwrap
from .Data_Call import Data_Call
import smtplib
from email.message import EmailMessage

class MailNews:
    
    def __init__(self):
        # don't create SMTP client at init to allow formatting/debug without network calls
        self.msg = EmailMessage()
        data_call = Data_Call()
        self.data = data_call.treat_all_data()
        self.Mailbody="""
        
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                *{{font-family:'sans-serif';margin:0;padding:0;}}
                .banner{{display:flex; justify-content: center;align-items: center;margin:auto;}}
                
                .banner img{{max-width:350px;}}

                .banner p{{font-size: 3rem;font-style: italic;font-weight: 600;}}

                .meteo{{padding:0.5em 2em 0.5em 0.5em;display:flex;align-items: center;gap:1em;width:fit-content;border:1px solid rgb(255, 255, 255);margin:1em auto 3em auto;border-radius:1em;box-shadow: 8px 8px 25px gray;border:1px solid gray;}}

                .meteo img{{ width:100px; height:70px;border-radius:10vh;object-fit: cover;}}

                .meteo div p{{ color:rgb(95, 95, 95);}}

                .font-sm{{font-size:small;}}

                .font-800{{ font-weight: 800; }}

                .font-light{{font-weight: 100;}}

                .intro{{font-size: 1.5em;height: fit-content;width:90%;margin:auto;}}

                .intro{{line-height: 1.3em;}}

                .actuality-card{{background-color: #313131;width:90%;padding:2em;border-radius: 5px;color:white;margin: 1em auto;}}

                .actuality-card img{{width:100%;margin:auto;}}

                .actuality-card a {{text-decoration: none;background-color: #EE9631;padding:0.5em;font-size: small;border-radius: 3px;font-weight:700;align-content: flex-end;color:white;margin:0.5em 0;transition: background-color 0.3s;}}

                .actuality-card a:hover{{cursor: pointer;background-color: #e7a860;}}

                .actuality-card p{{font-weight:lighter;width:90%;margin:1em 0;font-size:large;}}

                table{{width:80%;margin:1em auto 3em auto;border-collapse: collapse;font-size:medium;}}
                
                table th{{text-align: left;padding:1em;background-color:gray;color:white;}}

                table td{{padding:1em;}}

                .table-coin img{{width:30px;height:30px;}}

                .table-coin p span{{color:#585858;}}

                .table-coin{{display:flex;align-items: center;align-items:center;gap:0.5em;}}
                
            </style>
        </head>
        <body">
            <div class="banner">
                <p>Daily Break News</p>
            </div>

            <div class="meteo">
                <img src="{weatherImage}" alt="">
                <div>
                    <p class="font-sm font-light">Cotonou, Bénin</p>
                        <p class="font-800">{temperature}°C</p>
                    <p class="">{weather}</p>
                </div>
            </div>

            <div class="intro">
                <p>Bonjour à vous cher abonné , ici DAILY BREAK NEWS votre chaine préférée qui vous permet de suivre le fil de  l’actualité au quotiden. </p>
                <p>Voici ici quelques actualités de la journée.</p>
            </div>

            <div class="grid-news">
                {actuality}
            </div>

            <h1 style="text-align:center;font-size:2rem;margin:1em 0;">Info Crypto</h2>

            <table>
            <tr>
                    <th>Monnaie</th>
                    <th>Valeure</th>
            </tr>
            {coins}
            </table>      
            <footer style="text-align:center;font-size:medium;"> © COPYRIGHT Made by WeasleDev </footer>  

        </body>
        </html>
        
        """ 
        
    def formatNews(self):
        infos=""
        news = self.data[1]
        for info in news:
            infos += textwrap.dedent(f"""
            <div class="actuality-card">
                    <img src="{info['image']}" alt="">
                    <h1 style="margin:0;">{info['title']}</h1>
                    <p>{info['description']}</p>
                    <a href="{info['url']}">READ MORE</a>
             </div>
            """)
        return infos
    def formatCoinsInfo(self):
        coinInfos=""
        coins= self.data[2]
        for coin in coins:
            coinInfos+= textwrap.dedent(f"""
            <tr>
                    <td class="table-coin"> 
                        <img src="{coin['image']}" alt="">
                        <p> {coin['monnaie']} <span>{coin['symbol']}</span></p>
                    </td>
                    <td>{round(coin['currency'])} $USD</td>
            </tr>
            """)
        return coinInfos
    def formatMailbody(self):
        weat= self.data[0]
        act = self.formatNews()
        gecko = self.formatCoinsInfo()
        self.Mailbody = self.Mailbody.format(weatherImage=weat['icon'],temperature=weat["temperature"],weather=weat['weather'],actuality=act,coins=gecko)
        # print(self.Mailbody)
    
    def sendMail(self,receiver:str):
        try:
            sender = os.getenv('SMTP_EMAIL')
            Mailpass = os.getenv('SMTP_PASS')
            self.formatMailbody()
            self.msg['to']= receiver
            self.msg['subject']="Your Daily News"
            self.msg['From']= sender
            self.msg.add_alternative(self.Mailbody,subtype="html")
            
            with smtplib.SMTP_SSL("smtp.gmail.com", os.getenv('SMTP_PORT')) as smtp:
                smtp.login(sender, Mailpass)
                print("Login successful. Sending message...")
                smtp.send_message(self.msg)
                print("Email sent successfully!")
            
        except Exception as e:
            print(f"Error occured :{e}")
    
    def sendMailToSubscribers(self):
        try:
            with open("data/userEmail.txt","r") as f:
                users = f.readlines()
                for user in users:
                    user=user.replace('\n',"")
                    self.sendMail(user)
            
        except Exception as e:
            print(f"Error occured while sending email: {e}")