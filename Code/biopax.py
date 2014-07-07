import rdflib
from rdflib.namespace import Namespace, split_uri, XSD
from rdflib.term import Literal
from models import *


BP = Namespace('http://www.biopax.org/release/biopax-level3.owl')
RTL = Literal('RIGHT-TO-LEFT', datatype=XSD.string)
LTR = Literal('LEFT-TO-RIGHT', datatype=XSD.string)
REVERSIBLE = Literal('REVERSIBLE', datatype=XSD.string)


class Reader:
	def __init__(self):
		self.net = PetriNet('')

	def read(self, inputfile):
		graph = rdflib.Graph()
		graph.parse(inputfile)
		# Maybe rather parse a local copy of biopax-level3.owl for performance reason and since the file doesn't
		# change anyway?
		graph.parse(BP, format='application/rdf+xml')
		#graph.parse('biopax-level3.owl')

		self.add_conversions(graph)
		self.add_controls(graph)

		return self.net

	def add_conversions(self, graph):

		conversion_query = """
			PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
			SELECT ?conversionClass ?interaction ?relation ?participant ?participantName ?direction
			WHERE {
				?conversionClass rdfs:subClassOf+ bp:Conversion.
				?participantRelation rdfs:subPropertyOf bp:participant.

				?interaction
					a ?conversionClass;
					?relation ?participant.

				OPTIONAL { ?participant bp:displayName ?participantName }
				OPTIONAL { ?interaction bp:conversionDirection ?direction }
			}
		"""

		for conversion in graph.query(conversion_query):
			self.add_conversion(conversion)

	def add_conversion(self, conv):

		transition = self.net.create_transition(split_uri(conv.interaction)[1])
		place = self.net.create_place(split_uri(conv.participant)[1], conv.participantName)

		if conv.direction is REVERSIBLE:  # TODO: Is this intended behaviour?
			self.net.create_arc(transition, place)
			self.net.create_arc(place, transition)

		elif (conv.relation is BP.right and conv.direction is RTL) \
				or (conv.relation is BP.left and (conv.direction is LTR or not conv.direction)):
			self.net.create_arc(place, transition)

		else:  # TODO: Is this intended behaviour for _all_ other cases (i.e. if participant is neither left nor right)?
			self.net.create_arc(transition, place)

	def add_controls(self, graph):

		control_query = """
			PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
			SELECT ?controlClass ?interaction ?relation ?participant ?participantName ?direction ?controlType
			WHERE {
				?controlClass rdfs:subClassOf+ bp:Control.
				?relation rdfs:subPropertyOf bp:participant.

				?interaction
					a ?controlClass;
					?relation ?participant.

				OPTIONAL { ?participant bp:displayName ?participantName }
				OPTIONAL { ?interaction bp:catalysisDirection ?direction }
				OPTIONAL { ?interaction bp:controlType ?controlType }
			}
		"""

		for control in graph.query(control_query):
			self.add_control(control)

	def add_control(self, control):
		"""Not implemented

		How is a control interaction implemented in a petri net?
		controllers are places. controlled are transitions (e.g. a BiochemicalReaction).
		That works for exactly one controller: We can connect controller and controlled directly.
		But what happens if there is more than one controller? What happens if there are other
		participants (such as cofactor)?

		Connecting all controllers directly with the controlled is not an option since
		 > Multiple controllers are all required for the control to occur (AND relationship).
		 > OR relationships are defined using multiple control interaction instances.
		 > (BioPAX Level 3, Release Version 1 Documentation, 2010)

		Therefore an intermediate transition has to be added. However petri nets are bipartite
		and transitions must not be adjacent to transitions. Therefore another intermediate node
		has to be added: A place between the Control transition and the controlled transition.

		TODO: Is that the correct implementation?
		"""
		return NotImplemented


	def old(self, graph, query):

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


	def readPlaces(self):
		return self.net.places

	def readTransitions(self):
		return self.net.transitions

	def readArcs(self):
		return self.net.arcs