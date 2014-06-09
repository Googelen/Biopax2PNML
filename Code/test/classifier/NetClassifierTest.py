import unittest
import classifier

class MyTestCase(unittest.TestCase):
	def test_something(self):
		self.assertEqual(True, False)


class extended_simple_and_extended_free_choice_testcase(unittest.TestCase):
	def __init__(self):
		net=None
		classifier = classifier.NetClassifier(net)
		test_places1 = {
		'test1': (None,set(['0','1','2'])),
		'test2': (None,set(['3','4','5'])),
		'test3':(None,set(['1','2','0']))
	
		}
		
		test_places2 = {
		'test1': (None,set(['0','1','2'])),
		'test2': (None,set(['3','4','5'])),
		'test3':(None,set(['1','2']))
	
		}
		test_places3 = {
		'test1': (None,set(['0','1','2'])),
		'test2': (None,set(['3','4','5'])),
		'test3':(None,set(['1','2','3']))
	
		}
		self.test_extended_simple()
		self.test_extended_free_choice()
		
	def test_extended_simple(self):
		self.assertEqual(True,classifier.is_extended_simple_choice(test_places1))
		self.assertEqual(True,classifier.is_extended_simple_choice(test_places2))
		self.assertEqual(False,classifier.is_extended_simple_choice(test_places3))
		
	def test_extended_free_choice(self):
		self.assertEqual(True,classifier.is_extended_free_choice(test_places1))
		self.assertEqual(False, classifier.is_extended_free_choice(test_places2))
		self.assertEqual(False,classifier.is_extended_free_choice(test_places3))
if __name__ == '__main__':
	unittest.main()
