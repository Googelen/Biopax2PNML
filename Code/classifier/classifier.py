from models import *


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