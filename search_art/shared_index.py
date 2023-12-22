from google.cloud import storage
from google.cloud.storage import Blob
from pathlib import Path

from util.env import get_env, load_env

from .index import INDEX_DIR
from shutil import unpack_archive, make_archive, rmtree
from uuid import uuid4
import os
import time

load_env()

storage_client = storage.Client()
bucket = storage_client.bucket(get_env("GCS_INDEX_BUCKET"))

ARCHIVE_FORMAT = "zip"

def load_art_shared_search_index():
  # GCSからZIPをダウンロード
  zip_local = None

  try:
    id = uuid4().hex
    zip_local = Path("./tmp", id)
    zip_blob :Blob = bucket.blob(INDEX_DIR)
    zip_blob.download_to_filename(zip_local)

    # ZIPを解凍してINDEX_DIRに配置
    unpack_archive(zip_local, INDEX_DIR, format=ARCHIVE_FORMAT)
  except Exception as e:
    print(e)

  # TODO クリーンアップ
  if zip_local is not None:
    os.remove(zip_local)

MAX_UPLOAD_RETRY_COUNT = 5

def update_art_shared_search_index(retry_count=0):
  if MAX_UPLOAD_RETRY_COUNT < retry_count:
    raise NotImplementedError(f"shared_indexの更新に失敗しました。原因:update_art_shared_search_indexの最大リトライ数({MAX_UPLOAD_RETRY_COUNT}回)に達した")

  print("update_art_shared_search_index")

  zip_local = None
  zip_blob = None

  try:
    # TODO ロック中は1秒待ってから再度リトライ
    zip_blob :Blob = bucket.blob(INDEX_DIR)
    print(zip_blob.metadata["locked"])
    if zip_blob.exists() and zip_blob.metadata["locked"] == "YES":
      print("shared_search_index is locked . retry after 1sec")
      time.sleep(1)
      update_art_shared_search_index(retry_count=retry_count+1)
    zip_blob.upload_from_string("")
    zip_blob.metadata["locked"] = "YES"

    # ZIPに固める
    id = uuid4().hex
    zip_local = Path("./tmp", id)
    make_archive(zip_local, format=ARCHIVE_FORMAT, root_dir=INDEX_DIR)
    zip_local_path = f"{zip_local}.{ARCHIVE_FORMAT}"

    # GCSにアップロード
    zip_blob.upload_from_filename(zip_local_path)
  except Exception as e:
    print(e)

  # クリーンアップ
  if zip_local is not None:
    os.remove(str(zip_local) + ".zip")
  if zip_blob is not None:
    zip_blob.metadata["locked"] = "NO"

