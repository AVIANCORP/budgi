##SVN 2.0.0
##Author: AVIAN CORPORATION
##Date: 06-23-2024
##------------------------------------------------------------------
##Notes: 
##------------------------------------------------------------------ 
from fastapi import APIRouter
from fastapi.responses import FileResponse
system_router = APIRouter()

@system_router.get('/test.system_manager', name='System Manager Debug Endpoint', tags=['Diagnostics'])
def system_routerTest():
    return({"Module":"Active",
            "Module Version":"2.0.0"})


#---------------------------------
#runonce - You need this function otherwise you fucked up.
#--------------------------------

def system_runonce():
    return("app.include_router(system_router)")