import itertools


class NetClassifier:
	def __init__(self, net):
		self.net = net
		self.places = {place: (set(), set()) for place in self.net.places}
		self.transitions = {transition: (set(), set()) for transition in self.net.transitions}

	@property
	def classify(self):
		"""Classify net.

		Check if net is
		State Machine (there are neither forward branching nor backward branching transitions),
		Synchronisation Graph (there are neither forward branching nor backward branching places),
		Extended Free Choice (transitions in conflict have identical sets of preplaces),
		Extended Simple (every transition is involved in one conflict at most).

		:return: Dict of classes to boolean values.
		"""
		return {
			'state_machine': not self.contains_branching_node(self.transitions),
			'synchronisation_graph': not self.contains_branching_node(self.places),
			'extended_free_choice': self.is_extended_free_choice(),
			'extended_simple': self.is_extended_simple()
		}

	def get_pre_post_neighbours(self):
		"""Adds sources and targets from all arcs to pre- and post-neighbour sets of self.places and self.transitions.
		"""
		for arc in self.net.arcs:

			if arc.source in self.places:
				# source is Place => target is a Transition
				self.update_node(arc, self.places, self. transitions)

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

	def contains_branching_node(self, nodes):
		"""Check if nodes contains at least one branching node.

		:param nodes: Iterable of Places or Transitions
		:return: True if nodes contains at least one branching node.
		"""
		return all([(sources > 1) and (targets > 1) and (sources == targets) for (sources, targets) in nodes])
		
	def is_extended_free_choice(self):
		for combined_places in itertools.combinations(self.places,2):
			place1 = self.places[combined_places[0]]
			place2 = self.places[combined_places[1]]
			if(not(place1[1].isdisjoined(place2[1]) or place1[1]== place2[1])):
				return False
		return True

	def is_extended_simple(self):
		for combined_places in itertools.combinations(self.places,2):
			place1 = self.places[combined_places[0]]
			place2 = self.places[combined_places[1]]
			if(not(place1[1].isdisjoined(place2[1]) or place1[1]<=place2[1] or place2[1]<=place1[1])):
				return False
		return True
