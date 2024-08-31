##SVN 1.01
##Author: AVIAN CORPORATION
##Date: 12-24-2023
##------------------------------------------------------------------
##Notes:
##------------------------------------------------------------------ 
import mysql.connector, mysql.connector.errors, json
import configparser
from fastapi import APIRouter

# Load configuration file
dbConfig = configparser.ConfigParser()
dbConfig.read('./libraries/database/mysql/config.ini')
loginArray = {'host':dbConfig.get('database','ip'),
              'user':dbConfig.get('database','username'),
              'password':dbConfig.get('database','password'),
              'db':dbConfig.get('database','name')}

database_router = APIRouter()

@database_router.get('/test.db', include_in_schema=False)
def userRouterLogout():
    return({'Config':loginArray,
            'Instance Raw': str(StartDBInstance(creds=loginArray)),
            'Module':'Active'})

def StartDBInstance(creds=(None,None,None,None)):
    if creds:
        try:
            Instance = mysql.connector.connect(host=creds['host'], user=creds['user'], password=creds['password'], database=creds['db'])
            return(Instance.cursor(),Instance)
        except mysql.connector.errors.ProgrammingError as exception:
            if exception.errno == 1045:
                return({'error':'Invalid credentials'})
            elif exception.errno == 1049:
                return({'error':'Invalid database'})
            else:
                return({'error': str(exception)})
    else:
        return({'error': "Malformed request"}) #Malformed request


def DBFunction(functionName=None, arguments=[None], instance=None):
    DB = instance[0]
    template = 'SELECT {}({});'.format(functionName, ', '.join(['%s']*len(arguments)))
    try:
        DB.execute(template, arguments)
        sysResponse = DB.fetchall()[0]
        instance[1].commit()
        return(sysResponse)
    except mysql.connector.Error as err:
        return({'error':f"Exception occured while processing entity. Exception reason: {err.errno}"})

def TEMPDBBlobHandler(functionName=None, arguments=[None], instance=None):
    DB = instance[0]
    template = 'SELECT {}({});'.format(functionName, ', '.join(['%s']*len(arguments)))
    try:
        DB.execute(template, arguments)
        return DB.fetchall()[0]
    except mysql.connector.Error as err:
        return({'error':f"Exception occured while processing entity. Exception reason: {err.errno}"})


def DBBlobSetup(functionName=None, arguments=[None], instance=None):
    DB = instance[0]
    template = 'SELECT {}({});'.format(functionName, ', '.join(['%s']*len(arguments)))
    try:
        DB.execute(template, arguments)
        instance[1].commit()  # Commit changes before fetching results
        return DB.fetchall()[0]
    except mysql.connector.Error as err:
        return({'error':f"Exception occurred while processing entity.Exception reason: {err.errno}"})


def mysql_runonce():
    return("app.include_router(database_router)")

def DBVersion():
    return('MySQL: 808 Based API: 1.3')
