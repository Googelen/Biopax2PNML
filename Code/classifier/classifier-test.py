import classifier
net=None
classifier = classifier.NetClassifier(net)

test_places = {
	'test1': (None,set(['0','1','2'])),
	'test2': (None,set(['3','4','5'])),
	'test3':(None,set(['1','2','0']))

}
#should return true
print(classifier.is_extended_free_choice(test_places))
#should return true
print(classifier.is_extended_simple_choice(test_places))

test_places = {
	'test1': (None,set(['0','1','2'])),
	'test2': (None,set(['3','4','5'])),
	'test3':(None,set(['1','2']))

}
#should return false
print(classifier.is_extended_free_choice(test_places))
#should return true
print(classifier.is_extended_simple_choice(test_places))

test_places = {
	'test1': (None,set(['0','1','2'])),
	'test2': (None,set(['3','4','5'])),
	'test3':(None,set(['1','2','3']))

}
#should return false
print(classifier.is_extended_free_choice(test_places))
#should return false
print(classifier.is_extended_simple_choice(test_places))
