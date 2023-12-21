from functools import cache
import os, os.path as path
from whoosh.index import create_in, FileIndex

from search_art.schema import get_schema
import shutil

from whoosh.qparser import QueryParser
from time import time
from whoosh import scoring

INDEX_DIR = "indices/art_index"
_index :FileIndex | None = None

def init_local_index(index_dir:str=INDEX_DIR):
  print(":: init_local_index")
  if path.exists(index_dir):
    shutil.rmtree(index_dir)
  os.mkdir(index_dir)

  global _index
  _index = create_in(INDEX_DIR, get_schema())
  write_test_data(_index)

def write_test_data(ix: FileIndex):
  writer = ix.writer()

  text = u"あいうえお" * 3
  for i in range(len(text)):
    writer.add_document(
      artId=u"/b",
      title=text[0:i],
      description=text[0:i]*3,
      tags=[],
    )
  writer.commit()

def get_index():
  global _index
  if _index is None:
    init_local_index()
  return _index

def search(q:str):
  search_index = get_index()
  with search_index.searcher(weighting=scoring.TF_IDF()) as searcher:
    start = time()
    query = QueryParser("title", search_index.schema).parse(q)
    results = searcher.search(query, limit=20)
    return [res.get("title") for res in results]
