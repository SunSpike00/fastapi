import openai
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from bson.json_util import dumps
from bson.json_util import loads

# uvicorn main:app --reload --port=8000

openai.api_key = ""
app = FastAPI()
mongodb = None


class Product(BaseModel):
    product_name: str
    details: str
    tone_and_manner: Optional[str] = None


class AdGenerator:
    def __init__(self, engine='gpt-3.5-turbo'):
        self.engine = engine

    def using_engine(self, prompt):
        system_instruction = f"assiatant는 마케팅 문구 작성 도우미로 동작한다. user의 내용을 참고하여 마케팅 문구를 작성해라"
        messages = [{"role": "system", "content": system_instruction},
                    {"role": "assistant", "content": prompt}]
        response = openai.chat.completions.create(model=self.engine, messages=messages)
        result = response.choices[0].message.content.strip()
        return result

    def generate(self, product_name, details, tone_and_manner):
        prompt = f'제품 이름: {product_name}\n주요 내용: {details}\n광고 문구의 스타일:{tone_and_manner} 위 내용을 참고하여 마케팅 문구를 만들어라'
        result = self.using_engine(prompt)
        return result


class MongoDB:
    client = None
    collection = None

    def __init__(self, key=''):
        url = f'mongodb+srv://mia99938080:{key}@cluster0.sgkyqvf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
        self.client = MongoClient(url)

    def set_database(self):
        database = self.client['createAd']
        self.collection = database['adLog']

    def insert_one(self, data):
        self.collection.insert_one(data)

    def select_all(self):
        return self.collection.find({}, {"_id": 0})


# http://127.0.0.1:8000/create_ad
@app.post("/create_ad")
async def root(product: Product):

    ad_generator = AdGenerator()
    ad = ad_generator.generate(product_name=product.product_name,
                               details=product.details,
                               tone_and_manner=product.tone_and_manner)

    mongodb = MongoDB()
    mongodb.set_database()

    mongodb.insert_one(
        {"product": product.product_name, "details": product.details, "tone_and_manner": product.tone_and_manner,
         "ad": ad})

    cursor = mongodb.select_all()
    list_cur = list(cursor)
    json_data = loads(dumps(list_cur))

    return {'ad': ad, "json_data": json_data}