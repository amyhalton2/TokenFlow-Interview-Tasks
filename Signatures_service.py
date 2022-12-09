import requests
import pandas as pd
from flask import Flask,render_template,request,url_for,redirect
from flask_paginate import Pagination
from flask import json,jsonify


#Create Flask Service
app = Flask(__name__)


@app.route("/signatures/")
def Sig():
	page = request.args.get("page", 1, type=int)
	per_page = request.args.get("per-page", 10, type=int)
	
	url = "https://www.4byte.directory/api/v1/signatures/?format=json"
	params = {
		"hex_signature": request.args.get("hex"),
	}

	response = requests.get(url, params=params)
	json = response.json()
	df = pd.DataFrame(json['results'])
	text_signatures =  df.text_signature.tolist()

	start = per_page*(page - 1)
	if start+per_page>len(text_signatures):
		end = len(text_signatures)
	else:
		end = start+per_page

	paginated_signatures = text_signatures[start:end]

	results = {
	"results": [
		{"data": [
			{"Name": item}
		],
		"page": page, 
		"is_last_page": end >= len(text_signatures),
		} for item in paginated_signatures
		]
    	}
	return jsonify(results)



app.run(debug = True)