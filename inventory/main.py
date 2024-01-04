from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from os import getenv
from typing import Callable

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=getenv("ALLOWED_ORIGIN").split(","),
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host=getenv("REDIS_HOST"),
    port=getenv("REDIS_PORT"),
    password=getenv("REDIS_PASSWORD"),
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get('/products')
def all() -> list[Product]:
    return [format(pk) for pk in Product.all_pks()]

format:  Callable[[str], Product]  = lambda pk : Product.get(pk)

@app.post('/products')
def create(product: Product) -> Product:
    return product.save()


@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str) -> int:
    return Product.delete(pk)
