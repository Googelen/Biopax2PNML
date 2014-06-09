from models import *

Class classifier:
	def __init__(self, net):
		self.net=net

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
		classes['extended_free_choice'] = is_extened_free_choice(places)
		classes['extended_simple'] = is_extended_simple(places)
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
		for combined_places in itertools.combinations(places,2):
			place1 = combined_places[0]
			place2 = combined_places[1]
			if(!(place1[1].isdisjoined(place2[1]) or place1[1]== place2[1]))
				return False
		return True

	def is_extended_simple_choice(self,places):
		for combined_places in itertools.combinations(places,2):
			place1 = combined_places[0]
			place2 = combined_places[1]
			if(!(place1[1].isdisjoined(place2[1]) or place1[1]<=place2[1] or place2[1]<=place1[1])):
				return False
		return True
