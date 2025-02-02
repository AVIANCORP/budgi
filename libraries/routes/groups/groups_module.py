##SVN 2.0.0
##Author: AVIAN CORPORATION
##Date: 12-14-2024
##------------------------------------------------------------------
##Notes: 
##------------------------------------------------------------------ 
from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from libraries.database.mysql.mysql_module import *
import json, uuid
from libraries.routes.groups.response_lib import *

#-------------------------------------------------------------------
# Right now I am making the group module function with several different responses.
# Creation, Interaction and Removal will have separate API responses though RES will remain the same. 
# Deleting (disbanding) a group will result in an array being returned with the following data: {"GI":"[GROUP ID]","MOD":"None","RES":"OK"}
# Creating (formulating) a group will result in an array being returned with this data: {"UT":"[USER TOKEN]", "MOD": "[GROUP PUBLIC TOKEN]", "RES": "OK"} (MOD status will be automatically appointed to the group creator)
# Interacting (checking in) with a group will return: {"GI":"[GROUP ID]", "INT":"[INTERACTION DATA]", "RES":"OK"}
#
# Reading a groups data will be processed via GET and interacting will be processed with, you guessed it, POST.
#
# Only group moderation will be able to delete the groups. For now there is no hierarchy but that may be put in later on.
#------------------------------------------------------------------- 

group_router = APIRouter(tags=["Group Endpoint"])

@group_router.delete('/group/{groupid}', name='Disband A Group', responses=disbandResponse)
async def groupRouterDisband(userid: str, groupid: str):
    userInfo = json.loads(DBFunction(functionName='check_userpoint',
                                     arguments=[userid], 
                                     instance=StartDBInstance(creds=loginArray))[0])
    try:
            groupData = json.loads(json.loads(DBFunction(functionName='get_framework_datanode',
                                            arguments=[groupid], 
                                            instance=StartDBInstance(creds=loginArray))[0])['DAT'])
            if(int(userInfo['STD']) >= 10):
                groupDataArray = groupData['members'][userid]
                if (groupDataArray['ban'] == True and 
                    groupDataArray['delete'] == True and
                    groupDataArray['write'] == True and
                    groupDataArray['execute'] == True): #Dogshit coding. I know

                    #Step 1. - List all messages in api
                    try:
                        
                        postList = json.loads(DBFunction(functionName='list_datapoints',
                                                            arguments=[groupid], 
                                                            instance=StartDBInstance(creds=loginArray))[0])
                        if postList['DAT'] != None:
                            for postID in postList['DAT'].split(','): #Step 2. begin message termination
                                
                                returnTerminateResponse = json.loads(DBFunction(functionName='datanode_terminate',
                                                                                arguments=[groupid, postID], 
                                                                                instance=StartDBInstance(creds=loginArray))[0])
                                if(returnTerminateResponse['STC'] != '200'): #if termination fails, request fallback for later.
                                    DBFunction(functionName='init_datapoint',
                                            arguments=[json.dumps({'command':'delete','id':postID,'reason':'Orphaned post.'}), json.dumps({'mode':'raw'})], 
                                            instance=StartDBInstance(creds=loginArray))
                                
                        #Step 3. Delete the group ID
                        returnToken = json.loads(DBFunction(functionName='datanode_terminate',
                                                            arguments=[groupid, userid], 
                                                            instance=StartDBInstance(creds=loginArray))[0])
                        return{"GI":groupid,
                            "MOD":userid,
                            "RES":"OK"}

                    except:
                        return{"GI":"None",
                            "MOD":"None",
                            "RES":"ERR"}
                else:
                    return{"GI":"None",
                    "MOD":"None",
                    "RES":"LIM"} #LIM = Limited account
            else:
                return{"GI":"None",
                    "MOD":"None",
                    "RES":"LIM"} #LIM = Limited account
    except:    
             return{"GI":"None",
                    "MOD":"None",
                    "RES":"INV"} #INV = Invalid group
    
@group_router.put('/group/{groupid}', name='Modify Group', responses=checkInResponse)
async def groupRouterCheckInPost(groupid: str, userid: str, data: str, action: str):
    #try:
        userInfo = int(json.loads(DBFunction(functionName='check_userpoint', arguments=[userid], instance=StartDBInstance(creds=loginArray))[0])['STD'])
        groupInfo = json.loads(DBFunction(functionName='get_framework_datanode', arguments=[groupid], instance=StartDBInstance(creds=loginArray))[0])
        groupPrivs = json.loads(groupInfo['DAT'])['members']
        
        if('post' in action):
            if('delete' in action and userInfo >= 10 and groupPrivs[userid]['delete'] == True): #Right now only admins/mods can delete posts in groups
                serverReturn = json.loads(DBFunction(functionName='associate_datanode_terminate',
                                                        arguments=[data, groupid], 
                                                        instance=StartDBInstance(creds=loginArray))[0])

            try:
                if('create' in action and userInfo >= 10 and groupPrivs[userid]['write'] == True):
                    serverReturn = json.loads(DBFunction(functionName='init_associate_datanode',
                                                        arguments=[data,json.dumps({'user_id':userid,'mime':'text/text','associate_key':groupid})], 
                                                        instance=StartDBInstance(creds=loginArray))[0])
            except:
                serverReturn = {'RES':'ERR','INT':'ERR'}    
        if('group' in action):   
            if('join' in action and userInfo >= 10 and userid not in json.loads(groupInfo['DAT'])['blacklist']):
                initReturn = json.loads(DBFunction(functionName='get_framework_datanode',
                                                    arguments=[groupid], 
                                                    instance=StartDBInstance(creds=loginArray))[0])
                memberList = json.loads(initReturn['DAT'])['members']
                memberList[userid] = json.loads(initReturn['DAT'])['properties']['group_permissions']
                updatedGroup = json.loads(initReturn['DAT'])
                updatedGroup['members'] = memberList
                serverReturn = json.loads(DBFunction(functionName='datanode_unsafe_modify',
                                                        arguments=[groupid,json.dumps(updatedGroup)], 
                                                        instance=StartDBInstance(creds=loginArray))[0])
                
            if('leave' in action):
                initReturn = json.loads(DBFunction(functionName='get_framework_datanode',
                                                    arguments=[groupid], 
                                                    instance=StartDBInstance(creds=loginArray))[0])
                memberList = json.loads(initReturn['DAT'])['members']
                del memberList[userid]
                updatedGroup = json.loads(initReturn['DAT'])
                updatedGroup['members'] = memberList
                serverReturn = json.loads(DBFunction(functionName='datanode_unsafe_modify',
                                                        arguments=[groupid,json.dumps(updatedGroup)], 
                                                        instance=StartDBInstance(creds=loginArray))[0])
            if('modify' in action and groupPrivs[userid]['execute'] == True and groupPrivs[userid]['ban'] == True):
                if('title' in action):
                    modifiedTag = 'group_title'
                if('bio' in action):
                    modifiedTag = 'group_bio'
                if('image' in action):
                    modifiedTag = 'group_image'
                if('banner' in action):
                    modifiedTag = 'group_banner'
                if('permissions' in action):
                    modifiedTag = 'group_permissions'

                initReturn = json.loads(DBFunction(functionName='get_framework_datanode',
                                                    arguments=[groupid], 
                                                    instance=StartDBInstance(creds=loginArray))[0])
                propertyArray = json.loads(initReturn['DAT'])['properties']
                propertyArray[0][modifiedTag] = data
                updatedGroup = json.loads(initReturn['DAT'])
                updatedGroup['properties'] = propertyArray
                serverReturn = json.loads(DBFunction(functionName='datanode_unsafe_modify',
                                                        arguments=[groupid,json.dumps(updatedGroup)], 
                                                        instance=StartDBInstance(creds=loginArray))[0])
                
        if('user' in action):
            if(action == 'ban_user'):
                userInfo = json.loads(DBFunction(functionName='datanode_modify',
                                                        arguments=[userid], 
                                                        instance=StartDBInstance(creds=loginArray))[0])
            if(action == 'user_modify'):  
                userInfo = json.loads(DBFunction(functionName='datanode_modify',
                                                        arguments=[userid], 
                                                    instance=StartDBInstance(creds=loginArray))[0])
    #except:
    #    serverReturn = {'RES':'ERR','DAT':'ERR'}  

        return{"GI":groupid,
            "INT":serverReturn['DAT'],
            "RES":serverReturn['RES']}

@group_router.get('/group/{groupid}', name='Read Message IDs', responses=checkInResponse)
async def groupRouterCheckInGet(groupid: str, userid: str, data: str):
    try:
        groupData = json.loads(DBFunction(functionName='get_framework_datanode', arguments=[groupid], instance=StartDBInstance(creds=loginArray))[0])['DAT']
        groupMembers = json.loads(groupData)['members']
        if userid in groupMembers and groupMembers[userid]['read'] == True:
            returnArray = []
            for member in groupMembers:
                print(member)
                returnToken = json.loads(DBFunction(functionName='get_datanode_list_by_accesspoint',
                                                    arguments=[str(member.split('-')[4]), str(groupid)], 
                                                    instance=StartDBInstance(creds=loginArray))[0])
                for Token in returnToken['DAT']:
                    returnArray.append(Token)
            returnToken['DAT'] = returnArray
        else:
            returnToken = {}
            returnToken['DAT'] = 'Not in group. Must join to send a GET request'
        return{"GI":groupid,
               "DAT":returnToken['DAT'],
               "RES":"OK",
               "STC":200}
    except:
        return{"GI":"None",
               "DAT":"None",
               "RES":"ERR",
               "STC":500}
    

@group_router.post('/group', name='Form a Group', responses=formulationResponse)
async def groupRouterFormulate(userid: str):
        userInfo = json.loads(DBFunction(functionName='check_userpoint',
                                                    arguments=[userid], 
                                                    instance=StartDBInstance(creds=loginArray))[0])
        if(int(userInfo['STD']) >= 10):
            try:

                groupArray = {"group_id":str(uuid.uuid4()), 
                            "members":{str(userid):{'read':True,'write':True,'execute':True,'delete':True,'ban':True}},
                            "blacklist":[],
                            "whitelist":[],
                            "properties":[{"group_title":"<<HELLO GROUP!>>",
                                           "group_bio":"What does Lorem Ipsum mean?",
                                           "group_image":"",
                                           "group_banner":"",
                                           "group_permissions":{"read":True,"write":True,"execute":False,"delete":False,"ban":False}}],
                            "parent_identity_key":str(uuid.uuid4())}

                returnToken = json.loads(DBFunction(functionName='init_datanode',
                                                    arguments=[json.dumps(groupArray),json.dumps({"user_id":userid,"mime":"application/json"})], 
                                                    instance=StartDBInstance(creds=loginArray))[0])
                
                return({"UT":returnToken['UT'],
                    "MOD":returnToken['PID'],
                    "RES":returnToken['RES']})
            except:
                return{"UT":"None",
                    "CVP":"None",
                    "RES":"ERR"}
        else:
            return{"UT":"None",
                   "CVP":"None",
                   "RES":"LIM"} #LIM = Limited account
@group_router.get('/test.groups', name='Groups Debug Endpoint', tags=['Diagnostics'])
async def groupDebugEndpoint():
    return({'Module':'Active',
            'Module Version':'2.0.0'})


#---------------------------------
#runonce - You need this function otherwise you fucked up.
#--------------------------------

def groups_runonce():
    return("app.include_router(group_router)")
