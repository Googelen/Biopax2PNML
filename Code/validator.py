from models import *
import classifier
import itertools

class Validator:
	#check if there are places with no ingoing arcs (feedback? how?)
	def __init__(self, net):
		self.net=net
		self.startingPlaces = []
		self.endingPlaces = []
		self.number_of_cycles=0
		self.cycles=[]
		self.type=""
		self.number_of_components=0
		self.deadlock_places = {}
		self.trap_places = {}
		self.validate()
		
	def validate(self):
		self.checkArcs()
		self.checkCycles()
		self.countComponents()
		self.whatGraph()
		#this is very ugly, maybe your logger?
		print("Starting places")
		print(self.startingPlaces)
		print("Ending places")
		print(self.endingPlaces)
		print("Number of cycles")
		print(self.number_of_cycles)
		print("Type of graph")
		print(self.type)
		print("Number of Components")
		print(self.number_of_components)
		
	def find_deadlocks(self):
		classify = classifier.NetClassifier(self.net)
		places = classify.get_pre_post_places()
		(deadlock_places,trap_places) = get_deadlock_and_trap(places)

		if(not(len(deadlock_places) is 0)):
			self.deadlock_places = deadlock_places
			print("deadlocks found")
		if(not(len(trap_places) is 0)):
			self.trap_places = trap_places
			print("trap found")

	def get_deadlock_and_trap(self, places):
		places_in_deadlock ={}
		places_in_trap = {}
		for i in range(1,len(places)+1):
			for place_name in itertools.combinations(places,1):
				places_to_check = {}
				for name in place_name:
					places_to_check.union(places[name])
				post_places = {}
				pre_places = {}

				for j in range(0,len(place_name)):
					post_places.union(places_to_append[j][1])
					pre_places.union(places_to_append[j][1])

				if(pre_places<=post_places):
					places_in_deadlock.union(places_to_check)
				if(post_places<=pre_places):
					places_in_trap.union(places_to_check)
		return (places_in_deadlock, places_in_trap)
	
	
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
		
	def countComponents(self):
		#select starting place
		remaining_places = self.net.places
		while remaining_places:
			#get a place
			place=self.getFirst(remaining_places)
			component = self.getComponent(place)
			remaining_places = set(remaining_places)-set(component)
			self.number_of_components=self.number_of_components+1
	
	def getFirst(self,iterable, default=None):
		if iterable:
			for item in iterable:
				return item
		return default
	
	def getComponent(self,placeIn):
		previous_neighbours=[]
		neighbours=[placeIn]
		# expand the neighbours
		while(neighbours!=previous_neighbours):
			temp_neighbours=neighbours
			parents=[]
			children=[]
			#get children and parents
			for place in neighbours:
				if place not in previous_neighbours:
					parents.extend(self.getParents(place))
					children.extend(self.getChildren(place))
			#add them if they do not yet exist		
			for parent in parents:
				if parent not in neighbours:
					neighbours.append(parent)
			for child in children:
				if child not in neighbours:
					neighbours.append(child)
			previous_neighbours=temp_neighbours #for less loops
			
		return neighbours
	
	def getParents(self,placeIn):
		parents=[]
		transitionPrevious=[]
		for arc in self.net.arcs:
			if isinstance(arc.target, Place):
				if placeIn.id==arc.target.id:
					transitionPrevious.append(arc.source)
		
		for arc in self.net.arcs:
			if isinstance(arc.target,Transition):
				if arc.target in transitionPrevious:
					parents.append(arc.source)
		return parents
		
	
	#recursion, select a place and send it to the function. Send also all previous places.
	#check if the descendants are in the previous places, if so, cycle found.
	
	def getChildren(self,placeIn):
		children=[]
		transitionNext=[]
		for arc in self.net.arcs:
			if isinstance(arc.source,Place):
				if placeIn.id==arc.source.id:
					transitionNext.append(arc.target)
		for arc in self.net.arcs:
			if isinstance(arc.source,Transition):
				if arc.source in transitionNext:
					children.append(arc.target)
		return children
	
	def add_to_cycles(self,placesIn):
		duplicate_found=False
		for cycle in self.cycles:
			if(set(cycle)==set(placesIn)):
				duplicate_found=True
		
		if(not duplicate_found):
			self.cycles.append(placesIn)
	
	
	def cycleRecursion(self,placeIn,placesIn):
		placesIn.append(placeIn)
		children = self.getChildren(placeIn)
		if placeIn.id in children:
			#cycle found
			self.number_of_cycles = self.number_of_cycles + 1
			placesIn.pop() #the original place was added, remove this one
			add_to_cycles(placesIn)
			
		elif children==[]:
			#no cycle found
			return
		else:
			#make sure every split it searched
			for place in children:
				self. cycleRecursion(place,placesIn)
				
				
	def checkCycles(self):
		for place in self.net.places:
			placesIn=[]
			self.cycleRecursion(place,placesIn)
	#maybe better name
	
	#call this at the end
	def whatGraph(self):
		#every place has 1 arc exept for 1
		if (len(self.net.arcs)-1==len(self.net.places)):
			self.type="Linear"
		#there are no starting and ending places
		elif (len(self.startingPlaces)==0 and len(self.endingPlaces)==0):
		#elif(not structural.has_boundary_nodes)
			self.type="Cyclic"
		#there are no cycles
		elif self.number_of_cycles==0:
			self.type="Branch"
		else:
			self.type="Undefined"
