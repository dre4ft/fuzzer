from fastapi import  HTTPException,APIRouter,Depends
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
