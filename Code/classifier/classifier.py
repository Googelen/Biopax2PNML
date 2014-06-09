from models import *

	Class classifier:
	def classify(net):
	
		classes = {
			'state_machine': False,
			'synchronisation_graph': False,
			'extended_free_choice': False,
			'extended_simple': False
		}
	
		nodes = count_arcs_at_nodes(net.arcs)
		(places, transitions) = split_nodes(nodes)
	
		classes['state_machine'] = is_not_branching(transitions)
		classes['synchronisation_graph'] = is_not_branching(places)
	
		return classes
	
	
	def count_arcs_at_nodes(arcs):
		nodes = {}
	
		for arc in arcs:
			(sources, targets) = nodes[arc.source]
			nodes[arc.source] = (sources + 1, targets)
	
			(sources, targets) = nodes[arc.target]
			nodes[arc.target] = (sources, targets + 1)
	
		return nodes
	
	
	def split_nodes(nodes):
		transitions = {}
		places = {}
		for (d, v) in nodes.items():
			if isinstance(v, Transition):
				transitions[d] = v
			else:
				places[d] = v
	
		return (places, transitions)
	
	
	def is_not_branching(nodes):
		return all([(sources <= 1) and (targets <= 1) and (sources == targets) for (sources, targets) in nodes])
		
	def is_extended_free_choice(self,places):
		for place1 in places:
			for place2 in places:
				if(!(is_overlap(place1,place2) or is_the_same(place1,place2)))
					return False
		return True

	def is_extended_simple_choice(self,places):
		for place1 in places:
			#it should be possible to check less combinations here, by skipping if place2 is in place1
			for place2 in places:
				if(!(!is_overlap(place1,place2) or contains(place1,place2))):
					return False
		return True

	def contains(self,place1,place2):
		

	def is_overlap(self, place1, place2):
		for transition1 in place1[1]:
			for transition2 in place2[1]:
				if(transition2==transition1):
					return True
		return False

	def classify(self):
		places = create_post_places()
		self.EFC = is_extended_free_choice(places)
		self.ES = is_extended_simple(places)
