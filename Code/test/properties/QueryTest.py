import rdflib


class QueryTest:
	def __init__(self):

		self.graph = rdflib.Graph()
		self.graph.parse("../../WP78_70014.owl")
		self.graph.parse("http://www.biopax.org/release/biopax-level3.owl", format='application/rdf+xml')
		self.test_query()
		return

	def test_query(self):
		conversion_query = """
			PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
			SELECT  ?class ?interaction ?hasParticipant ?participant ?displayName ?direction
			WHERE {
				?class rdfs:subClassOf+ bp:Conversion.
				?hasParticipant rdfs:subPropertyOf bp:participant.

				?interaction
					a ?class;
					?hasParticipant ?participant.

				OPTIONAL {
					?child bp:displayName ?childName.
					?interaction bp:conversionDirection ?direction.
				}
			}
		"""
		control_query = """
			PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
			SELECT  ?class ?interaction ?hasParticipant ?participant ?displayName ?direction ?controlType
			WHERE {
				?class rdfs:subClassOf+ bp:Control.
				?hasParticipant rdfs:subPropertyOf bp:participant.

				?interaction
					a ?class;
					?hasParticipant ?participant.

				OPTIONAL {
					?child bp:displayName ?childName.
					?interaction bp:catalysisdirection ?direction.
					?interaction bp:controlType ?controlType.
				}
			}
		"""

		result = self.graph.query(control_query)

		print(len(result))

		for x in result:
			for prop in x:
				print(prop)
			print("")

		print(len(result))
		
test = QueryTest()
