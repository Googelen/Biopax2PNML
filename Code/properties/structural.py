import itertools


class NetStructuralProperties:
	def __init__(self, net):
		self.net = net
		self.places = {place: (set(), set()) for place in self.net.places}
		self.transitions = {transition: (set(), set()) for transition in self.net.transitions}

		self.get_pre_post_neighbours()

	@property
	def classifications(self):
		"""Classify net and return classifications.

		Check if net is
		State Machine (there are neither forward branching nor backward branching transitions),
		Synchronisation Graph (there are neither forward branching nor backward branching places),
		Extended Free Choice (transitions in conflict have identical sets of preplaces),
		Extended Simple (every transition is involved in one conflict at most).

		:return: Dict of classes to boolean values. Each entry is True if the classification applies.
		"""

		is_extended_free_choice, is_extended_simple = self.is_extended_classes()

		return {
			'state_machine': self.is_not_branching(self.transitions),
			'synchronisation_graph': self.is_not_branching(self.places),
			'extended_free_choice': is_extended_free_choice,
			'extended_simple': is_extended_simple
		}

	def get_pre_post_neighbours(self):
		"""Adds sources and targets from all arcs to pre- and post-neighbour sets of self.places and self.transitions.
		"""
		for arc in self.net.arcs:

			if arc.source in self.places:
				# source is Place => target is a Transition
				self.update_node(arc, self.places, self.transitions)

			elif arc.source in self.transitions:
				# source is Transition -> target is Place
				self.update_node(arc, self.transitions, self.places)

	def update_node(self, arc, sources, targets):
		"""Adds arc.target and arc.source as pre- and post-neighbours to targets and sources.

		Adds arc.target as post-neighbour to arc.source in sources.
		Adds arc.source as pre-neighbour to arc.target in targests.

		:param arc: Arc
		:param sources: Dict of nodes to tuple of sets of pre- and post-neighbours.
		:param targets: Dict of nodes to tuple of sets of pre- and post-neighbours.
		"""
		sources[arc.source][1].add(arc.target)
		targets[arc.target][0].add(arc.source)

	@property
	def is_pure(self):
		"""Is petri net pure?

		i.e. there are no two nodes connected in both directions.

		:rtype : Boolean
		:return: True if petri net is pure.
		"""
		# Create set of unique arcs. Remove duplicates.
		arcs = {(arc.source, arc.target) for arc in self.net.arcs}

		# Create set with undirected arcs.
		undirected_arcs = {set(arc) for arc in arcs}

		# Return if these two sets have the same number of elements.
		# If the length is equal, the petri net is pure.
		return len(arcs) == len(undirected_arcs)

	@property
	def is_homogeneous(self):
		"""Is petri net homogeneous?

		i.e. all outgoing arcs of a given place have the same multiplicity.

		:rtype : Boolean
		:return: If net is homogeneous.
		"""
		# Define keyfuncs to group arcs by.
		get_source = lambda arc: arc.source
		get_target = lambda arc: arc.target

		# Group arcs by source.
		for group in groupby(self.net.arcs, get_source):
			# Group arcs with same source by target and get length of these subgroups.
			lengths = {len(g) for g in groupby(group, get_target)}

			# If there is different lengths, the net is not homogeneous.
			if len(lengths) > 1:
				return False

		return True

	@property
	def is_static_conflict_free(self):
		"""Is petri net static conflict free?

		i.e. there are no two transitions sharing a preplace.

		:rtype : Boolean
		:return: If net is static conflict free.
		"""
		for (pre1, _), (pre2, _) in itertools.combinations(self.transitions.values(), 2):
			if not pre1.isdisjoint(pre2):
				return False

		return True

	@property
	def has_boundary_input_transitions(self):
		"""Check if petri net has boundary input transitions.

		:rtype : Boolean
		:return: True if net has boundary input transitions.
		"""
		return len(boundary_nodes(self.transitions, 'input')) > 0

	@property
	def has_boundary_output_transitions(self):
		"""Check if petri net has boundary output transitions.

		:rtype : Boolean
		:return: True if net has boundary output transitions.
		"""
		return len(boundary_nodes(self.transitions, 'output')) > 0

	@property
	def has_boundary_input_places(self):
		"""Check if petri net has boundary input places.

		:rtype : Boolean
		:return: True if net has boundary input places.
		"""
		return len(boundary_nodes(self.places, 'input')) > 0

	@property
	def has_boundary_output_places(self):
		"""Check if petri net has boundary output places.

		:rtype : Boolean
		:return: True if net has boundary output places.
		"""
		return len(boundary_nodes(self.places, 'output')) > 0

	@property
	def has_boundary_nodes(self):
		return self.has_boundary_input_places or self.has_boundary_input_transitions or \
			   self.has_boundary_output_places or self.has_boundary_output_transitions

	@property
	def is_connected(self):

		seen = set()

		if len(set.net.places) < 1 and len(set.net.transitions) < 1:
			return True
		elif len(set.net.places) < 1:
			seen.add(self.net.transitions[0])
		else:
			seen.add(self.net.places[0])

		visited = set()
		nodes = set(self.net.places + self.net.transitions)

		while len(seen) > 0 and seen < nodes:
			node = seen.pop()
			pre, post = self.transitions.get(node, self.places.get(node, (set(), set())))
			seen |= pre | post
			visited.add(node)
			seen -= visited

		return seen == nodes


def boundary_nodes(nodes, place='input'):
	"""Get  boundary nodes of net.

	:rtype : list(Places) or list(Transitions)
	:param nodes: Dict from Place or Transition to tupel of sets of Transition or Place.
	:param place: 'input' or 'output'
	:return: List of places or transitions which are boundary nodes.
	"""
	if place == 'output':
		get_set = lambda sets: set[1]
	else:
		get_set = lambda sets: set[0]

	return [t for (t, sets) in nodes.items() if len(get_set(sets)) < 1]


def groupby(arcs, keyfunc):
	return [list(g) for k, g in itertools.groupby(sorted(arcs, key=keyfunc), key=keyfunc)]
