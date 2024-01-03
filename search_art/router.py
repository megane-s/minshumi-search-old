from dataclasses import dataclass
from fastapi import APIRouter
from pydantic import BaseModel, Field
from search_art.search import search
from search_art import local_index

router = APIRouter(prefix="/art")

local_index.init_local_index()


@router.post(
    "/reload-index",
    description="LocalIndexを初期化しデータをSharedIndexからロードします。",
)
def update_local_index():
    local_index.init_local_index()
    return {"message": "ok"}


@dataclass
class AddArtData(BaseModel):
    art_id: str = Field(None, description="作品のID")
    title: str = Field("", description="作品のタイトル")
    description: str = Field("", description="作品の説明")
    tags: list[str] = Field("", description="作品のタグ")


@router.post(
    "/",
    description="作品をLocalIndexに追加します",
)
def add_art_to_index(
    art: AddArtData
):
    index = local_index.get_local_index()
    writer = index.writer()
    writer.add_document(
        art_id=art.art_id,
        title=art.title,
        description=art.description,
        tags=art.tags,
    )
    writer.commit()
    return {"message": "ok"}


@router.get(
    "/search",
    description="検索キーワードをもとにLocalIndexから検索します。",
)
def search_arts(
    q: str,
):
    return search(q)
