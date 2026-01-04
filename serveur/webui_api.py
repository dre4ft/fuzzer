from fastapi import  HTTPException,APIRouter,Depends
from fastapi.responses import HTMLResponse,FileResponse
import json
from pydantic import BaseModel
from .managedb import get_db
from sqlalchemy.orm import Session
from handler import do
from typing import Optional

router = APIRouter()




class ScanSchema(BaseModel):
    url: str
    fuzzType: str
    method: Optional[str] = None
    body: Optional[dict] = None
    headers: Optional[dict] = None


@router.post("/fuzz")
def submitscan(scan : ScanSchema, db : Session = Depends(get_db)):
    try:
        result = do(scan)
        return {"result_id":result, 
                "result": load_result(result)}
    except Exception as e:
        return HTTPException(status_code=469, detail=str(e))
    



def load_result(filename):
    with open(f"results/{filename}.json","r") as f: 
        data = f.read()
        return json.loads(data)

@router.get("/result/{result_id}")
def download_result(result_id: str):
    file_path = f"results/{result_id}.json"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Result not found")

    return FileResponse(
        path=file_path,
        media_type="application/json",
        filename=f"scan_{result_id}.json"
    )

@router.get("/wordlist")
def list_wordlists():
    return {
        "passwords.txt": "Common leaked passwords",
        "jwt.txt": "JWT-related payloads",
        "usernames.txt": "Common usernames",
        "admin.txt": "Admin & privileged words"
    }