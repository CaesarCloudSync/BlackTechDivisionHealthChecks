import os
import io
import json
import base64
import hashlib
import asyncio 
import uvicorn
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Header,Request,File, UploadFile,status,Form
from fastapi.responses import StreamingResponse,FileResponse,Response
from typing import Dict,List,Any,Union
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from CaesarAICronEmail.CaesarAIEmail import CaesarAIEmail
from BTDGetTokenDetails import BTDGetTokenDetails
from CaesarSQLDB.caesarcrud import CaesarCRUD
btdtokendets = BTDGetTokenDetails()
load_dotenv(".env")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


caesarcrud = CaesarCRUD()
JSONObject = Dict[Any, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]
KARTRA_API_KEY = os.getenv("KARTRA_API_KEY")
KARTRA_API_PASSWORD = os.getenv("KARTRA_API_PASSWORD")


@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAIWorld!"
@app.post('/btdhealthcheck') # POST
async def btdhealthcheck(data: JSONStructure = None):
    num_attempts = 3
    successes = 0
    for i in range(num_attempts):
        try:
            user = btdtokendets.get_token_details()
            lead_event_req = btdtokendets.lead_event_req
            resp = requests.post("https://blacktechdivisionreward-hrjw5cc7pa-uc.a.run.app/v1/rewardlead?leadaction=attendedonlineevent&reward=10&api_key=fPvimQSo&api_pass=xfdgUTCcYEqD",json=lead_event_req)
            ##print(resp.json())
            if resp.json().get("message"):
                user_after = btdtokendets.get_token_details()
                after_greater_than  = user_after["reward"] > user["reward"]
                if after_greater_than == True:
                    print(resp.json()['message'])
                    CaesarAIEmail.send(**{"email":"revisionbankedu@gmail.com","subject":f"BTDTokens Health Check Success","message":f"{resp.json()['message']}","attachment":None})
                    successes += 1
                    #return {"message":"success"}
                else:
                    CaesarAIEmail.send(**{"email":"revisionbankedu@gmail.com","subject":f"BTDTokens Health Check Error","message":f"Token was not awarded. Check Codebase.","attachment":None})
                    
            else:
                if resp.json().get("error"):
                    print(resp.json().get("error"))
                    CaesarAIEmail.send(**{"email":"revisionbankedu@gmail.com","subject":f"BTDTokens Health Check Error","message":f"{resp.json().get('error')}","attachment":None})
                    
                else:
                    CaesarAIEmail.send(**{"email":"revisionbankedu@gmail.com","subject":f"BTDTokens Health Check Error","message":f"Check Codebase went horribly wrong.","attachment":None})
                    
        except Exception as ex:
            error_detected = {"error": "error occured","errortype":type(ex), "error": str(ex)}
            print(error_detected)
            CaesarAIEmail.send(**{"email":"revisionbankedu@gmail.com","subject":f"BTDTokens Health Check Error","message":f"{type(ex)} - {ex}","attachment":None})
    if successes == 3:
        CaesarAIEmail.send(**{"email":"revisionbankedu@gmail.com","subject":f"BTDTokens Health Full Success","message":f"BTDTokens Health Full Success","attachment":None})
        res = caesarcrud.delete_data("rewardleads","email = 'test.token@gmail.com'")
        return {"message":"success"}
    else:
        CaesarAIEmail.send(**{"email":"revisionbankedu@gmail.com","subject":f"BTDTokens Health Check Error Num of errors: {num_attempts - successes}","message":f"BTDTokens Health Check Error {num_attempts - successes}","attachment":None})
        return {"message":"error"}
    

if __name__ == "__main__":

    uvicorn.run("main:app",port=8080,log_level="info")
    #uvicorn.run()
    #asyncio.run(main())