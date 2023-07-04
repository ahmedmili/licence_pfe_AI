from flask import Flask ,request, jsonify
# from flask_restful import Api, Resource
import pickle
import pandas as pd

from neo4j import GraphDatabase
import json

app=Flask(__name__)

# neo4j_uri = "bolt://localhost:7687"  # Replace with your Neo4j URI
# neo4j_username = "neo4j"  # Replace with your Neo4j username
# neo4j_password = "123456789"  # Replace with your Neo4j password

# driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))

def get_neo4j_driver():
    uri = "bolt://localhost:7687"  # Update with your Neo4j URI
    username = "neo4j"  # Update with your Neo4j username
    password = "123456789"  # Update with your Neo4j password

    return GraphDatabase.driver(uri, auth=(username, password))

def serialize_node(node):
    serialized = {
        'id': node["id"],
        # 'id': node.id,
        # 'labels': list(node.labels),
        # 'properties': dict(node)
    }
    return serialized

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
      
        "recommended_partner_names" :recommended_partner_names
    }
    return jsonify(data)


@app.route("/api/GrapData/<typee>")    
def recommendFromGraph(typee):

    with get_neo4j_driver().session() as session:
        result = session.run("MATCH (u:User{sexe: $typee})-[r]->(c:Order)<-[d *1]-(b:Box) RETURN b.id as id", typee=typee)
       
        nodes = [serialize_node(record) for record in result]
    # return jsonify(nodes)
    return jsonify(nodes)

if (__name__ == "__main__"):
    app.run(debug=True)


