import os
import rdflib
import requests

from rdflib.namespace import RDF, FOAF, OWL, RDFS, DCTERMS
from string import Template
from flask import Flask, escape, request, render_template
from markupsafe import Markup

app = Flask(__name__)
app.jinja_options['extensions'].append('jinja2.ext.debug')

@app.route('/')
def index():

	ttlurl = request.args.get('ttlurl', "https://raw.githubusercontent.com/ukparliament/ontologies/master/procedure/procedure-ontology.ttl")

	ppr = rdflib.Namespace("http://parliament.uk/ontologies/procedure/")
	g = rdflib.Graph()
	
	result = g.parse(data=requests.get(ttlurl).text, format="turtle")
	
	
	classes = []

	for s, p, o in g.triples((None, RDF.type, OWL.Class)):
		isSubClass = g.value(s, RDFS.subClassOf)
# 		print(isSubClass)
		
		superclasses = []
		
		superclassobjects = g.objects(s, RDFS.subClassOf)
		for superclassobject in superclassobjects:
			superclasses.append(superclassobject.split('/')[-1])
			
		superclass = ""
		if isSubClass is not None:
			superclass = g.value(s, RDFS.subClassOf).split('/')[-1]			
# 			print(superclass)
		h3id = g.label(s).lower().replace(" ", "-")
#		  classes.append(f'<article class="class"><h3 id="{h3id}">{g.label(s)}</h3> {subClassNote}<p>{g.value(s, RDFS.comment)}</p></article>')
		classes.append({'label':g.label(s), 'comment':g.value(s, RDFS.comment), 'superclass':superclass, 'superclasses':superclasses})
	
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
		namespaces.append(namespace)
	
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
		
	newfoafnames = []
	
	foafmakerids = []
	
	makerobjects = []
	
	for maker in g.objects(s, FOAF.maker):
		foafmakerids.append(maker)
		makerobject = {}
		for s,p,o in g.triples((maker,None,None)):
			makerobject['id'] = str(s)
			makerobject['name'] = str(g.value(s, FOAF.name))
			makerobject['homepage'] = str(g.value(s, FOAF.homepage))
				
			makerobjects.append(makerobject)
			
	makers = []
	for i in makerobjects:
		if i not in makers:
			makers.append(i)

	return render_template('index.html', 
	title=Markup(title),
	created=Markup(created),
	rights=Markup(rights),
	description=Markup(description),
	depiction=Markup(depiction),
	properties=Markup(properties),
	foafnames=Markup(foafnames),
	ttlurl=ttlurl,
	classes=classes,
	namespaces=namespaces,
	makers = makers
	)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)


# data=requests.get(githuburl).text

