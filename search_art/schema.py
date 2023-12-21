from whoosh.fields import *
from whoosh.analysis import NgramAnalyzer, StopFilter
from pathlib import Path

def stopWordsFilter():
  stopwords = []
  stopwords_path = Path(__file__).parent.joinpath("stopwords.txt")

  with open(stopwords_path, "r", encoding="utf-8") as f:
    stopwords = [word.replace("\n","") for word in f.readlines()]
  return StopFilter(stopwords)


# フロントエンドで定義したデータベースのスキーマに寄せるとフロントエンドからの引継ぎがしやすくて良さそう
# https://github.com/megane-s/minshumi-frontend/blob/main/prisma/schema.prisma
def get_schema():
  schema = Schema(
    artId=ID(
      stored=True,
    ),
    # タイトルはその作品を特徴づける印象的な文字列が入るのでストップワードの削除は行わない
    title=TEXT(
      stored=True,
      analyzer=NgramAnalyzer(minsize=1, maxsize=10),
    ),
    # TODO 形態素解析などで分かち書きするフィルターも入れたい
    description=TEXT(
      analyzer=NgramAnalyzer(minsize=1, maxsize=10) | stopWordsFilter(),
    ),
    tags=KEYWORD(
      stored=True,
    ),
  )
  return schema
