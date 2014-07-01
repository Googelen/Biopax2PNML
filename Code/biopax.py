import rdflib
from models import *
from rdflib import plugin
#rdflib.plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
#rdflib.plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')

class Reader:
	def __init__(self):
		self.net = PetriNet('')
		return
		#self.net = PetriNet()
	def read(self, inputfile):
		graph = rdflib.Graph()
		result = graph.parse(inputfile)


		query = """
			PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
			SELECT  ?left ?displayNameLeft ?right ?displayNameRight
			WHERE {
			    ?BiochemicalReaction bp:left ?left . 
			    ?BiochemicalReaction bp:right ?right .
			    ?left bp:displayName ?displayNameLeft . 
			    ?right bp:displayName ?displayNameRight
			}
		"""

		for x in graph.query(query):
			counter=0
			while(x.left):
				self.processQuery(x.left[counter],x.displayNameLeft[counter], x.right[0], x.displayNameRight[0])
				counter++
			#print("left: %s right: %s" % x)
		readCatalysis(inputfile)
		return self.net

		#print("graph has %s statements." % len(graph))
		#namespaces = {'bp': 'http://www.biopax.org/release/biopax-level3.owl'}
		#print(self.root.nsmap)
		#description = self.root.findall('bp:BiochemicalReaction',namespaces=self.root.nsmap)
		#print(description)
	def readCatalysis(self, inputfile):
		graph = rdflib.Graph()
		result = graph.parse(inputfile)


		query = """
			PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
			SELECT  ?controller ?controlled ?displayNameController ?displayNameControlled
			WHERE {
			    ?Catalysis bp:controller ?controller . 
			    ?Catalysis bp:controlled ?controlled .
			    ?controller bp:displayName ?displayNameController . 
			    ?controlled bp:displayName ?displayNameControlled
			}
		"""
		for x in graph.query(query):
			#This works both ways
			processQuery(x.controller, x.displayNameController,x.controlled,x.displayNameControlled)
			processQuery(x.controlled, x.displayNameControlled,x.controller,x.displayNameController)
		
	
	def processQuery(self, left,nameLeft, right,nameRight):
		placeLeft = Place(left, nameLeft)
		placeRight = Place(right, nameRight)
		transition = Transition()
		arcleft = Arc(placeLeft, transition)
		arcRight = Arc(transition, placeRight)

		self.net.newPlace(placeLeft)
		self.net.newPlace(placeRight)
		self.net.newTransition(transition)
		self.net.newArc(arcleft)
		self.net.newArc(arcRight)
		
	def readPlaces(self):
		return self.net.places
	def readTransitions(self):
		return self.net.transitions
	def readArcs(self):
		return self.net.arcs
