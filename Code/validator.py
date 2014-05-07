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
	def checkCycles(self):
		for place in self.net.places:
			cycleRecursion(place,[]) # does weird stuff here
		
	#maybe better name
	def cycleRecursion(self,placeIn,placesIn):
		placesIn.append(placeIn)
		descendants = getDescendants(placeIn)
		if placeIn.id in descendants:
			#cycle found
			for place in placesIn:
				print("Place id in cycle:")
				print(place.id)
				self.numberOfCycles = self.numberOfCycles + 1
		elif descendants==[]:
			#no cycle found
			return
		else:
			#make sure every split it searched
			for place in descendants:
				cycleRecursion(place,placesIn)
		
	
	def getDescendants(self,placeIn):
		descendants=[]
		transitionPrevious
		for arc in self.net.arcs:
			if isintance(arc.source,Place):
				if placeIn.id==arc.source.id:
					transitionPrevious = arc.target
		for arc in self.net.arcs:
			if isinstance(arc.source,Transition):
				if transitionPrevious==arc.source:
					descendants.append(arc.target.id)
		return descendants
