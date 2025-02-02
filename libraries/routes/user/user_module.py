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
import json
from libraries.routes.user.response_lib import *

#-------------------------------------------------------------------
#For the user login thingy, I am making a system that requires a ut (User Token) and a cvp (Client Verification Phrase)
#
#The response will help with any possible issues that the database may return. If the db returns a string,
#the RES code will return an error.
#------------------------------------------------------------------- 

user_router = APIRouter(tags=["User Endpoint"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@user_router.post('/login', name='Login', responses=loginResponse)
async def userRouterLogin(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        returnToken = json.loads(DBFunction(functionName='new_session',
                                            arguments=[form_data.username, form_data.password], 
                                            instance=StartDBInstance(creds=loginArray))[0])
        return{"UT":returnToken['token'],
               "CVP":returnToken['phrase'],
               "RES":"OK"}
    except:
        return{"UT":"None",
               "CVP":"None",
               "RES":"ERR"}

@user_router.post('/basic_login', name='Login (Basic Login)', responses=loginResponse)
async def userRouterLogin(username: str, password: str):
    try:
        returnToken = json.loads(DBFunction(functionName='new_session',
                                            arguments=[username, password], 
                                            instance=StartDBInstance(creds=loginArray))[0])
        return{"UT":returnToken['token'],
               "CVP":returnToken['phrase'],
               "RES":"OK"}
    except:
        return{"UT":"None",
               "CVP":"None",
               "RES":"ERR"}
    

@user_router.get('/logout', name='Logout', responses=logoutResponse)
async def userRouterLogout():
        return{"UT":"None",
               "CVP":"None",
               "RES":"RES"}

@user_router.post('/register', name='Register', responses=registerResponse)
async def userRouterRegister(username: str, password: str, userPhrase: str, tos_acknowledgement: bool = False):
    if(tos_acknowledgement == True):
        try:
            returnToken = json.loads(DBFunction(functionName='init_userpoint',
                                                arguments=[username, password, userPhrase], 
                                                instance=StartDBInstance(creds=loginArray))[0])
            return{"UT":returnToken['UT'],
                   "CVP":returnToken['CVP'],
                   "RES":returnToken['RES']}
        except:
            return{"UT":"None",
                   "CVP":"None",
                   "RES":"ERR"}
    else:
        return{"UT":"None",
               "CVP":"None",
               "RES":"TOS"}
#b'{"detail":[{"type":"int_parsing","loc":["query","index"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":""},{"type":"missing","loc":["body"],"msg":"Field required","input":null}]}'
@user_router.get('/user/stats/{username}', name='User Information')
async def userRouterStatus(username: str, userid: str):
    
        try:
            if username == '':
                returnToken = json.loads(DBFunction(functionName='check_userpoint',
                                                    arguments=[userid], 
                                                    instance=StartDBInstance(creds=loginArray))[0])
            else:
                returnToken = json.loads(DBFunction(functionName='check_userpoint',
                                                    arguments=[username], 
                                                    instance=StartDBInstance(creds=loginArray))[0])
            return{"SN":returnToken['SN'],
                   "DAT":returnToken['DAT'],
                   "HND":returnToken['HND'],
                   "TOK":returnToken['TOK'],
                   "RES":returnToken['RES'],
                   "STD":returnToken['STD'],
                   "LTD":returnToken['LTD']}
        except:
            return{"SN":'None',
                   "DAT":'None',
                   "HND":0,
                   "TOK":"None",
                   "RES":'ERR',
                   "STD":500}
        



@user_router.get('/test.users', name='User Debug Endpoint', tags=['Diagnostics'])
async def userRouterLogout():
    return({'Module':'Active',
            'Module Version':'2.0.0'})


#---------------------------------
#runonce - You need this function otherwise you fucked up.
#--------------------------------

def user_runonce():
    return("app.include_router(user_router)")
