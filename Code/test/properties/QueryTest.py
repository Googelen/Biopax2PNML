import rdflib
from rdflib import plugin

class Query_Test:
	def __init__(self):
		self.test_query("WP78_70014.owl")
		return

	def test_query(self,inputfile):
		query="""
			 PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        SELECT  ?about ?child ?displayName
                        WHERE {
                            {
                                SELECT DISTINCT ?instance ?about 
                                {
                                    ?class rdfs:subClassOf* bp:Conversion.
                                    ?instance a ?class;
                                              rdf:about ?about
                                }
                            }
                            
                            OPTIONAL {
                                ?instance bp:left/bp:right ?child.
                                ?child bp:displayName ?displayName
                            }
                        }
		"""
		

		query="""
			PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
			SELECT  ?subclass
			WHERE {
				 bp:BiochemicalReaction rdfs:subClassOf ?subclass
			}



		"""

		result = self.execute_query(inputfile,query)

		print(len(result))
		for x in result:
			print(x.subclass)
			#print(x.child)
			#print(x.displayName)
			print("")
			
	def execute_query(self, inputfile,query):
		graph = rdflib.Graph()
		graph.parse(inputfile)
		return graph.query(query)
		
test = Query_Test()
