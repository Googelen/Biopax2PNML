class Direction:
	unknown = 0
	left_to_right = 1
	right_to_left = 2
	reversible = 3

	@staticmethod
	def reverse(direction):
		if direction is Direction.right_to_left:
			return Direction.left_to_right
		elif direction is Direction.reversible:
			return direction
		else:
			# Structure wise unknown is treated like left_to_right
			return Direction.right_to_left


class PetriNet:
	def __init__(self, description):
		self.description = description
		self.places = {}
		self.transitions = {}
		self.arcs = set()
		self.arcs_from_source = {}
		self.arcs_from_target = {}

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

	def get_transition(self, control_id):
		transitions=[]
		for transition in self.transitions:
			if transition[2] == control_id:
				transitions.append(self.transitions[transition])
		return transitions;

	def create_transition(self, uid, direction=Direction.unknown, control_id=None):
		""" Get transition with given attributes from this petri net. Create new transition if non existent.

		Update any existing transition with same ID and without control_id. This possibly changes direction of
		a transition since Catalysis direction overwrites Conversion direction.

		:rtype : Transition
		:param uid: ID of transition to be returned.
		:param direction: Either Direction.left_to_right, Direction.right_to_left, or Direction.unknown.
		Defaults to Direction.unknown.
		:param control_id: ID of control which this transition is part of. Defaults to None.
		:return: Transition with uid, direction and control_id.
		"""

		if (uid, Direction.unknown, None) in self.transitions:
			# If there is transition with same ID and no information about direction and control, use that.
			self.change_transition(uid, Direction.unknown, direction, control_id)
			
		elif (uid, direction, None) in self.transitions:
			# If there is transition with same ID and direction but unknown control, use that.
			self.change_transition(uid, direction, direction, control_id)
			
		elif (uid, Direction.reverse(direction), None) in self.transitions:
			# If there is transition with same ID and reverse direction, but unknown control, use that.
			self.change_transition(uid, Direction.reverse(direction), direction, control_id)
			
		elif (uid, Direction.left_to_right, None) in self.transitions:
			#If there is a transition with same ID but unknown direction and known control
			direction = self.change_transition(uid, Direction.left_to_right, direction, control_id)
			
		elif (uid, Direction.right_to_left, None) in self.transitions:
			direction = self.change_transition(uid, Direction.right_to_left, direction, control_id)

		if (uid, direction, control_id) not in self.transitions:
			# If there still doesn't exist a transition with same attributes, create a new one.
			self.transitions[(uid, direction, control_id)] = Transition(uid, direction, control_id)

		return self.transitions[(uid, direction, control_id)]

	def change_transition(self, uid, old_direction, new_direction, control_id):
		"""Update transition from old to new values. Change direction of connected arcs if necessary.

		:rtype : Transition
		:param uid: ID of transition to be changed.
		:param old_direction: Direction of existing transition.
		:param new_direction: Direction to which transition should be updated.
		:param control_id: ID of control structure which transitions gets added to.
		:return: Updated transition.
		"""
		transition = self.transitions.pop((uid, old_direction, None))

		if new_direction != Direction.unknown:
			# Only update direction if new direction doesn't contain less information.

			if Direction.reverse(old_direction) == new_direction:
				# Only reverse arcs if direction actually changes
				self.reverse_arcs(transition)

			transition.direction = new_direction

		transition.control = control_id

		self.transitions[(uid, transition.direction, control_id)] = transition
		return transition.direction

	def reverse_arcs(self, transition):
		"""Reverse all arcs directly connected to transition.

		:param transition: Transition from which all arcs should be reversed.
		"""
		reversed_arcs_from_target = self.reverse_arcs_from_one_direction(self.arcs_from_source.get(transition))
		reversed_arcs_from_source = self.reverse_arcs_from_one_direction(self.arcs_from_target.get(transition))

		self.arcs_from_source[transition].update(reversed_arcs_from_source)
		self.arcs_from_target[transition].update(reversed_arcs_from_target)

	def reverse_arcs_from_one_direction(self, original_arcs):
		"""Reverse all arcs in original_arcs. Remove arcs from original_arcs and from self.arcs.

		:rtype : Set(Arc)
		:param original_arcs: Either self.arcs_from_source[source] or self.arcs_from_target[target]
		:return: Set of reversed arcs.
		"""
		reversed_arcs = set()

		for arc in original_arcs:
			# Remove old arc
			self.arcs.remove(arc)
			original_arcs.remove(arc)

			# Create new arc
			reversed_arc = Arc(arc.target, arc.source)

			# Add new arc to sets
			self.arcs.add(reversed_arc)
			reversed_arcs.add(reversed_arc)

		return reversed_arcs

	def get_arcs(self, transition):
		arcs = []
		for arc in self.arcs:
			if arc.source.id == transition.id:
				arcs.append(arc)
			if arc.target.id == transition.id:
				arcs.append(arc)
		return arcs

	def create_arc(self, source, target):
		"""Create and get arc from source to target.

		:rtype : Arc
		:param source: Starting node of this arc.
		:param target: Ending node of this arc.
		:return: Arc from source to target
		"""
		arc = Arc(source, target)
		self.arcs.add(arc)

		arcs = self.arcs_from_source.get(source, set())
		arcs.add(arc)
		self.arcs_from_source[source] = arcs

		arcs = self.arcs_from_target.get(target, set())
		arcs.add(arc)
		self.arcs_from_target[target] = arcs

		return arc


class Node:
	def __init__(self, uid):
		self.id = uid

	def __attributes(self):
		return self.id

	def __eq__(self, other):
		return isinstance(other, self.__class__) and (self.__attributes() == other.__attributes)

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.__attributes())


class Place(Node):
	def __init__(self, uid, description):
		Node.__init__(self, uid)
		self.description = description
		# activated? Cellular location? Maybe put all in the description?


class Arc:
	def __init__(self, source, target):
		self.source = source
		self.target = target


class Transition(Node):
	def __init__(self, uid, direction=Direction.unknown, control=None):
		Node.__init__(self, uid)
		self.direction = direction
		self.control = control

	def __attributes(self):
		return self.id, self.direction, self.control