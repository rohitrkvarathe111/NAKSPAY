from fastapi import FastAPI, Request
from users import routes as user_routes
from orgist import routes as org_routes
from help_fun import routes as helper_routes
from users.models import User
from orgist.models import Orgist
import random
from database import engine, Base
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

# app = FastAPI()
app = FastAPI(debug=True)
templates = Jinja2Templates(directory="templates")  

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
app.include_router(org_routes.router, prefix="/org", tags=["Orgist"])
app.include_router(helper_routes.router, prefix="/help", tags=["Help"])

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    message = "Oops! The page you are looking for is lost in space."
    error = random.randint(1000, 9999)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": message,
        "error": error
    })

@app.post(
    "/hii",
    summary="Greet the user",
    description="This API endpoint returns a simple greeting message to confirm the server is responding.",
    response_description="A JSON message containing a greeting."
)
def read_root():
    return {"detail": "Hello this is user"}
