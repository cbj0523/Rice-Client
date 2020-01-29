# -*- coding:UTF-8 -*-

from flask import Flask, request
from flask_cors import CORS, cross_origin
import get_meal
import json


app = Flask(__name__)
CORS(app)

@app.route('/')
def mealapi():
    edu = request.args.get("office_of_education")
    sc = request.args.get("school_code")
    stc = request.args.get("school_type_code")
    year = request.args.get("year")
    month = request.args.get("month")
    date = request.args.get("date")
    res = get_meal.get_meal(edu, sc, stc, date, month, year)
    res = json.dumps(res, ensure_ascii=False).encode('utf8')
    return res
