import openai
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app)
openai.api_key = "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"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    password = db.Column(db.String(100))

    def __init__(self, name, password):
        self.name = name
        self.password = password

class AuthSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'password')

article_schema = AuthSchema()
articles_schema = AuthSchema(many=True)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    return response

@app.route('/chatgpt', methods=['POST'])
def chat():
    message = request.json['message']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": message},
            {"role": "user", "content": ""}
        ],
        max_tokens=50,
        temperature=0.7,
        n=1
    )
    generated_text = response.choices[0].message.content.strip()
    return jsonify({'res': generated_text})

@app.route('/pharmacie', methods=['POST'])
def chat1():
    x = request.json['x']
    y = request.json['y']
    url = "https://lematin.ma/pharmacie-garde-casablanca/" + x+ "/" + y + ".html"
    page_to_scrape = requests.get(url)  
    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
    pharmacies = soup.findAll('div', attrs={'class': 'pharmacie'})
    tex=""
    if len(pharmacies) > 0:
        for pharmacy in pharmacies:
            pharmacy_text = pharmacy.text.strip()
            if "Voir la position" in pharmacy_text:
                pharmacy_text = pharmacy_text.replace("Voir la position", "")
            tex=pharmacy_text+"\n "+tex

                 
        return jsonify({'res': tex}) 
    else:
        return jsonify({'res': 'Aucun résultat trouvé pour cette sélection'})



@app.route('/meteo', methods=['POST'])
def chat2():
    tex = ""
    page_to_scrape = requests.get("http://www.meteomaroc.com/meteo/casablanca")
    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
    dates = soup.findAll('label', attrs={'class': 'time-small'})
    temperature = soup.findAll('label', attrs={'class': 'observation_c-small'})
    rain1 = soup.findAll('li', attrs={'class': 'precipmm-0'})
    
    for i, (date, temp, rai) in enumerate(zip(dates, temperature, rain1)):
        if i >= 8:
            tex += f"{date.text.strip()} - température entre: {temp.text.strip()}- précipitations:{rai.text.strip()}\n"
                                                                  
    return jsonify({'res': tex})


@app.route('/login', methods=['POST'])
def login():
    email = request.json['name']
    password = request.json['password']
    
    article = Auth.query.filter_by(name=email, password=password).first()
    if article:
        return jsonify({'status': 'success', 'id': article.id, 'name': article.name})
    else:
        return jsonify({'status': 'refuse'})


if __name__ == "__main__":
    app.run(host='192.168.11.103', port=3000, debug=True)
