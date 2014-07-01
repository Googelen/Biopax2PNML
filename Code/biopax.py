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
			self.processQuery(x.left, x.displayNameLeft, x.right, x.displayNameRight)
			#print("left: %s right: %s" % x)

		self.readCatalysis(inputfile)

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
			SELECT  ?controller ?displayNameController ?controlled  ?leftPlaceControlled ?rightPlaceControlled
			WHERE {
			    ?Catalysis bp:controller ?controller . 
			    ?Catalysis bp:controlled ?controlled .
			    ?controller bp:displayName ?displayNameController .
			    ?controlled bp:left ?leftPlaceControlled.
			    ?controlled bp:left ?rightPlaceControlled

			}
		"""
		tempPlaces = []
		tempArcs = []
		for x in graph.query(query):
			# the controlled is not a place, but a entire reaction, so this is wrong, it should go directly into the transition of the reaction which is in the 'controlled'
			#it should find the transition which is the pretransition of the place right of the reaction which it points to
			transition = self.findTransition(x.leftPlaceControlled, x.rightPlaceControlled)
			catalysisPlace = Place(x.controller,x.displayNameController)

			tempArcs.append(Arc(catalysisPlace,transition))
			tempArcs.append(Arc(transition,catalysisPlace))
			tempPlaces.append(catalysisPlace)
		i=0
		while i<len(tempPlaces):
			self.net.newPlace(tempPlaces[i])
			i += 1
		j=0
		while j<len(tempArcs):
			self.net.newArc(tempArcs[j])
			j+=1


	def findTransition(self,leftPlace,rightPlace):
		"""
		find the transition inbeteen the places defined by the not yet id-ified (making up words here) string which represends the place left and right

		"""
		leftPlaceId = leftPlace.rsplit('/',1)[1]
		rightPlaceId = rightPlace.rsplit('/',1)[1]
		transition=[]
		for arc in self.net.arcs:
			if(isinstance(arc.source, Place) and arc.source.id==leftPlaceId):
				transition = arc.target
				print(arc.source.id +" "+leftPlaceId)

		for arc in self.net.arcs:
			if(isinstance(arc.target, Place) and arc.target.id==rightPlaceId):
				if(transition is arc.source):
					return transition


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
