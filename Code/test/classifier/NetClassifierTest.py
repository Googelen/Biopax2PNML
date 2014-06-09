import unittest
from models import PetriNet
from classifier import NetClassifier


class EmptyNetTestCase(unittest.TestCase):
	def setUp(self):
		net = PetriNet("This petri net is empty")
		c = NetClassifier(net)
		self.classes = c.classify()

	def test_empty_net_should_be_sm(self):
		self.assertTrue(self.classes['state_machine'])

	def test_empty_net_should_be_sg(self):
		self.assertTrue(self.classes['synchronisation_graph'])


class extended_simple_and_extended_free_choice_testcase(unittest.TestCase):
	def setUp(self):
		net = PetriNet("This petri net is empty")
		c = NetClassifier(net)

		# This should all be defined in net (above) instead of as dicts.

		# test_places1 = {
		# 'test1': (None,set(['0','1','2'])),
		# 'test2': (None,set(['3','4','5'])),
		# 'test3':(None,set(['1','2','0']))
		#
		# }
		#
		# test_places2 = {
		# 'test1': (None,set(['0','1','2'])),
		# 'test2': (None,set(['3','4','5'])),
		# 'test3':(None,set(['1','2']))
		#
		# }
		# test_places3 = {
		# 'test1': (None,set(['0','1','2'])),
		# 'test2': (None,set(['3','4','5'])),
		# 'test3':(None,set(['1','2','3']))
		#
		# }

	def test_extended_simple(self):
		# These should not call c.is_extended_...
		# Rather call c.classify and compare the classes in the resulting dict.
		self.assertEqual(True,c.is_extended_simple_choice(test_places1))
		self.assertEqual(True,c.is_extended_simple_choice(test_places2))
		self.assertEqual(False,c.is_extended_simple_choice(test_places3))
		
	def test_extended_free_choice(self):
		# These should not call c.is_extended_...
		# Rather call c.classify and compare the classes in the resulting dict.
		self.assertEqual(True,c.is_extended_free_choice(test_places1))
		self.assertEqual(False, c.is_extended_free_choice(test_places2))
		self.assertEqual(False,c.is_extended_free_choice(test_places3))
		

if __name__ == '__main__':
	unittest.main()
