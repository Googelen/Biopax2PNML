import rdflib
from rdflib.resource import Resource


class QueryTest:
	def __init__(self):

		self.graph = rdflib.Graph()
		self.graph.parse("../../WP78_70014.owl")
		self.graph.parse("http://www.biopax.org/release/biopax-level3.owl", format='application/rdf+xml')
		self.test_query()


	def test_query(self):
		conversion_query = """
			PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
			SELECT ?interaction ?relation ?participant ?participantName ?direction
			WHERE {
				?conversionClass rdfs:subClassOf+ bp:Conversion.
				?participantRelation rdfs:subPropertyOf bp:participant.

				?interaction
					a ?conversionClass;
					?relation ?participant.

				OPTIONAL { ?participant bp:displayName ?participantName }
				OPTIONAL { ?interaction bp:conversionDirection ?direction }
			}
		"""
		control_query = """
			PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
			SELECT ?interaction ?relation ?participant ?participantName ?direction ?controlType
			WHERE {
				?controlClass rdfs:subClassOf+ bp:Control.
				?relation rdfs:subPropertyOf bp:participant.

				?interaction
					a ?controlClass;
					?relation ?participant.

				OPTIONAL { ?participant bp:displayName ?participantName }
				OPTIONAL { ?interaction bp:catalysisDirection ?direction }
				OPTIONAL { ?interaction bp:controlType ?controlType }
			}
		"""

		query = """
			PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
			SELECT ?property
			WHERE {
				?property rdfs:subPropertyOf bp:participant.
			}
		"""

		result = self.graph.query(query)

		print(len(result))

		for x in result:
			for prop in x:
				print(Resource(self.graph, prop))
			print("")

		print(len(result))

		return result
		
test = QueryTest()
