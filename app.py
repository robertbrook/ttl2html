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
		h3id = g.label(s).lower().replace(" ", "-")
		classes.append(f'<article class="class"><h3 id="{h3id}">{g.label(s)}</h3> <p>{g.value(s, RDFS.comment)}</p>{subClassNote}</article>')

	classes = ''.join(classes)
	
	properties = []

	for s, p, o in g.triples((None, RDF.type, OWL.ObjectProperty)):
		h3id = g.label(s).lower().replace(" ", "-")
		properties.append(
			f'<article class="property"><h3 id="{h3id}">{g.label(s)}</h3> <p>{g.value(s, RDFS.comment)}</p> <p>This object property has the <strong>domain</strong> {g.value(s, RDFS.domain)}</p><p>The object property is in the <strong>range</strong> {g.value(s, RDFS.range)}</p></article>')

	properties = ''.join(properties)
	
	namespaces = []

	for namespace in g.namespaces():
		namespaces.append(f'<p class="namespace"><strong>{namespace[0]}</strong> {namespace[1]}</p>')

	namespaces = ''.join(namespaces)
	
	foafnames = []
	
	for foafname in g.objects(None, FOAF.name):
		print(foafname)
		foafnames.append(f'<p class="">{foafname}</p>')
		
	foafnames = ''.join(foafnames)

	for s, p, o in g.triples((None, RDF.type, OWL.Ontology)):
		title = g.value(s, DCTERMS.title)
		description = g.value(s, DCTERMS.description)
		created = g.value(s, DCTERMS.created)
		rights = g.value(s, DCTERMS.rights)
		depiction = g.value(s, FOAF.depiction) or "" # check
		# makers = g.value(s, FOAF.maker) or "" # check

	
	return render_template('ttl.html', 
	title=Markup(title),
	created=Markup(created),
	rights=Markup(rights),
	description=Markup(description),
	depiction=Markup(depiction),
	classes=Markup(classes),
	properties=Markup(properties),
	namespaces=Markup(namespaces),
	foafnames=Markup(foafnames)
	)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)


# data=requests.get(githuburl).text

