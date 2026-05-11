from fastapi import FastAPI
from my_site.api.user import user_router
from my_site.api.category import category_router
from my_site.api.subcategory import subcategory_router
from my_site.api.product import product_router
from my_site.api.product_image import product_image_router
from my_site.api.review import review_router
from my_site.api.auth import auth_router
import uvicorn

store_app = FastAPI()

store_app.include_router(user_router)
store_app.include_router(category_router)
store_app.include_router(subcategory_router)
store_app.include_router(product_router)
store_app.include_router(product_image_router)
store_app.include_router(review_router)
store_app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run(store_app, host='127.0.0.1', port=8000)