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
from libraries.routes.timeline.timeline_lib import *

timeline_router = APIRouter(tags=["Timeline Endpoint"])

@timeline_router.get('/timeline/{userid}/{group}', name='Pull up timeline', tags=['Timeline'])
async def timelineGroupEndpoint(userid: str, group: str):
    try:
        returnToken = json.loads(DBFunction(functionName='get_datanode_list_by_accesspoint',
                                    arguments=[str(userid), str(group)], 
                                    instance=StartDBInstance(creds=loginArray))[0])
        return(returnToken)
    except:
        return({"DAT":"none",
                "STC":500,
                "RES":"ERR"})

@timeline_router.get('/test.timeline', name='Timeline Debug Endpoint', tags=['Diagnostics'])
async def timelineDebugEndpoint():
    return({'Module':'Active',
            'Module Version':'2.0.0'})

@timeline_router.get('/timeline/{userid}', name='Pull up timeline', tags=['Timeline'])
async def timelineUserEndpoint(userid: str):
    #try:
        returnToken = json.loads(DBFunction(functionName='get_datanode_list_by_accesspoint',
                                    arguments=[str(userid), None], 
                                    instance=StartDBInstance(creds=loginArray))[0])
        return(returnToken)
    #except:
    #    return({"DAT":"none",
    #            "STC":500,
    #            "RES":"ERR"})

@timeline_router.get('/test.timeline', name='Timeline Debug Endpoint', tags=['Diagnostics'])
async def timelineDebugEndpoint():
    return({'Module':'Active',
            'Module Version':'2.0.0'})


#---------------------------------
#runonce - You need this function otherwise you fucked up.
#--------------------------------

def timeline_runonce():
    return("app.include_router(timeline_router)")
