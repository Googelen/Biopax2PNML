class PetriNet:
	def __init__(self, description):
		self.description = description;
		self.places = set()
		self.transitions = set()
		self.arcs = set()

	def newPlace(self, place):
		self.places.add(place)

	def newTransition(self, transition):
		self.transitions.add(transition)

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