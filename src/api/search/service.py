import whoosh.index as index
from whoosh.qparser import QueryParser

medicines_index = index.open_dir("api/search/indexes/medicines_index")
medicines_searcher = medicines_index.searcher()
medicines_query_parser = QueryParser("description", schema=medicines_index.schema)


async def medicine_search(query: str) -> list[dict]:
    """
    Searches for medicines based on a query.

    Args:
        query (str): The search query.

    Returns:
        list[dict]: A list of dictionaries containing the code and description of the medicines.
    """

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


async def symptom_search(query: str) -> list[dict]:
    """
    Searches for symptoms based on a query.

    Args:
        query (str): The search query.

    Returns:
        list[dict]: A list of dictionaries containing the code and description of the symptoms.
    """

    results = symptoms_searcher.search(symptoms_query_parser.parse(f"{query.strip()}*"))
    return [
        {"code": result["code"], "description": result["description"]}
        for result in results
    ]


diseases_index = index.open_dir("api/search/indexes/diseases_index")
diseases_searcher = diseases_index.searcher()
diseases_query_parser = QueryParser("description", schema=diseases_index.schema)


async def disease_search(query: str) -> list[dict]:
    """
    Searches for diseases based on a query.

    Args:
        query (str): The search query.

    Returns:
        list[dict]: A list of dictionaries containing the code and description of the diseases.
    """

    results = diseases_searcher.search(diseases_query_parser.parse(f"{query.strip()}*"))
    return [
        {"code": result["code"], "description": result["description"]}
        for result in results
    ]
