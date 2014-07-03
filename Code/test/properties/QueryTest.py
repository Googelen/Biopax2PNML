import rdflib


class QueryTest:
	def __init__(self):

		self.graph = rdflib.Graph()
		self.graph.parse("../../WP78_70014.owl")
		self.graph.parse("http://www.biopax.org/release/biopax-level3.owl", format='application/rdf+xml')
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
		#I also made a query for the other part
		#or did you want to merge these 2?
		query = """ 
			PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
			SELECT  ?class ?control ?controller ?controlled ?direction
			WHERE {
				?class rdfs:subClassOf+ bp:Control.
				?control a ?class.
				{
					?control bp:controller ?controller .
					?control bp:controlled ?controlled
				} 
				OPTIONAL { ?control bp:catalysisDirection ?direction }
			}

		"""

		result = self.graph.query(query)

		print(len(result))

		for x in result:
			for prop in x:
				print(prop)
			print("")

		
test = QueryTest()
