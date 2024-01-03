import os
import os.path as path
from typing import cast
from whoosh.index import create_in, FileIndex

from search_art.schema import get_schema
import shutil
import time
from faker import Faker
from random import random

INDEX_DIR = "indices/art_index"
_index: FileIndex | None = None


def init_local_index(index_dir: str = INDEX_DIR):
    print(":: [start]\tinit_local_index")
    start = time.time()
    if path.exists(index_dir):
        shutil.rmtree(index_dir)
    os.makedirs(index_dir)

    global _index
    _index = create_in(INDEX_DIR, get_schema())
    write_test_data(_index)
    # TODO load shared index data
    end = time.time()
    print(f":: [end]\tinit_local_index time:{end - start}s")


def write_test_data(ix: FileIndex):
    faker = Faker("ja-JP")
    writer = ix.writer()

    for i in range(500):
        title = faker.sentence().replace("。", "")
        description = faker.text()
        tags = [faker.name() for _ in range(int(random()*10)+1)]
        writer.add_document(
            art_id=u"search-test-art-"+str(i),
            title=title,
            description=description,
            tags=tags,
        )
    writer.commit()


def get_local_index():
    global _index
    if _index is None:
        init_local_index()
    return cast(FileIndex, _index)
