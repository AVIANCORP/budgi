publishResponse = {
    200:{'description':'Published',
         'content':{"application/json":
            {"example":{
                "ID":"[POST ID]",
                "UT":"[USER TOKEN]",
                "RES":"OK"}
            }
            }
        },
    300:{'description':'Unpublished - Banned/Limited',
         'content':{"application/json":
            {"example":{
                "ID":"None",
                "UT":"None",
                "RES":"TOS"}
            }
            }
        

    },
    409:{'description':'Unpublished - Not logged in',
         'content':{"application/json":
            {"example":{
                "ID":"None",
                "UT":"None",
                "RES":"ERR"}
            }
            }
        },
    429:{'description':'Unpublished - Rate-Limited',
         'content':{"application/json":
            {"example":{
                "ID":"None",
                "UT":"None",
                "RES":"RAT"}
            }
            }
        },
    500:{'description':'Unpublished - Server issue',
         'content':{"application/json":
            {"example":{
                "ID":"None",
                "UT":"None",
                "RES":"SYS"}
            }
            }
        

    }
}

uploadResponse = {
    200:{'description':'Uploaded',
         'content':{"application/json":
            {"example":{
                "ID":"[FILE ID]",
                "UT":"[USER TOKEN]",
                "RES":"OK"}
            }
            }
        },    
    300:{'description':'Unable to upload - Banned/Limited',
         'content':{"application/json":
            {"example":{
                "ID":"None",
                "UT":"None",
                "RES":"TOS"}
            }
            }
        

    },
    409:{'description':'Unable to upload - Not logged in',
         'content':{"application/json":
            {"example":{
                "ID":"None",
                "UT":"None",
                "RES":"ERR"}
            }
            }
        },    
    413:{'description':'Unable to upload - File too big',
         'content':{"application/json":
            {"example":{
                "ID":"None",
                "UT":"None",
                "RES":"BIG"}
            }
            }
        

    },
    429:{'description':'Unable to upload - Rate-Limited',
         'content':{"application/json":
            {"example":{
                "ID":"None",
                "UT":"None",
                "RES":"RAT"}
            }
            }
        },

    500:{'description':'Unpublished - Server issue',
         'content':{"application/json":
            {"example":{
                "ID":"None",
                "UT":"None",
                "RES":"SYS"}
            }
            }
        

    }
}

deleteResponse = {
    200:{'description':'Successful removal',
         'content':{"application/json":
            {"example":{"RID":"[REMOVED POST ID]",
                        "UT": "[USER TOKEN]",
                        "RES": "OK"}
            }
            }
        },

    406:{'description':'Not post owner',
        'content':{"application/json": 
                    {"example":{
                        "UT":"None",
                        "CVP":"None",
                        "RES":"OBV"}
                    }
                }
        },
    409:{'description':'Account already exists',
         'content':{"application/json":
            {"example":{"UT":"None",
                        "CVP": "None",
                        "RES": "DUP"}
            }
            }
        },
    500:{'description':'SERVER ERROR',
         'content':{"application/json":
            {"example":{"UT":"None",
                        "CVP": "None",
                        "RES": "ERR"}
            }
            }
        },
    }