from fastapi import FastAPI, UploadFile, File, HTTPException, Form, APIRouter, Security
from help_fun.backblaze import BackblazeB2
from fastapi.responses import JSONResponse
from users.routes import oauth2_scheme
from help_fun.auth_helpers import get_current_user




router = APIRouter()
b2 = BackblazeB2()


@router.post("/file_upload")
async def upload_file(file: UploadFile = File(...),
                    token: str = Security(oauth2_scheme)):
    
    payload = get_current_user(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        content = await file.read()
        result = b2.upload_file(content, file.filename)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/file_url")
async def get_signed_url_for_file(file_name: str, 
                        expiry: int = 120,
                        token: str = Security(oauth2_scheme)
                        ):
    payload = get_current_user(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        url = b2.get_signed_url(file_name, expiry)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.delete("/delete_file")
async def delete_file(
    file_name: str,
    token: str = Security(oauth2_scheme)
    ):

    payload = get_current_user(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        result = b2.delete_file(file_name)
        return JSONResponse(content=result)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
