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
from libraries.routes.files.response_lib import *

relations_router = APIRouter(tags=["Relations Endpoint"])


@relations_router.get('/test.relations', name='Relation Debug Endpoint', tags=['Diagnostics'])
async def fileDebugEndpoint():
    return({'Module':'Active',
            'Module Version':'2.0.0'})


#---------------------------------
#runonce - You need this function otherwise you fucked up.
#--------------------------------

def relations_runonce():
    return("app.include_router(relations_router)")
