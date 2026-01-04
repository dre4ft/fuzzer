from fastapi import FastAPI, HTTPException,APIRouter,Depends
import json
from pydantic import BaseModel
from .managedb import get_db
from sqlalchemy.orm import Session
from handler import do


router = APIRouter()


class ScanSchema(BaseModel):
    url : str 
    fuzzType : str
    method : str = None 
    body : dict = None 
    headers : dict  = None 


@router.post("/submitscan")
def submitscan(scan : ScanSchema, db : Session = Depends(get_db)):
    try:
        result = do(scan)
        return {"result_id":result, 
                "result": load_result(result)}
    except Exception as e:
        return {"ko":e}



def load_result(filename):
    with open(f"results/{filename}.json","r") as f: 
        data = f.read()
        return json.loads(data)
