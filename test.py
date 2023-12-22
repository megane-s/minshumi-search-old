

from whoosh.index import create_in, FileIndex
from whoosh.fields import *
import os, os.path as path
from whoosh import scoring
from whoosh.analysis import NgramAnalyzer, StopFilter

# setup index

def stopWordsFilter():
  words = []
  with open("./stopwords.txt", "r", encoding="utf-8") as f:
    line = f.readline()
    words.append(line)
  return StopFilter(words)

def get_schema():
  schema = Schema(
    title=TEXT(
      stored=True, 
      analyzer=NgramAnalyzer(minsize=1, maxsize=10),
    ),
    path=ID(stored=True), 
    content=TEXT(
      analyzer=NgramAnalyzer(minsize=1, maxsize=10) | stopWordsFilter(),
    ),
  )
  return schema

def init_index(index_dir:str):
  if not path.exists(index_dir):
    os.mkdir(index_dir)

def get_index():
  INDEX_DIR = "index_dir"

  init_index(INDEX_DIR)
  return create_in(INDEX_DIR, get_schema())

ix = get_index()

def write_data(ix: FileIndex):
  writer = ix.writer()

  text = u"あいうえお" * 3
  for i in range(len(text)):
    writer.add_document(
      title=text[0:i],
      path=u"/b",
      content=text[0:i]*3,
    )
  writer.commit()
write_data(ix)

# search

from whoosh.qparser import QueryParser

from time import time

with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
  query_text = input("検索ワードを入力:")
  start = time()
  query = QueryParser("title", ix.schema).parse(query_text)
  results = searcher.search(query, limit=20)
  result_time = time() - start
  print("search result", len(results), results, "in", result_time)
  for i, result in enumerate(results):
    print(" ", i,":", result)



