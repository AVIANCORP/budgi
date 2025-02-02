listResponse = {
                    200:{'description':'Successful listing',
                        'content':{"application/json":
                                {"example":{
                                    "UT":"[Your User Token]",
                                    "DAT":"['TOKEN RESPONSE ID','TOKEN RESPONSE ID']",
                                    "RES":"[Response Code]",
                                    "STC":200}
                                }
                            }
                        },
                    500:{'description':'Server issue',
                        'content':{"application/json":
                            {"example":{
                                "UT":"None",
                                "DAT":"None",
                                "RES":"ERR",
                                "STC":500}
                            }
                        }
                    }
                }

loginResponse = {
    200:{'description':'Successful login',
        'content':{"application/json": 
                    {"example":{
                        "UT":"[USER TOKEN]",
                        "CVP":"[CLIENT VERIFICATION PHRASE]",
                        "RES":"OK"}
                    }
                }
        },
    300:{'description':'Failed login',
        'content':{"application/json": 
                    {"example":{
                        "UT":"None",
                        "CVP":"None",
                        "RES":"ERR"}
                    }
                }
        },
    500:{'description':'Server issue',
        'content':{"application/json": 
                    {"example":{
                        "UT":"None",
                        "CVP":"None",
                        "RES":"ERR"}
                    }
                }
        }    
    }

registerResponse = {
    200:{'description':'Successful registration',
         'content':{"application/json":
            {"example":{"UT":"[USER TOKEN]",
                        "CVP": "[CLIENT VERIFICATION PHASE]",
                        "RES": "OK"}
            }
            }
        },

    406:{'description':'TOS terms are not accepted',
        'content':{"application/json": 
                    {"example":{
                        "UT":"None",
                        "CVP":"None",
                        "RES":"TOS"}
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