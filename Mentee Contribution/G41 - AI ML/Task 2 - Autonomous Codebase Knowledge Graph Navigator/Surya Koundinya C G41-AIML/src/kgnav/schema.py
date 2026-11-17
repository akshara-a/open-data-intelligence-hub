"""Graph schema conventions. Edit this file to adapt the agent to YOUR graph.

Edge direction convention:  (A)-[:REL]->(B)  means  "A depends on B"
for every relationship in DEPENDENCY_RELS. A change/removal of B can therefore
break A, so blast radius = reverse reachability from the target.
"""

# Relationships where source DEPENDS ON target (used for blast radius)
DEPENDENCY_RELS = ["CALLS", "IMPLEMENTED_BY", "CALLS_ROUTE", "CONSUMES", "READS_FROM", "WRITES_TO"]

# Structural ownership (service -> its modules / routes)
OWNERSHIP_RELS = ["CONTAINS", "EXPOSES"]

# Coarse service-to-service dependency (used for cycles / coupling / SPOF)
SERVICE_REL = "DEPENDS_ON"

SERVICE_LABEL = "Service"
MODULE_LABEL = "Module"
ROUTE_LABEL = "APIRoute"
DB_LABEL = "Database"
FRONTEND_LABEL = "FrontendComponent"

SCHEMA_GUIDE = """\
Node labels (all have a unique `name` property):
  Service(name, team, language, tier, deprecated?)   - a microservice
  Module(name, deprecated?)                          - code module inside a service
  APIRoute(name, method, path)                       - e.g. name='POST /orders'
  Database(name)                                     - datastore
  FrontendComponent(name)                            - UI component / app screen
Relationships (A)-[r]->(B) means A depends on B unless noted:
  (Service)-[:CONTAINS]->(Module)        (Service)-[:EXPOSES]->(APIRoute)   [ownership]
  (APIRoute)-[:IMPLEMENTED_BY]->(Module)
  (Module)-[:CALLS]->(Module)            (Module)-[:CALLS_ROUTE]->(APIRoute)
  (FrontendComponent)-[:CONSUMES]->(APIRoute)
  (Module)-[:READS_FROM|WRITES_TO]->(Database)
  (Service)-[:DEPENDS_ON]->(Service)     [coarse, derived service-level coupling]
"""
