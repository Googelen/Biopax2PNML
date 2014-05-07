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
	#recursion, select a place and send it to the function. Send also all previous places.
	#check if the descendants are in the previous places, if so, cycle found.
	def getDescendants(self,placeIn):
		descendants=[]
		transitionPrevious=0
		for arc in self.net.arcs:
			if isinstance(arc.source,Place):
				print(placeIn)
				if placeIn.id==arc.source.id:
					transitionPrevious = arc.target
		for arc in self.net.arcs:
			if isinstance(arc.source,Transition):
				if transitionPrevious==arc.source:
					descendants.append(arc.target)
		return descendants
	
	def cycleRecursion(self,placeIn,placesIn):
		placesIn.append(placeIn)
		descendants = self.getDescendants(placeIn)
		if placeIn.id in descendants:
			#cycle found
			for place in placesIn:
				self.numberOfCycles = self.numberOfCycles + 1
		elif descendants==[]:
			#no cycle found
			return
		else:
			#make sure every split it searched
			for place in descendants:
				self. cycleRecursion(place,placesIn)
	def checkCycles(self):
		for place in self.net.places:
			placesIn=[]
			self.cycleRecursion(place,placesIn)
		print("Number Of Cycles:")
		print(self.numberOfCycles)
	#maybe better name
