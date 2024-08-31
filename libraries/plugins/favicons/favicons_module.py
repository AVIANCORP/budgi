##SVN 2.0.0
##Author: AVIAN CORPORATION
##Date: 06-23-2024
##------------------------------------------------------------------
##Notes: 
##------------------------------------------------------------------ 
from fastapi import APIRouter
from fastapi.responses import FileResponse
icon_router = APIRouter()

@icon_router.get('/favicon.ico', include_in_schema=False)
def favicon():
    return FileResponse('./libraries/plugins/favicons/favicon.png')

@icon_router.get('/test.favicon', include_in_schema=False)
def faviconTest():
    return({"Module":"Active",
            "favicon_image":"./libraries/plugins/favicons/favicon.png"})


#---------------------------------
#runonce - You need this function otherwise you fucked up.
#--------------------------------

def favicons_runonce():
    return("app.include_router(icon_router)")