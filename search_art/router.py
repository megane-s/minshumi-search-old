from fastapi import APIRouter
from search_art import index

router = APIRouter()

index.init_local_index()

@router.post(
  "/search-index", 
  description="LocalIndexを初期化しデータをSharedIndexからロードします。",
)
def update_local_index():
  index.init_local_index()
  return { "message": "ok" }

@router.get(
  "/search",
  description="検索キーワードをもとにLocalIndexから検索します。",
)
def search_arts(
  q: str,
):
  return index.search(q)
