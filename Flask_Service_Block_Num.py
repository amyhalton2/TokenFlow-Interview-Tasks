import requests
import pandas as pd
from flask import Flask,render_template,request,url_for,redirect


#Create Flask Service
app = Flask(__name__)

 
@app.route("/enterblocknum", methods = ["POST", "GET"])
def data():
	if request.method == "POST":
		BN = request.form["num"]
		return redirect(url_for("BN", BlockNum=hex(int(BN))))
	else:
		return render_template('form.html')

@app.route("/<BlockNum>")
def BN(BlockNum):
	url = "https://eth-mainnet.g.alchemy.com/v2/BdhXlgWaNY1OGWDEYR0oTpVRv4w4qLI2"
	payload = {
		"id": 1,
		"jsonrpc": "2.0",
		"method": "eth_getBlockByNumber",
		"params": [BlockNum, True]
	}
	headers = {
		"accept": "application/json",
		"content-type": "application/json"
	}

	response = requests.post(url, json=payload, headers=headers)
	if response.status_code == 200:
		json = response.json()
		block_info = {'Gas Limit':int(json['result']['gasLimit'],base = 16), 'Gas Used': int(json['result']['gasUsed'],base = 16),\
'Number':int(json['result']['number'],base = 16),'Difficulty':int(json['result']['difficulty'],base = 16), 'Total Difficulty':int(json['result']['totalDifficulty'],base = 16)}
		return render_template('data.html', block_info = block_info)
	else:
		return f"<h1>Status Code: {response.status_code}</h1>"


app.run(debug = True)