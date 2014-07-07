class PetriNet:
	def __init__(self, description):
		self.description = description
		self.places = {}
		self.transitions = {}
		self.arcs = set()

	def newPlace(self, place):
		""" Add new place to places in this petri net. Return unique place for place.id

		If place with same id already exists, then input place is not added and
		previously existing place is returned.

		:rtype : Place
		:param place: Place to be added to petri net.
		:return: Place with same id as input place.
		"""
		if place not in self.places:
			self.places[place.id] = place

		return self.places[place.id]

	def newTransition(self, transition):
		""" Add new transition to this petri net. Return unique transition for transition.id

		If transition with same id already exists, then input transition is not added and
		previously existing transition is returned.

		:rtype : Transition
		:param transition: Transition to be added to petri net.
		:return: Transition with same id as input place.
		"""
		if transition not in self.transitions:
			self.transitions[transition.id] = transition

		return self.transitions[transition.id]

	def newArc(self, arc):
		self.arcs.add(arc)


class Node:
	def __init__(self, uid):
		self.id = uid

	def __eq__(self, other):
		return isinstance(other, self.__class__) and (self.id == other.id)

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.id)


class Place(Node):
	def __init__(self, uid, description):
		Node.__init__(self, uid.rsplit('/', 1)[1])  # split should be executed before calling constructor.
		self.description = description


class Arc:
	def __init__(self, source, target):
		self.source = source
		self.target = target


class Transition(Node):
	def __init__(self, uid):
		Node.__init__(self, uid.rsplit('/', 1)[1])  # split should be executed before calling constructor.