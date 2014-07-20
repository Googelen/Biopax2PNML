from rdflib.namespace import Namespace, split_uri, XSD
from rdflib.term import Literal
from models import Direction

BP = Namespace('http://www.biopax.org/release/biopax-level3.owl#')
RTL = Literal('RIGHT-TO-LEFT', datatype=XSD.string)
LTR = Literal('LEFT-TO-RIGHT', datatype=XSD.string)
REVERSIBLE = Literal('REVERSIBLE', datatype=XSD.string)
PHYSIOL_LTR = Literal('PHYSIOL-LEFT-TO-RIGHT', datatype=XSD.string)
PHYSIOL_RTL = Literal('PHYSIOL-RIGHT-TO-LEFT', datatype=XSD.string)
IRR_LTR = Literal('IRREVERSIBLE-LEFT-TO-RIGHT', datatype=XSD.string)
IRR_RTL = Literal('IRREVERSIBLE-RIGHT-TO-LEFT', datatype=XSD.string)


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

	def get_direction(self, control):
		direction = Direction.unknown

		if REVERSIBLE == control.direction:
			direction = Direction.reversible

		if PHYSIOL_LTR == control.direction or IRR_LTR == control.direction:
			direction = Direction.left_to_right

		if PHYSIOL_RTL == control.direction or IRR_RTL == control.direction:
			direction = Direction.right_to_left

		return direction


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
			self.connect(transition, place, conv.relation)

	def connect(self, transition, place, relation):
		# Default direction for Direction.unknown is left to right.
		if (transition.direction == Direction.right_to_left and relation == BP.right) or \
				(transition.direction != Direction.right_to_left and relation == BP.left):
			self.net.create_arc(place, transition)
		else:
			self.net.create_arc(transition, place)

	def create_transitions(self, conv):
		direction = self.get_conversion_direction(conv.spontaneous, conv.direction)
		uid = split_uri(conv.interaction)[1]

		if direction == Direction.reversible:
			return [self.net.create_transition(uid, Direction.left_to_right),
					self.net.create_transition(uid, Direction.right_to_left)]
		else:
			return [self.net.create_transition(uid, direction)]

	def get_conversion_direction(self, spontaneous_property, direction_property):
		direction = Direction.unknown

		if direction_property and direction_property == RTL:
			direction = Direction.right_to_left

		if direction_property and direction_property == LTR:
			direction = Direction.left_to_right

		if direction_property and direction_property == REVERSIBLE:
			direction = Direction.reversible

		# Spontaneous property overwrites direction property.
		if spontaneous_property and spontaneous_property == RTL:
			direction = Direction.right_to_left

		if spontaneous_property and spontaneous_property == LTR:
			direction = Direction.left_to_right

		return direction


class ActivatingControlConverter(BiopaxConverter):

	order = 100

	def __init__(self, graph, petri_net):
		"""Converts members of class Control from BioPAX to a Petri Net.

		:param graph: rdflib.Graph
		:param petri_net: PetriNet
		"""
		BiopaxConverter.__init__(self, graph, petri_net)

	query = """
		PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
		SELECT *
		WHERE {
			?controlClass rdfs:subClassOf+ bp:Control.

			{ ?relation rdfs:subClassOf* bp:controller }
			UNION
			{ ?relation rdfs:subClassOf* bp:cofactor }

			?interaction
				a ?controlClass;
				bp:controlled ?controlled;
				?relation ?participant.

			OPTIONAL { ?participant bp:displayName ?participantName }
			OPTIONAL { ?interaction bp:catalysisDirection ?direction }
			{ ?interaction a bp:Catalysis } UNION { ?interaction bp:controlType 'ACTIVATION' }
		}
	"""

	def convert(self):
		for control in self.graph.query(self.query):
			self.add_control(control)

	def add_control(self, control):
		"""Adds a controller to a controlled transition.

		Catalysis can only be of activating control type. Thus the controllers and cofactors are added to input
		places of the transition.

		If the direction is reversible, the transition gets duplicated.
		"""
		# Create place for new controller or cofactor
		place = self.net.create_place(split_uri(control.participant)[1], control.participantName)
		# Get all transitions which are instances of controlled
		transitions = self.get_transitions(control)

		for transition in transitions:
			self.connect(transition, place)

	def connect(self, transition, place):
		self.net.create_arc(transition, place)
		self.net.create_arc(place, transition)

	def get_transitions(self, control):
		direction = self.get_direction(control)
		control_id = split_uri(control.interaction)[1]
		conversion_id = split_uri(control.controlled)[1]

		transitions = []

		if direction == Direction.left_to_right or direction == Direction.reversible:
			t = self.net.create_transition(conversion_id, Direction.left_to_right, control_id)
			transitions.append(t)

		if direction == Direction.right_to_left or direction == Direction.reversible:
			t = self.net.create_transition(conversion_id, Direction.right_to_left, control_id)
			transitions.append(t)

		if not direction:
			t = self.net.create_transition(conversion_id, Direction.unknown, control_id)
			transitions.append(t)

		return transitions

class ActivationInhibitionAlossteric(BiopaxConverter):
	def __init__(self, graph, petri_net):
		"""Converts members of class Control with controlType Inhibition, Inhibition-Alossteric and Activation-Alossteric from BioPAX to a Petri Net.

		:param graph: rdflib.Graph
		:param petri_net: PetriNet
		"""
		BiopaxConverter.__init__(self, graph, petri_net)

	query = """
		PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
		SELECT *
		WHERE {
			?controlClass rdfs:subClassOf+ bp:Control.

			{ ?relation a bp:controller } UNION { ?relation a bp:cofactor }

			?interaction
				a ?controlClass;
				bp:controlled ?controlled;
				?relation ?participant.

			OPTIONAL { ?participant bp:displayName ?participantName }
			OPTIONAL { ?interaction bp:catalysisDirection ?direction }
			{ ?interaction a bp:Catalysis }	UNION { ?interaction bp:controlType ?types } 

			VALUES (?types) { 
			("INHIBITION")
			("INHIBITION-ALOSSTERIC")
			("ACTIVATION-ALOSSTERIC")
			("ACTIVATION")
			}
		}
	"""

	def convert(self):
		for control in self.graph.query(self.query):
			self.add_control(control)

	def add_control(self, control):
		"""Adds a controller to a controlled transition.

		Catalysis can only be of activating control type. Thus the controllers and cofactors are added to input
		places of the transition.

		If the direction is reversible, the transition gets duplicated.
		"""
		# Create place for new controller or cofactor
		place = self.net.create_place(split_uri(control.participant)[1], control.participantName)
		# Get all transitions which are instances of controlled
		transitions = self.get_transitions(control)

		for transition in transitions:
			self.connect(transition, place)

		#TODO finish this stuff
		raise NotImplementedError


class InhibitionIrreversible(BiopaxConverter):
	def __init__(self, graph, petri_net):
		"""Converts members of class Control with controlType Inhibition, Inhibition-Alossteric and Activation-Alossteric from BioPAX to a Petri Net.

		:param graph: rdflib.Graph
		:param petri_net: PetriNet
		"""
		BiopaxConverter.__init__(self, graph, petri_net)

	query = """
		PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
		SELECT *
		WHERE {
			?controlClass rdfs:subClassOf+ bp:Control.

			{ ?relation a bp:controller } UNION { ?relation a bp:cofactor }

			?interaction
				a ?controlClass;
				bp:controlled ?controlled;
				?relation ?participant.

			OPTIONAL { ?participant bp:displayName ?participantName }
			OPTIONAL { ?interaction bp:catalysisDirection ?direction }
			{ ?interaction a bp:Catalysis }	UNION { ?interaction bp:controlType ?types } 
			
			VALUES (?types) { 
			("INHIBITION-IRREVERSIBLE")
			}
		}
	"""

	def convert(self):
		for control in self.graph.query(self.query):
			self.add_control(control)

	def add_control(self, control):
		"""Adds a controller to a controlled transition.

		Catalysis can only be of inhibition irreversible control type. Thus the controllers and cofactors are added to input
		places of the transition.

		If the direction is reversible, the transition gets duplicated.
		"""
		# Create place for new controller or cofactor
		place = self.net.create_place(split_uri(control.participant)[1], control.participantName)
		place2 = self.net.create_place(split_uri(control.participant)[1]+"_IRREVERSIBLE", control.participantName+"*")
		# Create transitions necessairy
		transitions = self.create_transitions(control)

		#Create arcs
		self.connect(transitions, place, place2)

	def create_transitions(self, control):
		"""
		Creats 3 transitions which are neccesairy for the contruction of a irreversible controller
		2 are created for the controlled
		1 is created for the 2 instances of the controller

		:rtype: Set(Transition)

		"""
		direction = self.get_direction(control)
		transitions = []
		transitions.append(self.net.create_transition(split_uri(control.controlled)[1],direction,split_uri(control.interaction)[1]))
		transitions.append(self.net.create_transition(split_uri(control.controlled)[1],Direction.reverse(direction),split_uri(control.interaction)[1]))
		transitions.append(self.net.create_transition(split_uri(control.participant)[1],Direction.left_to_right, split_uri(control.participant)[1]+"_IRREVERSIBLE",))

		return transitions

	def add_reversed_arcs(self, interaction, transition):
		current_direction = []
		ingoing_places = []
		outgoing_places = []

	def connect(self, transitions, place1, place2):
		self.connect_both_ways(transitions[0],place1)
		self.connect_both_ways(transitions[1],place2)

		self.net.create_arc(place1,transitions[2])
		self.net.create_arc(transitions[2],place2)

	def connect_both_ways(self, transition, place):
		self.net.create_arc(transition, place)
		self.net.create_arc(place, transition)

class NonUnCompetitiveOther(BiopaxConverter):
	def __init__(self, graph, petri_net):
		"""Not implemented

		:param graph: rdflib.Graph
		:param petri_net: PetriNet
		"""
		BiopaxConverter.__init__(self, graph, petri_net)