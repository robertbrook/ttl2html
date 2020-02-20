import os
import rdflib
import requests
from rdflib.namespace import RDF, FOAF, OWL, RDFS, DCTERMS
from string import Template
from flask import Flask, escape, request, render_template
app = Flask(__name__)
from markupsafe import Markup

    
@app.route('/')
def index():

	ttlurl = request.args.get('ttlurl', "https://raw.githubusercontent.com/ukparliament/ontologies/master/procedure/procedure-ontology.ttl")
	
	ppr = rdflib.Namespace("http://parliament.uk/ontologies/procedure/")
	g = rdflib.Graph()
	
	result = g.parse(data=requests.get(ttlurl).text, format="turtle")
	
	classes = []

	for s, p, o in g.triples((None, RDF.type, OWL.Class)):
		isSubClass = g.value(s, RDFS.subClassOf)
		subClassNote = ""
		if isSubClass is not None:
			subClassNote = f"<p>This class is a <strong>subclass</strong> of {g.value(s, RDFS.subClassOf)}.</p>"

		classes.append(f'<article><h3>{g.label(s)}</h3> <p>{g.value(s, RDFS.comment)}</p>{subClassNote}</article>')

	classes = ''.join(classes)
	
	return render_template('ttl.html', title="title",
	description="description",
	classes=Markup(classes),
	properties="properties",
	namespaces="namespaces",
	makers="TK makers")

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)


# data=requests.get(githuburl).text

