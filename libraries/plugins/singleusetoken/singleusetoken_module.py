##SVN 2.0.0
##Author: AVIAN CORPORATION
##Date: 06-19-2024
##------------------------------------------------------------------
##Notes: 
##------------------------------------------------------------------ 
from fastapi import APIRouter, Depends
from typing import Annotated
from libraries.database.mysql.mysql_module import *
import json, uuid, configparser, cryptocode
from libraries.plugins.singleusetoken.response_lib import *
config = configparser.ConfigParser()
config.read('config.ini', encoding="utf8")

singleusetoken_router = APIRouter(tags=["Token Endpoint"])

@singleusetoken_router.get('/token/list/{user_id}', name='Token Interaction Listing Endpoint', tags=['Token Endpoint'], responses=listResponse)

async def SUTRouterGet(user_id: str): #lists all interactions with token
    try:
        returnToken = json.loads(DBFunction(functionName='check_userpoint',
                                            arguments=[user_id], 
                                            instance=StartDBInstance(creds=loginArray))[0])
        if(returnToken['LTD'] == 'private'): #verifies that user is not being looked up and is who they say they are.
           SUTReply = json.loads(DBFunction(functionName='get_datanode_list_by_parent_id',
                                            arguments=[returnToken['TOK']], 
                                            instance=StartDBInstance(creds=loginArray))[0]) 
        return{"TOK":returnToken['TOK'],
               "DAT":SUTReply['DAT'],
               "RES":"OK",
               "STC":200}
    except:
        return{"UT":"None",
               "CVP":"None",
               "RES":"ERR",
               "STC":500}

@singleusetoken_router.post('/token/{token_id}', name='Create Token Interaction', tags=['Token Endpoint'])

async def SUTRouterPost(token_id: str, user_id: str, data: str):
    try:
        jsonArray = json.loads(data)
        if('type' in jsonArray and 'data' in jsonArray and 'type' in jsonArray):
            response = json.loads(data)
            returnToken = json.loads(DBFunction(functionName='init_datanode',
                                                arguments=[cryptocode.encrypt(json.dumps(response), token_id), json.dumps({"reply_to":token_id, "mime":"application/json","user_id": user_id})], 
                                                instance=StartDBInstance(creds=loginArray))[0])

            return{"TOK":returnToken['PID'],
                   "UT":user_id,
                   "RES":returnToken['RES'],
                   "STC":returnToken['STC']}
        else:
            return{"TOK":returnToken['PID'],
                   "UT":user_id,
                   "RES":'BAD',
                   "STC":400}
    except:
        return{"TOK":"None",
               "UT":"None",
               "RES":"ERR",
               "STC":500}

@singleusetoken_router.delete('/token/{token_id}', name='Delete interaction from token list', tags=['Token Endpoint'])
async def SUTRouterDelete(token_id: str, publicToken:str):
    try:

        deletedToken = json.loads(DBFunction(functionName='datanode_terminate_as_parent',
                                            arguments=[token_id, publicToken], 
                                            instance=StartDBInstance(creds=loginArray))[0])
        return{"TOK":deletedToken['DAT'],
               "RES":"OK",
               "STC":200}
    except:
        return{"TOK":"None",
               "RES":"ERR",
               "STC":500}

@singleusetoken_router.get('/test.tokens', name='Token Debug Endpoint', tags=['Diagnostics'])
async def sstDebugEndpoint():
    return({'Module':'Active',
            'Module Version':'2.0.0'})

@singleusetoken_router.get('/token/{token_id}', name='Read Token Interaction', tags=['Token Endpoint'])
async def sstReadEndpoint(token_id: str, token: str):
    try:

        readToken = json.loads(DBFunction(functionName='get_framework_datanode',
                                          arguments=[token_id], 
                                          instance=StartDBInstance(creds=loginArray))[0])
        return{"DAT":json.loads(cryptocode.decrypt(readToken['DAT'], token))['data'],
               "STC":readToken['STC'], 
               "MIM":readToken['TYP'],
               "TYP":json.loads(cryptocode.decrypt(readToken['DAT'], token))['type'],
               "RES":readToken['RES']}
    except:
        return{"TOK":"None",
            "UT":"None",
            "RES":"ERR",
            "STC":500}

#Read modified token

#---------------------------------
#runonce - You need this function otherwise you fucked up.
#--------------------------------

def singleusetoken_runonce():
    return("app.include_router(singleusetoken_router)")
