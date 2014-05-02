from models import *

class Validator:
	#check if there are places with no ingoing arcs (feedback? how?)
	def __init__(self, net):
		self.net=net
		self.startingPlaces = []
		self.endingPlaces = []
		
	def checkArcs(self):
		for place in self.net.places:
			setStart=True
			setEnd=True
			for arc in self.net.arcs:
				#check for starting places
				if isinstance(arc.target,Place):
					if place.id==arc.target.id: #this place has an incoming arc
						setStart=False
				#check for ending places
				if isinstance(arc.source,Place):
					if place.id==arc.source.id: #this place has an outgoing arc
						setEnd=False
			if setStart:	
				self.startingPlaces.append(place.id)
			if setEnd:
				self.endingPlaces.append(place.id)
		print("The starting places:")
		print(self.startingPlaces)
		print("The ending places:")
		print(self.endingPlaces)
	#def checkEndingArcs():
	#check for cycles(how?)
	#def checkForCycles():
