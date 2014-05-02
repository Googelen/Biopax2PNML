import biopax
import pnml
from models import *
import validator

class Convertor:
	def __init__(self, inputfile, outputfile):
		reader = biopax.Reader()
		net = reader.read(inputfile)
		validatorThingy = validator.Validator(net)
		validatorThingy.checkArcs()
		writer = pnml.Writer(net)
		writer.write(outputfile)
