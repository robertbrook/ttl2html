import os
import rdflib
import requests
from rdflib.namespace import RDF, FOAF, OWL, RDFS, DCTERMS
from string import Template
from flask import Flask, escape, request, render_template
app = Flask(__name__)

@app.route("/")
@app.route('/fromurl/<ttlurl>')
def hello(ttlurl=None):
    return render_template('ttl.html', ttlurl=ttlurl, title="title",
    description="description",
    classes="classes",
    properties="properties",
    namespaces="namespaces",
    makers="makers")

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)


# data=requests.get(githuburl).text

