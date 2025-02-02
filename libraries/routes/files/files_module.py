##SVN 2.0.0
##Author: AVIAN CORPORATION
##Date: 06-19-2024
##------------------------------------------------------------------
##Notes: 
##------------------------------------------------------------------ 
from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from libraries.database.mysql.mysql_module import *
import json, uuid
from libraries.routes.files.response_lib import *

file_router = APIRouter(tags=["File Endpoint"])


@file_router.get('/test.files', name='File Debug Endpoint', tags=['Diagnostics'])
async def fileDebugEndpoint():
    return({'Module':'Active',
            'Module Version':'2.0.0'})


#---------------------------------
#runonce - You need this function otherwise you fucked up.
#--------------------------------

def files_runonce():
    return("app.include_router(file_router)")
