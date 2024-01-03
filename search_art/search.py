
from search_art.local_index import get_local_index
from whoosh.qparser import QueryParser
from whoosh import scoring
from dataclasses import dataclass


@dataclass
class Art:
    art_id: str
    title: str


def search(q: str):
    search_index = get_local_index()
    with search_index.searcher(weighting=scoring.TF_IDF()) as searcher:
        query = QueryParser("title", search_index.schema).parse(q)
        results = searcher.search(query, limit=20)
        return [
            Art(
                art_id=res.get("art_id"),
                title=res.get("title"),
            )
            for res in results
        ]
