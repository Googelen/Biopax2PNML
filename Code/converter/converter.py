from rdflib.namespace import Namespace, split_uri, XSD
from rdflib.term import Literal
from models import Direction

BP = Namespace('http://www.biopax.org/release/biopax-level3.owl')
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
		 """
		 #Luc's comments
		 """
		 I thought that the AND relation ship works with multiple input places and OR relations work with multiple transitions
		 I thought he said that in the meeting.
		 However if a transition has 2 catalysis and they both do the same thing
		 You need to duplicate the reaction and have a second catalysis pointed to the newly added transition
		 Also this direction should be both ways.
		 At least thats what I thought.
		 """
		 """
		 > OR relationships are defined using multiple control interaction instances.
		 > (BioPAX Level 3, Release Version 1 Documentation, 2010)

		Therefore an intermediate transition has to be added. However petri nets are bipartite
		and transitions must not be adjacent to transitions. Therefore another intermediate node
		has to be added: A place between the Control transition and the controlled transition.

		TODO: Is that the correct implementation?
		I am not sure, I added a file with all the drawn out situations of the controllers
		"""
		return NotImplementedError


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

			{ ?relation a bp:controller } UNION { ?relation a bp:cofactor }

			?interaction
				a ?controlClass;
				bp:controlled ?controlled;
				?relation ?participant.

			OPTIONAL { ?participant bp:displayName ?participantName }
			OPTIONAL { ?interaction bp:catalysisDirection ?direction }
			OPTIONAL { ?interaction bp:controlType ?controlType }
		}
	"""
	#This query does not only select active control stuff, and also not only catalysis, or am I wrong?
	#If this should be specific should I add ?controlClass a bp:Catalysis?
	#Also there is no such thing as bp:controlClass, so I suppose you ment ?controlClass

	def convert(self):
		for control in self.graph.query(self.query):
			self.add_control(control)

	def add_control(self, control):
		"""Adds a controller to a controlled transition.

		Catalysis can only be of activating control type. Thus the controllers and cofactors are added to input
		places of the transition.

		If the direction is reversible, the transition gets duplicated.
		"""
		#Luc's comments
		"""
		A controller should be both ways right? So I suspect that the get_direction etc. may be superfluous...
		At least, I do not see the use for it.
		"""
		place = self.net.create_place(split_uri(control.participant)[1], control.participantName)
		transitions = self.get_transitions(control)

		for transition in transitions:
			self.connect(transition, place)

	def connect(self, transition, place):
		# Default direction for Direction.unknown is left to right.
		if transition.direction is Direction.right_to_left:
			self.net.create_arc(transition, place)
		else:
			self.net.create_arc(place, transition)

	def get_transitions(self, control):
		# TODO: This should also duplicate this transition so that each control has its own transition(s). For that (uid, direction, control) should probably the index for the transitions dict.
		direction = self.get_direction(control)
		uid = split_uri(control.interaction)[1]

		transitions = []

		if direction is Direction.left_to_right or direction is Direction.reversible:
			transitions.append(self.get_transition_with_correct_direction(uid, Direction.left_to_right))
			# TODO: For left_to_right, this should also turn around an existing right_to_left transition.

		if direction is Direction.reversible:
			transitions.append(self.net.create_transition(uid, Direction.right_to_left))

		if direction is Direction.left_to_right:
			transitions.append(self.get_transition_with_correct_direction(uid, Direction.right_to_left))
			# TODO: This should also turn around an existing left_to_right transition!!!

		return transitions

	def get_direction(self, control):
		direction = Direction.unknown

		if control.direction is REVERSIBLE:
			direction = Direction.reversible

		if control.direction is PHYSIOL_LTR or control.direction is IRR_LTR:
			direction = Direction.left_to_right

		if control.direction is PHYSIOL_RTL or control.direction is IRR_RTL:
			direction = Direction.right_to_left

		return direction

	def get_transition_with_correct_direction(self, uid, direction):

		if self.net.transitions.get((uid, Direction.unknown)):
			return self.update_transition_direction(uid, Direction.unknown, direction)
		else:
			return self.net.create_transition(uid, Direction.left_to_right)

	def update_transition_direction(self, uid, old_direction, new_direction):
		transition = self.transitions[(uid, old_direction)]
		transition.direction = new_direction

		self.transitions.pop((uid, old_direction))
		self.transitions[(uid, new_direction)] = transition

		# TODO: This should also change the arcs.

		return transition