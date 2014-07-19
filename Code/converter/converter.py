from rdflib.namespace import Namespace, split_uri, XSD
from rdflib.term import Literal

BP = Namespace('http://www.biopax.org/release/biopax-level3.owl')
RTL = Literal('RIGHT-TO-LEFT', datatype=XSD.string)
LTR = Literal('LEFT-TO-RIGHT', datatype=XSD.string)
REVERSIBLE = Literal('REVERSIBLE', datatype=XSD.string)


class BiopaxConverter(object):
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
	def __init__(self, graph, petri_net):
		"""Converts members of class Conversion from BioPAX to a Petri Net.

		:param graph: rdflib.Graph
		:param petri_net: PetriNet
		"""
		BiopaxConverter.__init__(self, graph, petri_net)

	query = """
		PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
		SELECT ?conversionClass ?interaction ?relation ?participant ?participantName ?direction
		WHERE {
			?conversionClass rdfs:subClassOf+ bp:Conversion.
			?relation rdfs:subPropertyOf bp:participant.

			?interaction
				a ?conversionClass;
				?relation ?participant.

			OPTIONAL { ?participant bp:displayName ?participantName }
			OPTIONAL { ?interaction bp:conversionDirection ?direction }
		}
	"""

	def convert(self):
		for conversion in self.graph.query(self.query):
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


class ControlConverter(BiopaxConverter):
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