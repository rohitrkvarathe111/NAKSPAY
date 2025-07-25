from fastapi import FastAPI, Request
from users import routes as user_routes
from orgist import routes as org_routes
from users.models import User
from orgist.models import Orgist
from database import engine, Base
from fastapi.responses import RedirectResponse

# app = FastAPI()
app = FastAPI(debug=True)

#================ This code is used for redirect any url on doc or swegger ================#
# @app.get("/", include_in_schema=False)
# async def root():
#     return RedirectResponse(url="/docs")

# # Redirect all other undefined paths to /docs
# @app.get("/{path:path}", include_in_schema=False)
# async def catch_all(path: str, request: Request):
#     # Let known routes pass
#     known_routes = [route.path for route in app.routes]
#     if request.url.path in known_routes:
#         return

#     return RedirectResponse(url="/docs")
#================ ================ ================ ====================== ================#

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(org_routes.router, prefix="/org", tags=["Org"])

@app.get("/")
def read_root():
    return {"message": "Hello"}
