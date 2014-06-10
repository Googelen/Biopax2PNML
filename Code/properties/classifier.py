import itertools


class NetClassifier:
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
	def get_pre_post_places(self):
		return self.places

	def get_pre_post_transitions(self):
		return self.transitions
		
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

	def is_not_branching(self, nodes):
		"""Check if nodes contains at least one branching node.

		:param nodes: Iterable of Places or Transitions
		:return: True if nodes contains at least one branching node.
		"""
		return all([(len(pre) <= 1) and (len(post) > 1) and (len(pre) == len(post)) for (pre, post) in nodes.values()])

	def is_extended_classes(self):
		"""Check if net is Extended Free Choice and/or Extended Simple.

		:rtype : tuple(Bool, Bool)
		:return: (is_extended_free_choice, is_extended_simple)
		"""
		extended_free_choice = True
		for (_, post1), (_, post2) in itertools.combinations(self.places.values(), 2):
			if not (post1.isdisjoint(post2) or post1 == post2):
				extended_free_choice = False

			if not (post1.isdisjoint(post2) or post1 <= post2 or post2 <= post1):
				return False, False

		return extended_free_choice, True
