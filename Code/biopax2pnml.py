import biopax
import pnml
from models import *
import validator
import classifier

class Convertor:
	def __init__(self, inputfile, outputfile):
		reader = biopax.Reader()
		net = reader.read(inputfile)
		validatorThingy = validator.Validator(net)
		validatorThingy.checkArcs()
		classify = classifier.Classifier(net)
		classify.classify()
		writer = pnml.Writer(net)
		writer.write(outputfile)
