disbandResponse = {
    200:{'description':'Successful group deletion.',
         'content':{"application/json":
            {"example":{
                "GI":"[GROUP ID]",
                "MOD":"None",
                "RES":"OK"}
            }
            }
        }
    }

checkInResponse = {
    200:{'description':'Successful group interaction',
        'content':{"application/json": 
                    {"example":{
                        "GI":"[GROUP ID]",
                        "INT":"[INTERACTION DATA]",
                        "RES":"OK"}
                    }
                }
        },
    300:{'description':'Improper group privileges',
        'content':{"application/json": 
                    {"example":{
                        "GI":"None",
                        "INT":"[INTERACTION DATA]",
                        "RES":"ERR"}
                    }
                }
        },
    500:{'description':'Server issue',
        'content':{"application/json": 
                    {"example":{
                        "GI":"None",
                        "INT":"[INTERATION DATA]",
                        "RES":"ERR"}
                    }
                }
        }    
    }

formulationResponse = {
    200:{'description':'Successful group creation',
         'content':{"application/json":
            {"example":{"UT":"[USER TOKEN]",
                        "MOD": "[USER PUBLIC TOKEN]",
                        "RES": "OK"}
            }
            }
        },

    409:{'description':'Group already exists',
         'content':{"application/json":
            {"example":{"UT":"[USER TOKEN]",
                        "MOD": "None",
                        "RES": "DUP"}
            }
            }
        },

    500:{'description':'Server error',
         'content':{"application/json":
            {"example":{"UT":"[USER TOKEN]",
                        "MOD": "None",
                        "RES": "ERR"}
            }
            }
        },
    }