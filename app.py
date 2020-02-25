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
			subclassstub = g.value(s, RDFS.subClassOf).split('/')[-1]
			subClassNote = f"<p>{g.label(s)} (subclass) &larr; {subclassstub} (superclass)</p>"
			
			print(subclassstub)
		h3id = g.label(s).lower().replace(" ", "-")
		classes.append(f'<article class="class"><h3 id="{h3id}">{g.label(s)}</h3> {subClassNote}<p>{g.value(s, RDFS.comment)}</p></article>')

	classes = ''.join(classes)
	
	properties = []

	for s, p, o in g.triples((None, RDF.type, OWL.ObjectProperty)):
		h3id = g.label(s).lower().replace(" ", "-")
		domainstub = g.value(s, RDFS.domain).split('/')[-1]
		rangestub = g.value(s, RDFS.range).split('/')[-1]
		# rangestub = g.value(s, RDFS.range).n3(g.namespace_manager)

		properties.append(
			f'<article class="property"><h3 id="{h3id}">{g.label(s)}</h3><p>{domainstub} (domain) &rarr; {g.label(s)} (property) &rarr; {rangestub} (range)</p><p>{g.value(s, RDFS.comment)}</p></article>')

	properties = ''.join(properties)
	
	namespaces = []

	for namespace in g.namespaces():
		namespaces.append(f'<p class="namespace"><strong>{namespace[0]}</strong> {namespace[1]}</p>')

	namespaces = ''.join(namespaces)
	
	foafnames = []
	
	for foafname in g.objects(None, FOAF.name):
		foafnames.append(f'<li class="name">{foafname}</li>')
		
	foafnames = ''.join(foafnames)

	for s, p, o in g.triples((None, RDF.type, OWL.Ontology)):
		title = g.value(s, DCTERMS.title)
		description = g.value(s, DCTERMS.description)
		created = g.value(s, DCTERMS.created)
		rights = g.value(s, DCTERMS.rights)
		depiction = g.value(s, FOAF.depiction) or "" # check
		# makers = g.value(s, FOAF.maker) or "" # check
		
		
	for maker in g.objects(s, FOAF.maker):
		for s,p,o in g.triples((maker,None,None)):
			print(s,p,o)
	
# 	for foafhomepage in g.objects(None, FOAF.homepage):
# 		print(foafhomepage)
	
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

