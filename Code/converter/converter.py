from rdflib.namespace import Namespace, split_uri, XSD
from rdflib.term import Literal
from models import Direction

BP = Namespace('http://www.biopax.org/release/biopax-level3.owl')
RTL = Literal('RIGHT-TO-LEFT', datatype=XSD.string)
LTR = Literal('LEFT-TO-RIGHT', datatype=XSD.string)
REVERSIBLE = Literal('REVERSIBLE', datatype=XSD.string)


class BiopaxConverter(object):

	# Order in which subclasses of BiopaxConverter get executed when converting.
	order = -1

	def __init__(self, graph, petri_net):
		"""Converter class. All conversions from BioPAX to a Petri Net must use this
		as a superclass.

		:param graph: rdflib.Graph the parsed BioPAX file.
		:param petri_net: PetriNet the Petri Net to add nodes and arcs to.
		"""
		self.graph = graph
		self.net = petri_net

	def convert(self):
		"""Convert class from BioPAX to a Petri Net.

		Add transitions, places, and arcs to petri_net.
		"""
		raise NotImplementedError


class ConversionConverter(BiopaxConverter):

	order = 20

	def __init__(self, graph, petri_net):
		"""Converts members of class Conversion from BioPAX to a Petri Net.

		:param graph: rdflib.Graph
		:param petri_net: PetriNet
		"""
		BiopaxConverter.__init__(self, graph, petri_net)

	query = """
		PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
		SELECT *
		WHERE {
			?conversionClass rdfs:subClassOf+ bp:Conversion.
			?relation rdfs:subPropertyOf bp:participant.

			?interaction
				a ?conversionClass;
				?relation ?participant.

			OPTIONAL { ?participant bp:displayName ?participantName }
			OPTIONAL { ?participant bp:cellularLocation ?participantLocation }
			OPTIONAL { ?interaction bp:conversionDirection ?direction }
			OPTIONAL { ?interaction bp:spontaneous ?spontaneous }
		}
	"""

	def convert(self):
		for conversion in self.graph.query(self.query):
			self.add_conversion(conversion)

	def add_conversion(self, conv):

		transitions = self.create_transitions(conv)

		location = ' (' + conv.participantLocation + ') ' if conv.participantLocation else ''
		place = self.net.create_place(split_uri(conv.participant)[1], conv.participantName + location)

		for transition in transitions:
			self.connect(transitions, place, conv.relation)

	def connect(self, transition, place, relation):
		# Default direction for Direction.unknown is left to right.
		if (transition.direction is Direction.right_to_left and relation is BP.right) or \
				(transition.direction is not Direction.right_to_left and relation is BP.left):
			self.net.create_arc(place, transition)
		else:
			self.net.create_arc(transition, place)

	def create_transitions(self, conv):
		direction = self.get_direction(conv.spontaneous, conv.direction)
		uid = split_uri(conv.interaction)[1]

		if direction is Direction.reversible:
			return [self.net.create_transition(uid, Direction.left_to_right),
					self.net.create_transition(uid, Direction.right_to_left)]

		return [self.net.create_transition(uid, direction)]

	def get_direction(self, spontaneous_property, direction_property):
		direction = Direction.unknown

		if direction_property and direction_property is RTL:
			direction = Direction.right_to_left

		if direction_property and direction_property is LTR:
			direction = Direction.left_to_right

		if direction_property and direction_property is REVERSIBLE:
			direction = Direction.reversible

		# Spontaneous property overwrites direction property.
		if spontaneous_property and spontaneous_property is RTL:
			direction = Direction.right_to_left

		if spontaneous_property and spontaneous_property is LTR:
			direction = Direction.left_to_right

		return direction


class ControlConverter(BiopaxConverter):

	order = 10
	def __init__(self, graph, petri_net):
		"""Converts members of class Control from BioPAX to a Petri Net.

		:param graph: rdflib.Graph
		:param petri_net: PetriNet
		"""
		BiopaxConverter.__init__(self, graph, petri_net)

	query = """
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

	def convert(self):
		for control in self.graph.query(self.query):
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
		return NotImplementedError