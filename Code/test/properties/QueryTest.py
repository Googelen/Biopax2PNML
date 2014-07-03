class Query_Test:
	def __init__(self):
		self.test_query("WP78_70014.owl")
		return

	def test_query(self,inputfile):
		query="""
			PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
			SELECT  ?left ?displayNameLeft ?right ?displayNameRight ?type ?classs
			WHERE {
				?classs bp:left ?left . 
                ?classs bp:right ?right .
                ?left bp:displayName ?displayNameLeft . 
                ?right bp:displayName ?displayNameRight
                
			}
		"""
		
		result = self.test_query(inputfile,query)

		print(len(result))
		for x in result:
			print(x.left)
			print(x.displayNameLeft)
			print(x.right)
			print(x.displayNameRight)
			print("")
			
	def test_query(self, inputfile,query):
		graph = rdflib.Graph()
		graph.parse(inputfile)
		return graph.query(query)
		
test = Query_Test()
