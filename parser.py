#!/usr/bin/python3

import rdflib
import requests
from rdflib.namespace import RDF, FOAF, OWL, RDFS, DCTERMS
from string import Template

ppr = rdflib.Namespace("http://parliament.uk/ontologies/procedure/")

githuburl = "https://raw.githubusercontent.com/ukparliament/ontologies/master/procedure/procedure-ontology.ttl"

# data=requests.get(githuburl).text

g = rdflib.Graph()
result = g.parse(data=requests.get(githuburl).text, format="turtle")

classes = []

for s, p, o in g.triples((None, RDF.type, OWL.Class)):
    isSubClass = g.value(s, RDFS.subClassOf)
    subClassNote = ""
    if isSubClass is not None:
        subClassNote = f"<p>This class is a <strong>subclass</strong> of {g.value(s, RDFS.subClassOf)}.</p>"

    classes.append(f'<article><h3>{g.label(s)}</h3> <p>{g.value(s, RDFS.comment)}</p>{subClassNote}</article>')

classes = ''.join(classes)

makers = []

for s, p, o in g.triples((None, RDF.type, OWL.Ontology)):
    title = g.value(s, DCTERMS.title)
    description = g.value(s, DCTERMS.description)

makers = ''.join(makers)

properties = []

for s, p, o in g.triples((None, RDF.type, OWL.ObjectProperty)):
    properties.append(
        f'<article><h3>{g.label(s)}</h3> <p>{g.value(s, RDFS.comment)}</p> <p>This object property has the <strong>domain</strong> {g.value(s, RDFS.domain)}</p><p>The object property is in the <strong>range</strong> {g.value(s, RDFS.range)}</p></article>')

properties = ''.join(properties)

namespaces = []

for namespace in g.namespaces():
    namespaces.append(f'<p><strong>{namespace[0]}</strong> {namespace[1]}</p>')

namespaces = ''.join(namespaces)

# https://ukparliament.github.io/ontologies/procedure/procedure-ontology.html

htmlTemplate = Template("""<html>
<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/kognise/water.css@latest/dist/light.min.css">
<title>$title</title>
<style>
article {margin: 2rem auto;}
</style>
</head>
<body>
<header>

<h1 id="title">$title</h1>

<p>$description</p>

$makers
</header>
<main>


<h2 id="classes">Classes</h2>
<hr>
$classes

<h2 id="properties">Object properties</h2>
<hr>
$properties

<h2 id="namespaces">Namespaces</h2>
<hr>
$namespaces

</main>
<footer></footer>
</body>
</html>

""")

output = open('output.html', 'w+')

output.write(htmlTemplate.safe_substitute(
    title=title,
    description=description,
    classes=classes,
    properties=properties,
    namespaces=namespaces,
    makers=makers
))
output.close()