from flask import *
from api.api import api_blueprint
from api.user import user_blueprint
from api.booking import booking_blueprint
from decouple import config
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config['JSON_SORT_KEYS'] = False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.register_blueprint(api_blueprint,url_prefix='/api')
app.register_blueprint(user_blueprint,url_prefix='/api')
app.register_blueprint(booking_blueprint,url_prefix='/api')
app.secret_key=config("secret_key")

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run(host="0.0.0.0",port=3000,debug=False)