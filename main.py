##SVN 2.0.0
##Author: AVIAN CORPORATION
##Date: 06-15-2024
##------------------------------------------------------------------
##Notes: 
##------------------------------------------------------------------ 

from fastapi import FastAPI, HTTPException, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from typing import Union
import configparser, uvicorn, os, sys, importlib

def library_folder_inject(folder):
   for route_listing in os.listdir(str(folder)):
      try:
         for filename_listing in os.listdir(f"{str(folder)}/{route_listing}"):
            if '_module.py' in filename_listing:
               currentLibrary = f"{str(folder)}{route_listing}.{filename_listing}".replace('/','.').replace('.py','')
               exec(f"from {currentLibrary} import *")
               #exec(f"moduleObject = __import__({currentLibrary})")
               #exec(f"globals()[{currentLibrary}] = moduleObject")
               exec(f"exec({filename_listing.split('_')[0]}_runonce())")
               print(f"Loaded {filename_listing.split('_')[0]} library")
      except Exception as e:
         print(f"Issue loading library: {currentLibrary}\n[EXCEPTION]\n{e}\n[/EXCEPTION]")

def library_folder_import(folder):
    moduleList = []
    for route_listing in os.listdir(str(folder)):
        try:
            for filename_listing in os.listdir(f"{str(folder)}/{route_listing}"):
                if '_module.py' in filename_listing:
                    currentLibrary = f"{str(folder)}{route_listing}.{filename_listing}".replace('/','.').replace('.py','')
                    importlib.import_module(currentLibrary)
                    moduleList.append(currentLibrary)
                    print(f"Loaded {filename_listing.split('_')[0]} library")
        except Exception as e:
            print(f"Issue loading library: {currentLibrary}\n[EXCEPTION]\n{e}\n[/EXCEPTION]")
    return moduleList

# Load configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Load configuration settings
app = FastAPI(title=str(config.get('devConfig','title')),
              description=config.get('devConfig','description'),
              version=config.get('devConfig','version'),
              terms_of_service=config.get('devConfig','terms_of_use'))

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
oauth2_schema = OAuth2PasswordBearer(tokenUrl="authorize")

#Currently God wants me dead. I got COVID, my car got crunched, and NOW this script double fucking loads! Why?
#Good question! I don't fucking know! Some faggot on stackoverflow will probably be a fucking douche or whatever,
#but I honestly don't care at this point. It works. That's all that matters. If you don't like it, then fucking fix it
#because I sure don't know how.


#temporary explicit import of mysql is needed since the injection method does not work for this.
from libraries.database.mysql.mysql_module import *

library_folder_inject('libraries/routes/')
library_folder_inject('libraries/plugins/')
library_folder_inject('libraries/database/')



#Generate a list of debug points from imported libraries

apiCallList = []

for apiCall in app.routes:
   if 'test.' in str(apiCall): #Looks for any string with "test." since test.* is the primary debug port for addons.
      apiCallList.append(str(apiCall).split("'")[1])

#For security debugging is able to be disabled. config->debug=False
if config.get('config','debug') == "False":

   for endpoint in apiCallList:
      print(f"Disabling debugging for {endpoint}") #Obvious

      for routeToRemove in app.routes:
         try:
            app.routes.remove(routeToRemove) #Removes the endpoint from the list
         except:
            print(f"Unable to disable debugging mode on \"endpoint\".")

      @app.get(endpoint, tags=["Diagnostics"], name='Built-in Diagnosics',response_description="Debug information", include_in_schema=False, )
      def debugEndpointOff():
         return('Endpoint debugging disabled') #I wonder what this does

#Initialize FastAPI

if config.get('config','debug') == "True":
   
   @app.get("/test", tags=["Diagnostics"], name='Built-in Diagnosics',response_description="Debug information")
   def debugMainOn():
      return(
               {"Loaded modules": list(sys.modules.keys()),
               "Server Settings": {"port":int(config.get('config','port')),
                                   "reload upon update":config.get('config','auto_reload')},
               "Main":"Active",
               "Database": DBVersion(),
               "Debug Points": list(apiCallList)
               }
            )
else:
   @app.get("/test", tags=["Diagnostics"], name='Built-in Diagnosics',response_description="Debug information", include_in_schema=False)
   def debugMainOff():
      

      return(  
               {"Loaded modules": "Debug mode disabled",
               "Server Settings": {"Debug mode disabled"},
               "Main":"Active",
               "Database": "Debug mode disabled",
               "Debug Points": list(apiCallList)
               }
            )

      
#Landing page for retards and/or script kiddies.

#NOTE: Why did I prestate values? Because I don't want to explain to the lowest common denominator why they can't use a string in place
#NOTE: of a boolean value. If you are that dipshit I have to do this for, kill yourself.

@app.get("/", include_in_schema=False,response_description="System information")
def default():
   return {"version_number":float("3.02"),
           "developmental_version":bool(True),
           "public_config":int(config.get('config','port')),
           "live_update":bool(config.get('config','auto_reload')),
           "documentation":str("localhost:8000/docs/")}

if __name__ == "__main__":
   uvicorn.run("main:app", 
               port=int(config.get('config','port')), 
               reload=bool(config.get('config','auto_reload')),
               host=bool(config.get('config','host')))
