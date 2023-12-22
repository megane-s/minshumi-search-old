import os, os.path as path
from whoosh.index import create_in, FileIndex

from search_art.schema import get_schema
import shutil

from whoosh.qparser import QueryParser
from time import time
from whoosh import scoring

from search_art.shared_index import load_art_shared_search_index

INDEX_DIR = "indices/art_index"
_index :FileIndex | None = None

def init_local_index(index_dir:str=INDEX_DIR):
  print(":: init_local_index")
  if path.exists(index_dir):
    shutil.rmtree(index_dir)
  os.makedirs(index_dir)

  global _index
  _index = create_in(INDEX_DIR, get_schema())
  load_art_shared_search_index()

def write_test_data(ix: FileIndex):
  writer = ix.writer()

  writer.add_document(
    artId=u"test-art-1",
    title="キメツのやばい",
    description="キメツのやばい" * 10,
    tags=["アクション", "アニメ", "アニメ映画", "バトル", "マンガ", "少年マンガ", "週刊少年ジャンプ"],
  )
  writer.add_document(
    artId=u"test-art-2",
    title="ジュルジュル回線",
    description="ジュルジュル回線" * 10,
    tags=["アニメ", "アニメ映画", "バトル", "マンガ", "少年マンガ"],
  )
  writer.add_document(
    artId=u"/test-art-3",
    title="きっとマヨネーズでいいのに。",
    description="きっとマヨネーズでいいのに。" * 10,
    tags=["J-POP", "アーティスト", "ジャズ", "ロック"],
  )
  writer.add_document(
    artId=u"/test-art-4",
    title="俺の名は。",
    description="俺の名は。" * 10,
    tags=["RADWIMPS", "アニメ映画", "古海誠", "映画"],
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
