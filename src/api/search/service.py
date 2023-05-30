import whoosh.index as index
from whoosh.qparser import QueryParser

medicines_index = index.open_dir("api/search/indexes/medicines_index")
medicines_searcher = medicines_index.searcher()
medicines_query_parser = QueryParser("description", schema=medicines_index.schema)


async def medicine_search(query):
    results = medicines_searcher.search(
        medicines_query_parser.parse(f"{query.strip()}*")
    )
    return [
        {"code": result["code"], "description": result["description"]}
        for result in results
    ]


symptoms_index = index.open_dir("api/search/indexes/symptoms_index")
symptoms_searcher = symptoms_index.searcher()
symptoms_query_parser = QueryParser("description", schema=symptoms_index.schema)


async def symptom_search(query):
    results = symptoms_searcher.search(symptoms_query_parser.parse(f"{query.strip()}*"))
    return [
        {"code": result["code"], "description": result["description"]}
        for result in results
    ]
