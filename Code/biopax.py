import rdflib
from rdflib.namespace import Namespace
from models import PetriNet
from converter.converter import BiopaxConverter

BP = Namespace('http://www.biopax.org/release/biopax-level3.owl')


class Reader:
	def __init__(self):
		self.net = PetriNet('')

	def read(self, inputfile):
		self.net.describtion = inputfile
		graph = rdflib.Graph()
		graph.parse(inputfile)
		graph.parse('biopax-level3.owl')

		self.convert(graph)
		return self.net

	def convert(self, graph):
		for Converter in sorted(BiopaxConverter.__subclasses__(), key=lambda t: t.order):
			if Converter.order > -1:
				c = Converter(graph, self.net)
				c.convert()

	def readPlaces(self):
		return self.net.places

	def readTransitions(self):
		return self.net.transitions

	def readArcs(self):
		return self.net.arcs