from flask import *
from currency_api import *
from data_process import *
from auth import *
from datetime import timedelta
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

app = Flask(__name__)
app.secret_key = "123abcxyz_testsecretkey"
app.permanent_session_lifetime = timedelta(minutes = 30)    

def insert_currency_data(token, pair, price, time, date):
    payload = decode_token(token)
    if "message" in payload:
        return payload
    
    email = payload["email"]

    insert_data = {
        "email": email,
        "pair": pair,
        "price": price,
        "time": time,
        "date": date
    }

    result = supabase.table("currency_data").insert(insert_data).execute()
    return result

@app.route("/")
def on_start():
    return redirect("/search")

@app.route("/search", methods = ["GET", "POST"])
def search():
    if "token" not in session:
        return redirect("/login")
    
    payload = decode_token(session["token"])
    if "message" in payload:
        return redirect("/login")

    if request.method == "POST":
        symbol = request.form["symbol_name"]
        base = request.form["base_name"]
        
        result = get_result(base, symbol)
        data = get_currency_data(result)
        insert_currency_data(session["token"], data["curr_pairs"], data["curr_prices"], data["time"], data["date"])
        return render_template("result.html", **data)
    
    return render_template("search.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        sign_up(username, email, password)

        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        result = sign_in(email, password)

        session["token"] = result["token"]

        return redirect("/search")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("token", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug = True)