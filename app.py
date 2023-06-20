from flask import Flask ,request, jsonify
# from flask_restful import Api, Resource
import pickle
import pandas as pd

import json

app=Flask(__name__)

@app.route("/api/data/<typee>")    
def recommend(typee):
    partner_dict = pickle.load(open('partner_dict.pkl','rb'))
    partners= pd.DataFrame(partner_dict)

    similarity=pickle.load(open('similarity.pkl','rb'))

    index = partners[partners['name'] == typee].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_partner_names = []
    for i in distances[1:11]:
        recommended_partner_names.append(partners.iloc[i[0]]['name'])

    data = {
        # "partners" :partners.to_dict(orient='records'),
        # "index" :partners[partners['name'] == "PIZZA & GO"].to_dict(orient='records'),
        "recommended_partner_names" :recommended_partner_names
    }
    return jsonify(data)


if (__name__ == "__main__"):
    app.run(debug=True)


