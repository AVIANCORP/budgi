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

@post_router.post('/publish', name='Publish post/comment', responses=publishResponse)
async def postRouterPublish(utoken: str, index: int, content: str, metadata: dict):
    try:
        returnToken = json.loads(DBFunction(functionName='init_post',
                                            arguments=[utoken, index, content, metadata], 
                                            instance=StartDBInstance(creds=loginArray))[0])
        return Response(content={"PID":returnToken['PID'], 
                                 "UT":returnToken['UT'], 
                                 "RES":returnToken['RES']}, 
                        status_code=returnToken['STC'])
    except:
        return{"ID":"None",
               "UT":"None",
               "RES":"ERR"}
    
@post_router.delete('/delete', name='Delete post/comment', responses=deleteResponse)
async def postRouterDelete(utoken: str, postid: int, ):
    try:
        returnToken = json.loads(DBFunction(functionName='init_userpoint',
                                            arguments=[utoken, file], 
                                            instance=StartDBInstance(creds=loginArray))[0])
        return Response(content={"RID":returnToken['RID'], 
                                 "UT":returnToken['UT'], 
                                 "RES":returnToken['RES']}, 
                                 status_code=returnToken['STC'])
    except:
        return{"RID":"None",
               "UT": "None",
               "RES": "ERR"}


@post_router.post('/upload', name='Upload file', responses=uploadResponse)
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

@post_router.get('/test.posts', name='Post Debug Endpoint', tags=['Diagnostics'])
async def postDebug():
    return({'Module': 'Active',
            'Module Version': '1.0.0'})


#---------------------------------
#runonce - You need this function otherwise you fucked up.
#--------------------------------

def posts_runonce():
    return("app.include_router(post_router)")
