import xml.etree.cElementTree as ET
ET.register_namespace('pnml','http://www.pnml.org/version-2009/grammar/pnml')

class Writer:
	def __init__(self, net):
		self.elementcount = 0
		self.net = net

	#Return a new identifier
	def uniqueId(self, prefix='id'):
		self.elementcount += 1
		return prefix + str(self.elementcount)

	def writeName(self, parent, nameValue):
		name = ET.SubElement(parent, 'name')
		nameText = ET.SubElement(name, 'text')
		nameText.text = nameValue

	def writePlace(self, parent, place):
		if not place.id:
			place.id = self.uniqueId('p') 
		placeElement = ET.SubElement(parent, 'place', {
			'id': place.id
			})
		self.writeName(placeElement, place.description)

	def writeTransition(self, parent, transition):
		if not transition.id:
			transition.id = self.uniqueId('t')
		transitionElement = ET.SubElement(parent, 'transition', {
			'id': transition.id
			})

	def writeArc(self, parent, arc):
		uid = self.uniqueId('a')
		arcElement = ET.SubElement(parent, 'arc',{
			'id': uid,
			'source': arc.source.id,
			'target': arc.target.id
			})
		return uid

	def prepare(self):
		self.root = ET.Element('pnml');	
		net = ET.SubElement(self.root, 'net', {
			'type': 'http://www.pnml.org/version-2009/grammar/ptnet',
			'id': self.uniqueId('id-')
			})

		page = ET.SubElement(net, 'page', {
			'id': 'top-level'			
			})
		return page

	def write(self, location):
		page = self.prepare()

		self.writeName(page, self.net.description)

		for place in self.net.places:
			self.writePlace(page, self.net.places[place])

		for transition in self.net.transitions:
			self.writeTransition(page, self.net.transitions[transition])

		for arc in self.net.arcs:
			self.writeArc(page, arc)

		indent(self.root)
		tree = ET.ElementTree(self.root)
		tree.write(location)


def indent(elem, level=0):
	"""in-place prettyprint formatter

	Prettyprint from http://effbot.org/zone/element-lib.htm#prettyprint

	:param elem: Element to format. Start with root element.
	:param level: Indention level. Is recursively used to increase indention.
	"""
	i = "\n" + level*"  "
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "  "
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			indent(elem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i