from flask import Flask, request, render_template
from sqlite3 import connect
import db_init
from utils import pf_calc
from flask_cors import CORS
import time
import os

db_init.initer()
app = Flask(__name__)
app.secret_key = "abc123"
CORS(app)

@app.route("/val", methods=["POST"])
def val():
    if request.get_json() is None:
        resp = dict(request.form)
    else:
        resp = request.get_json()
    for i in resp.keys():
        resp[i] = float(resp[i])
    print(resp)
    resp["RECVTS"] = time.time()
    conn = connect("data.db")
    prev = conn.execute("SELECT * FROM SMETER WHERE SAMPLECOUNT = 50 ORDER BY RECVTS DESC").fetchone()
    resp['SAMPLECOUNT']=50 
    resp = pf_calc(resp, prev)
    conn.execute("INSERT INTO SMETER("+(",".join(list(resp.keys())))+") VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [resp[i] for i in resp.keys()])
    conn.commit()
    conn.close()
    return "200"

@app.route("/table")
def table():
    conn = connect("data.db")
    p = conn.execute("SELECT RECVTS, VOLTAGE, CURRENT, PHASEANGLE, POWERFACTOR, FREQUENCY, POWER, ENERGY, TARIFF FROM SMETER ORDER BY RECVTS DESC").fetchall()
    conn.close()
    return render_template("tableviz.html", p=p)

@app.route("/")
def defaul():
    return render_template("index.html")

@app.route("/vars", methods=["POST"])
def vars():
    conn = connect("data.db")
    p = conn.execute("SELECT * FROM SMETER ORDER BY RECVTS").fetchall()
    conn.close()
    x = dict()
    x["voltage"]=list()
    x["current"]=list()
    try:
        for i in range(max(0, len(p)-100), len(p)):
            x["voltage"].append(p[i][1])
            x["current"].append(p[i][2])
        x["Power Factor"] = p[-1][-5]
        x["Frequency"] = p[-1][-4]
    except:
        pass
    return x

@app.route("/resetdb")
def reset():
    os.remove("data.db")
    db_init.initer()
    return "Database reset!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

