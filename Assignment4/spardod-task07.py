# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/FacultadInformatica-LinkedData/Curso2021-2022/blob/master/Assignment4/course_materials/notebooks/Task07.ipynb

**Task 07: Querying RDF(s)**
"""

!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

print("RDFlib:")
ns = Namespace("http://somewhere#")
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print(s, "subclass of Person")
  for s1, p1, o1 in g.triples((None, RDFS.subClassOf, s)):
    print(s1, "subclass of", s, "and Person")

print("SPARQL:")
from rdflib.plugins.sparql import prepareQuery
q1 = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Subject(rdfs:subClassOf/rdfs:subClassOf*) ns:Person
    }
    ''',
    initNs = {"rdfs": RDFS,"ns": ns}
)

for r in g.query(q1):
  print(r)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

print("RDFlib:")
ns = Namespace("http://somewhere#")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  print(s, "type Person")
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s1, p1, o1 in g.triples((None, RDF.type, s)):
      print(s1, "subclass of", s, "and type Person")

print("SPARQL:")
from rdflib.plugins.sparql import prepareQuery
q1 = prepareQuery('''
  SELECT DISTINCT ?Subject WHERE {
    {?Subject rdf:type ns:Person} UNION
      {
        ?s2(rdfs:subClassOf/rdfs:subClassOf*) ns:Person .
        ?t rdf:type ?s2
      }
    }
    ''',
    initNs = {"rdfs": RDFS,"ns": ns,"rdf": RDF}
)

for r in g.query(q1):
  print(r)

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

print("RDFlib:")
ns = Namespace("http://somewhere#")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  for s1, p1, o1 in g.triples((s, None, None)):
    print(s1, p1, o1)
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s1, p1, o1 in g.triples((None, RDF.type, s)):
      for s2, p2, o2 in g.triples((s1, None, None)):
        print(s2, p2, o2)

print("SPARQL:")
from rdflib.plugins.sparql import prepareQuery
q1 = prepareQuery('''
  SELECT DISTINCT ?Subject ?p ?o WHERE {
    {?Subject rdf:type ?s2 .
    ?s2 (rdfs:subClassOf/rdfs:subClassOf*) ns:Person .
    ?Subject ?p ?o
    } UNION 
      {
        ?s rdf:type ns:Person .
        ?Subject ?p ?o
      }
    }
    ''',
    initNs = {"rdfs": RDFS,"ns": ns,"rdf": RDF}
)

for r in g.query(q1):
  print(r)