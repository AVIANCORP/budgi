##SVN 2.0.0
##Author: AVIAN CORPORATION
##Date: 06-19-2024
##------------------------------------------------------------------
##Notes: 
##------------------------------------------------------------------ 
from fastapi import APIRouter, Depends
from typing import Annotated
from libraries.database.mysql.mysql_module import *
import json, uuid
from libraries.routes.messages.response_lib import *


message_router = APIRouter(tags=["Message Endpoint"])

@message_router.post('/message', name='Send message', responses=messagePostResponse, description=messagePostDescription) 
async def messageRouterPost(utoken: str, inboxID: int, content: str, metadata: dict):
    try:
        returnToken = json.loads(DBFunction(functionName='init_datanode',
                                            arguments=[json.dumps({"content":content, "data":metadata}), json.dumps({"reply_to":inboxID, "mime":"text/text","user_id": utoken})], 
                                            instance=StartDBInstance(creds=loginArray))[0])
        return ({"PID":str(returnToken['PID']), 
                                 "UT":str(returnToken['UT']), 
                                 "RES":str(returnToken['RES']),
                                 "STC":int(returnToken['STC'])})
    except:
        return{"ID":"None",
               "UT":"None",
               "RES":"ERR"}
    
@message_router.get('/message', name='Read message', responses=messageReadResponse, description=messageReadDescription)
async def messageRouterRead(utoken: str, postid: str, ):
    try:
        returnToken = json.loads(DBFunction(functionName='get_datanode',
                                            arguments=[postid, utoken], 
                                            instance=StartDBInstance(creds=loginArray))[0])
        return ({"DAT":returnToken['DAT'], 
                 "ID":returnToken['UT'], 
                 "RES":returnToken['RES'],
                 'STC':returnToken['STC']})
    except:
        return{"RID":"None",
               "ID": "None",
               "RES": "ERR"}

@message_router.get('/test.message', name='Messaging Debug Endpoint', tags=['Diagnostics'])
async def messageDebugEndpoint():
    return({'Module':'Active',
            'Module Version':'2.0.0'})


#---------------------------------
#runonce - You need this function otherwise you fucked up.
#--------------------------------

def messages_runonce():
    return("app.include_router(message_router)")
