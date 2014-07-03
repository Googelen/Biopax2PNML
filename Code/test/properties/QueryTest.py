import rdflib


class QueryTest:
	def __init__(self):

		self.graph = rdflib.Graph()
		self.graph.parse("../../WP78_70014.owl")
		self.graph.parse("../../biopax-level3.owl")
		self.test_query()
		return

	def test_query(self):
		query = """
			PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
			SELECT  ?class ?conversion ?child ?childName ?direction
			WHERE {
				?class rdfs:subClassOf+ bp:Conversion.
				?conversion a ?class.
				{
					?conversion bp:left ?child.
					?child bp:displayName ?childName
				} UNION {
					?conversion bp:right ?child.
					?child bp:displayName ?childName
				}
				OPTIONAL { ?conversion bp:conversionDirection ?direction }
			}
		"""

		result = self.graph.query(query)

		print(len(result))

		for x in result:
			for prop in x:
				print(prop)
			print("")

		
test = QueryTest()
