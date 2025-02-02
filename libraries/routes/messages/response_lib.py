messageReadResponse = {
    200:{'description':'Successful message read out',
         'content':{"application/json":
            {"example":{
                "DAT":"[MESSAGE ID]",
                "TYP":"Read",
                "STC":200,
                "RES":"OK"}
            }
            }
        }
    }

messageReadDescription = "Get message IDs"

messagePostResponse = {
    200:{'description':'Message sent successfully',
        'content':{"application/json": 
                    {"example":{
                        "DAT":"[MESSAGE ID]",
                        "STC":"Post",
                        "STC":200,
                        "RES":"OK"}
                    }
                }
        },
    500:{'description':'Server issue',
        'content':{"application/json": 
                    {"example":{
                        "DAT":"ERR",
                        "STC":"ERR",
                        "STC":500,
                        "RES":"ERR"}
                    }
                }
        }    
    }

messagePostDescription = "Send a message"