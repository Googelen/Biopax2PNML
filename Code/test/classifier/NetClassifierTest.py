import unittest
from models import *
from classifier import NetClassifier


class BasicNetTestCase(unittest.TestCase):

	def test_empty_net(self):

		c = NetClassifier(PetriNet("This petri net is empty")).classifications
		self.assertTrue(c['state_machine'])
		self.assertTrue(c['synchronisation_graph'])

	def test_basic_nets(self):
		nets = [PetriNet("Petri net " + str(i)) for i in range(3)]

		places = [Place("i/" + str(i), "place" + str(i)) for i in range(4)]
		transitions = [Transition() for i in range(0,3)]

		for net in nets:
			net.places = places
			net.transitions = transitions

		nets[0].newArc(Arc(places[0], transitions[0]))
		nets[0].newArc(Arc(transitions[0], places[1]))
		nets[0].newArc(Arc(places[1], transitions[1]))
		nets[0].newArc(Arc(transitions[1], places[2]))
		nets[0].newArc(Arc(places[2], transitions[2]))
		nets[0].newArc(Arc(transitions[2], places[3]))

		nets[1].newArc(Arc(places[0], transitions[0]))
		nets[1].newArc(Arc(transitions[0], places[1]))
		nets[1].newArc(Arc(places[1], transitions[1]))
		nets[1].newArc(Arc(transitions[0], places[2]))
		nets[1].newArc(Arc(places[2], transitions[2]))
		nets[1].newArc(Arc(transitions[1], places[3]))
		nets[1].newArc(Arc(transitions[2], places[3]))

		nets[2].newArc(Arc(places[0], transitions[0]))
		nets[2].newArc(Arc(transitions[0], places[1]))
		nets[2].newArc(Arc(places[1], transitions[1]))
		nets[2].newArc(Arc(transitions[0], places[2]))
		nets[2].newArc(Arc(transitions[1], places[3]))


		c = NetClassifier(nets[0]).classifications
		d = NetClassifier(nets[1]).classifications
		e = NetClassifier(nets[2]).classifications

		self.assertFalse(c['state_machine'])
		self.assertFalse(c['synchronisation_graph'])
		self.assertTrue(c['extended_free_choice'])
		self.assertTrue(c['extended_simple'])

		self.assertFalse(d['state_machine'])
		self.assertFalse(d['synchronisation_graph'])
		self.assertTrue(d['extended_free_choice'])
		self.assertTrue(d['extended_simple'])

		self.assertFalse(e['state_machine'])
		self.assertFalse(e['synchronisation_graph'])
		self.assertTrue(e['extended_free_choice'])
		self.assertTrue(e['extended_simple'])
		

if __name__ == '__main__':
	unittest.main()
