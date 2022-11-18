import uvicorn

from fastapi import FastAPI

from .db_queries import db_init_table, db_get_products, db_get_categories, db_get_product_to_category


app = FastAPI()


@app.get("/")
async def root():
    return "Hello!"


@app.get("/get_products")
async def root():
    return db_get_products()


@app.get("/get_categories")
async def root():
    return db_get_categories()


@app.get("/get_products_to_categories")
async def root():
    return db_get_product_to_category()


@app.get("/db_init_table")
async def root():
    return db_init_table()


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8080)
