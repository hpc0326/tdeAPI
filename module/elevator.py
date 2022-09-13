import random
import json

def elevator_response():

    busy_level = ["red" , "yello" , "green"]
    up_or_down = ["up" , "down" , "stop"]
    current_floor = random.randint(1,11)

    information ={
                    
                    'TR':[
                        {'Name' : 'front_left' ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } , 

                        {"Name" : "left_rear" ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } ,

                        {"Name" : "right_rear" ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } ,
                        
                        {"Name" : "front_right" ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        }
                        ]
                    ,

                    
                    'IB':[
                        {'Name' : 'front_left' ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } , 

                        {"Name" : "left_rear" ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } ,

                        {"Name" : "right_rear" ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } ,
                        
                        {"Name" : "front_right" ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        },

                        {"Name" : "cargo" ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } ,

                        {"Name" : "scenery" ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        }
                        ]
                    ,
                        
                    
                    'EE':[
                        {'Name' : 'elevator' ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } 
                        ]
                    ,

                    
                    'MA':[
                        {'Name' : 'elevator' ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } 
                        ]
                    ,

                    
                    'E1':[
                        {'Name' : 'elevator' ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } 
                        ]
                    ,

                    
                    'E2':[
                        {'Name' : 'left' ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } , 

                        {"Name" : "right" ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } ,
                        ]
                    ,

                    
                    'T3':[
                        {'Name' : 'left' ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } , 

                        {"Name" : "right" ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } 
                        ]
                    ,

                    
                    'T4':[
                        {'Name' : 'left' ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } , 

                        {"Name" : "middle" ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } ,

                        {"Name" : "right" ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        }
                        ]
                    ,

                    
                    'S':[
                        {'Name' : 'elevator' ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } 
                        ]
                    ,

                    
                    'RB':[
                        {'Name' : 'left' ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } , 

                        {"Name" : "right" ,
                        'Busy_Level' : busy_level[random.randint(0,2)],
                        'Direction' : up_or_down[random.randint(0,2)],
                        'Current_Floor' : random.randint(1,11)
                        } 
                        ]
                    
                }
    #test = {"cool": "guys"}
    #test = '{"cool": "guys"}'
    inform = json.dumps(information)
    inform = json.loads(inform)
    return inform


