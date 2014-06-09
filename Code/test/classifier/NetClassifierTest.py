import unittest
from models import PetriNet
from classifier import NetClassifier


class EmptyNetTestCase(unittest.TestCase):
	def setUp(self):
		net = PetriNet("This petri net is empty")
		c = NetClassifier(net)
		self.classes = c.classifications

	def test_empty_net_should_be_sm(self):
		self.assertTrue(self.classes['state_machine'])

	def test_empty_net_should_be_sg(self):
		self.assertTrue(self.classes['synchronisation_graph'])


class extended_simple_and_extended_free_choice_testcase(unittest.TestCase):
	def setUp(self):
		net = PetriNet("This petri net is empty")
		net1 = PetriNet("This petri net is empty")
		net2= PetriNet("This petri net is empty")
		places=[]
		for i in range(0,4):
			places.append(Place("i/"+str(i),"place"+str(i)))
		transitions = []
		for i in range(0,3):
			transitions.append(Transition())
		
		arcs = []
		arcs.append(Arc(places[0],transitions[0]))
		arcs.append(Arc(transitions[0],places[1]))
		arcs.append(Arc(places[1],transitions[1]))
		arcs.append(Arc(transitions[1],places[2]))
		arcs.append(Arc(places[2],transitions[2]))
		arcs.append(Arc(transitions[2],places[3]))

		arcs1=[]
		arcs1.append(Arc(places[0],transitions[0]))
		arcs1.append(Arc(transitions[0],places[1]))
		arcs1.append(Arc(places[1],transitions[1]))
		arcs1.append(Arc(transitions[0],places[2]))
		arcs1.append(Arc(places[2],transitions[2]))
		arcs1.append(Arc(transitions[1],places[3]))
		arcs1.append(Arc(transitions[1],places[3]))

		arcs2=[]
		arcs2.append(Arc(places[0],transitions[0]))
		arcs2.append(Arc(transitions[0],places[1]))
		arcs2.append(Arc(places[1],transitions[1]))
		arcs2.append(Arc(transitions[0],places[2]))
		arcs2.append(Arc(transitions[1],places[3]))

		for place in places:
			net.newPlace(place)
			net1.newPlace(place)
			net2.newPlace(place)
		for transition in transitions:
			net.newTransition(transition)
			net1.newTransition(transition)
			net2.newTransition(transition)
		for arc in arcs:
			net.newArc(arc)
		for arc in arcs1:
			net1.newArc(arc)
		for arc in arcs2:
			net2.newArc(arc)

		c = NetClassifier(net)
		self.c = c.classify()
		d = NetClassifier(net1)
		self.d = d.classify()
		e = NetClassifier(net2)
		self.e = e.classify()

		
	def test_extended_simple(self):
		self.assertEqual(True,self.c['exteded_simple'])
		self.assertEqual(False,self.d['exteded_simple'])
		self.assertEqual(False,self.e['exteded_simple'])
		
	def test_extended_free_choice(self):
		self.assertEqual(False,self.c['exteded_free_choice'])
		self.assertEqual(False,self.d['exteded_free_choice'])
		self.assertEqual(False,self.e['exteded_free_choice'])
		

if __name__ == '__main__':
	unittest.main()
