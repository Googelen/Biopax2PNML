class PetriNet:
	def __init__(self, description):
		self.description = description
		self.places = {}
		self.transitions = {}
		self.arcs = set()

	def create_place(self, uid, description=''):
		"""Get place with ID from this petri net. Create new place if non existent.

		Description is not updated if place already exists.

		:rtype : Place
		:param uid: ID of place to be returned.
		:return: Place with ID uid.
		"""
		if uid not in self.places:
			self.places[uid] = Place(uid, description)

		return self.places[uid]

	def create_transition(self, uid):
		""" Get transition with ID uid from this petri net. Create new transition if non existent.


		:rtype : Transition
		:param uid: ID of transition to be returned.
		:return: Transition with ID uid.
		"""
		if uid not in self.transitions:
			self.transitions[uid] = Transition(uid)

		return self.transitions[uid]

	def create_arc(self, source, target):
		"""Create and get arc from source to target.

		:rtype : Arc
		:param source: Starting node of this arc.
		:param target: Ending node of this arc.
		:return: Arc from source to target
		"""
		arc = Arc(source, target)
		self.arcs.add(arc)

		return arc


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
		Node.__init__(self, uid)
		self.description = description


class Arc:
	def __init__(self, source, target):
		self.source = source
		self.target = target


class Transition(Node):
	def __init__(self, uid):
		Node.__init__(self, uid)