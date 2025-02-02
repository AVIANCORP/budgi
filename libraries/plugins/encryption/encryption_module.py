##SVN 2.0.0
##Author: AVIAN CORPORATION
##Date: 06-19-2024
##------------------------------------------------------------------
##Notes: 
##------------------------------------------------------------------ 
from fastapi import APIRouter
import cryptocode

encryption_router = APIRouter(include_in_schema=False)

@encryption_router.get('/v1_encrypt/', include_in_schema=False)

async def encryptionGet(data: str, key: str): #lists all interactions with token
    try:
        return{"DAT":str(cryptocode.encrypt(str(data), str(key))),
               "INPUT":str(data),
               "KEY":str(key),
               "RES":"OK",
               "STC":200}

    except:
        return{"DAT":"",
               "INPUT":"",
               "KEY":"",
               "RES":"ERR",
               "STC":500}

@encryption_router.get('/v1_decrypt/', include_in_schema=False)

async def decryptionGet(data: str, key: str): #lists all interactions with token
    try:
        return{"DAT":str(cryptocode.decrypt(str(data), str(key))),
               "INPUT":str(data),
               "KEY":str(key),
               "RES":"OK",
               "STC":200}

    except:
        return{"DAT":"",
               "INPUT":"",
               "KEY":"",
               "RES":"ERR",
               "STC":500}

@encryption_router.get('/test.encryption', include_in_schema=False)
async def sstDebugEndpoint():
    return({'Module':'Active',
            'Module Version':'2.0.0'})


#Read modified token

#---------------------------------
#runonce - You need this function otherwise you fucked up.
#--------------------------------

def encryption_runonce():
    return("app.include_router(encryption_router)")
