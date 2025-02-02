##SVN 2.0.0
##Author: AVIAN CORPORATION
##Date: 06-19-2024
##------------------------------------------------------------------
##Notes: 
##------------------------------------------------------------------ 
from fastapi import APIRouter, Depends, UploadFile, Response
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from libraries.database.mysql.mysql_module import *
import json
from libraries.routes.posts.response_lib import *

#-------------------------------------------------------------------
#For the user login thingy, I am making a system that requires a ut (User Token) and a cvp (Client Verification Phrase)
#
#The response will help with any possible issues that the database may return. If the db returns a string,
#the RES code will return an error.
#------------------------------------------------------------------- 

post_router = APIRouter(tags=["Post Endpoint"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@post_router.post('/post', name='Publish post/comment', responses=publishResponse, description=publishDescription) 
async def postRouterPublish(utoken: str, index: int, content: str, metadata: dict):
    try:
        returnToken = json.loads(DBFunction(functionName='init_datanode',
                                            arguments=[json.dumps({"content":content, "data":metadata}), json.dumps({"reply_to":index, "mime":"text/text","user_id": utoken})], 
                                            instance=StartDBInstance(creds=loginArray))[0])
        return ({"PID":str(returnToken['PID']), 
                                 "UT":str(returnToken['UT']), 
                                 "RES":str(returnToken['RES']),
                                 "STC":int(returnToken['STC'])})
    except:
        return{"ID":"None",
               "UT":"None",
               "RES":"ERR"}
    
@post_router.delete('/post', name='Delete post/comment', responses=deleteResponse, description=deleteDescription)
async def postRouterDelete(utoken: str, postid: str, ):
    try:
        returnToken = json.loads(DBFunction(functionName='datanode_terminate',
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


@post_router.post('/upload', name='Upload file', responses=uploadResponse, description=uploadDescription)
async def postRouterUpload(utoken: str, file: UploadFile):
    try:
        returnToken = json.loads(DBFunction(functionName='init_userpoint',
                                            arguments=[utoken, file], 
                                            instance=StartDBInstance(creds=loginArray))[0])
        return Response(content={"ID":returnToken['ID'], 
                                 "UT":returnToken['UT'], 
                                 "RES":returnToken['RES']}, 
                        status_code=returnToken['STC'])
    except:
        return{"UT":"None",
               "UT":"None",
               "RES":"ERR"}

@post_router.get('/post/{publicid}', name='Get post/comment', tags=['Post Endpoint'], description='Load a post in raw form.')
async def postRouterGet(publicid: str):
#    try:
        returnToken = json.loads(DBFunction(functionName='get_datanode',
                                            arguments=[publicid], 
                                            instance=StartDBInstance(creds=loginArray))[0])
        return ({"DAT":returnToken['DAT'], 
                 "STC":returnToken['STC'], 
                 "MIM":returnToken['TYP'],
                 "RES":returnToken['RES']})
#    except:
 #       return{"UT":"None",
 #              "UT":"None",
 #              "RES":"ERR"}

@post_router.get('/test.posts', name='Post Debug Endpoint', tags=['Diagnostics'], description='Disable in production')
async def postDebug():
    return({'Module': 'Active',
            'Module Version': '1.0.0'})


#---------------------------------
#runonce - You need this function otherwise you fucked up.
#--------------------------------

def posts_runonce():
    return("app.include_router(post_router)")
