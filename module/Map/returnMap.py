#based on mapTest.py. Seperate each component to functions
import cv2
from cv2 import IMWRITE_JPEG2000_COMPRESSION_X1000 
import numpy as np
import math
from sympy import *
import os
import shutil
from fastapi.responses import StreamingResponse

points = np.array([
    [260, 1290], [260 , 1098], [260, 905], [260, 695], [417, 695], [417, 570], [616, 570],
    [666, 695], [666, 905], [829, 800], [829, 905], [829, 970], [829, 1098], [829, 1290],
    [904, 1253], [904, 970], [939, 869], [939, 746], [939, 570], [939, 377], [939, 332], [939, 905],
    [1007, 970], [1007, 1167], [1007, 1253], [1149, 1253], [1149, 1167], [1149, 970],
    [1149, 869], [1278, 1253], [1065, 746], [1149, 746], [1265, 746], [1065, 435], [1065, 332] , [1265, 332],
    [1265, 435], [1440, 332], [1440, 746], [1440, 869], [1440, 970], [1440, 1100], [1440, 1182],
    [1440, 1288], [1617, 1288], [1617, 1100], [1617, 869], [1790, 147], [1790, 252], [1790, 332],
    [1790, 512], [1790, 702], [1790, 778], [1790, 869], [1790, 1100], [1790, 1133], [1790, 1288], 
    [1790, 1248], [2094, 252], [2094, 512], [1981, 512], [1981, 332], [1981, 702], [2094, 778], 
    [2060, 778], [2060, 869], [2060, 1133], [2060, 1248]
])


firstRest = {'EE': [[829, 800], [829, 905], [939, 869], [1790, 869], [1790, 252], [2094, 252]],
            'MA' : [[829, 800], [829, 905], [939, 869], [1790, 869], [1790, 512], [1850, 512]],
            'T2' : [[829, 800], [829, 905], [939, 869], [1790, 869], [1790, 778], [2094, 778], [2094, 512]],
            'E2' : [[829, 800], [829, 905], [939, 869], [1790, 869], [1790, 778], [2094, 778]],
            'IB' : [[829, 800], [829, 905], [939, 869], [2060, 869], [2060, 1248]],
            'AD' : [[829, 800], [829, 905], [939, 869], [1617, 869], [1617, 985]],
            'E1' : [[829, 800], [829, 905], [939, 869], [939, 746], [1149, 746]],
            'T4' : [[829, 800], [829, 905], [939, 869], [939, 940], [1007, 940]],
            'RB' : [[829, 800], [829, 905], [829 , 970], [904, 970] , [904, 1253], [1149, 1253]],
            'T1' : [[829, 800], [829, 905], [829 , 970], [904, 970] , [904, 1253]],
            'LB' : [[829, 800], [829, 905], [939, 869], [1428, 869], [1428, 1182]],
            'TR' : [[829, 800], [829, 905], [666, 905], [260 , 905], [260 , 1098]],
            'IA' : [[829, 800], [829, 905], [666, 905], [260 , 905], [220, 800]],
            'S' : [[829, 800], [829, 905], [939, 869], [939, 746], [939, 570], [750, 570]],
            'T3' : [[829, 800], [829, 905], [939, 869], [939, 746], [939, 570], [939, 377]],
            'GYM': [[829, 800], [829, 570], [417, 570]],
            'D1' : [[829, 800], [829, 905], [939, 869], [939, 746], [1065, 746], [1065, 252]],
            'D2' : [[829, 800], [829, 905], [939, 869], [939, 746], [1428 , 746], [1428, 252]],
            'D3' : [[829, 800], [829, 905], [939, 869], [939, 746], [1428 , 746], [1428, 332], [1617, 332], [1617, 252]]
            }

staffRest = {'EE': [[850, 658], [939, 658], [939, 746], [1065, 746], [1065, 332], [1790, 332], [1790, 252], [2094, 252]],
            'MA' : [[850, 658], [939, 658], [939, 869], [1790, 869], [1790, 512], [1850, 512]],
            'T2' : [[850, 658], [939, 658], [939, 869], [1790, 869], [1790, 778], [2094, 778], [2094, 512]],
            'E2' : [[850, 658], [939, 658], [939, 869], [1790, 869], [1790, 778], [2094, 778]],
            'IB' : [[850, 658], [939, 658], [939, 869], [2060, 869], [2060, 1248]],
            'AD' : [[850, 658], [939, 658], [939, 869], [1617, 869], [1617, 985]],
            'E1' : [[850, 658], [939, 658], [939, 746], [1149, 746]],
            'T4' : [[850, 658], [939, 658], [939, 869], [939, 940], [1007, 940]],
            'RB' : [[850, 658], [939, 658], [904, 1253], [1149, 1253]],
            'T1' : [[850, 658], [939, 658], [904, 1253]],
            'LB' : [[850, 658], [939, 658], [939, 869], [1428, 869], [1428, 1182]],
            'TR' : [[850, 658], [939, 658], [939, 905], [666, 905], [260 , 905], [260 , 1098]],
            'IA' : [[850, 658], [939, 658], [939, 905], [666, 905], [260 , 905], [220, 800]],
            'S' : [[850, 658], [939, 658], [939, 570], [750, 570]],
            'T3' : [[850, 658], [939, 658], [939, 570], [939, 377]],
            'GYM': [[850, 658], [829, 658],[829, 570], [417, 570]],
            'D1' : [[850, 658], [939, 658], [939, 746], [1065, 746], [1065, 252]],
            'D2' : [[850, 658], [939, 658],  [939, 746], [1428 , 746], [1428, 332], [1617, 332], [1617, 252]],
            'D3' : [[850, 658], [939, 658],  [939, 746], [1428 , 746], [1428, 252]]
            }

thirdRest = {'EE': [[2034, 558], [2034, 512], [2094, 512], [2094, 252]],
            'MA' : [[2034, 558], [2034, 512], [1850, 512]],
            'T2' : [[2034, 558], [2034, 512], [2094, 512]],
            'E2' : [[2034, 558], [2034, 512], [2094, 512], [2094, 778]],
            'IB' : [[2034, 558], [2034, 512], [2094, 512], [2094, 869], [2060, 869], [2060, 1248]],
            'AD' : [[2034, 558], [2034, 512], [1981, 512], [1981, 702], [1790, 702], [1790, 869], [1617, 869], [1617, 985]],
            'E1' : [[2034, 558], [2034, 512], [1981, 512], [1981, 702], [1790, 702], [1790, 869], [1428, 869], [1428, 746], [1149, 746]],
            'T4' : [[2034, 558], [2034, 512], [1981, 512], [1981, 702], [1790, 702], [1790, 869], [1149, 869], [1149, 940], [1007, 940]],
            'RB' : [[2034, 558], [2034, 512], [1981, 512], [1981, 702], [1790, 702], [1790, 869], [1149, 869], [1149, 970], [904, 970], [904, 1253], [1149, 1253]],
            'T1' : [[2034, 558], [2034, 512], [1981, 512], [1981, 702], [1790, 702], [1790, 869], [1149, 869], [1149, 970], [904, 970], [904, 1253]],
            'LB' : [[2034, 558], [2034, 512], [1981, 512], [1981, 702], [1790, 702], [1790, 869], [1428, 869], [1428, 1182]],
            'TR' : [[2034, 558], [2034, 512], [1981, 512], [1981, 702], [1790, 702], [1790, 869], [939, 869], [829, 905], [260, 905], [260, 1098]],
            'IA' : [[2034, 558], [2034, 512], [1981, 512], [1981, 702], [1790, 702], [1790, 869], [939, 869], [829, 905], [260, 905], [220, 800]],
            'S' : [[2034, 558], [2034, 512], [2034, 332], [939, 332], [939, 570], [750, 570]],
            'T3' : [[2034, 558], [2034, 512], [2034, 332], [939, 332], [939, 377], [829, 377]],
            'GYM': [[2034, 558], [2034, 512], [2034, 332], [939, 332], [939, 570], [417, 570]],
            'D1' : [[2034, 558], [2034, 512], [2034, 332], [1065, 332], [1065, 252]],
            'D2' : [[2034, 558], [2034, 512], [2034, 332], [1428, 332], [1428, 252]],
            'D3' : [[2034, 558], [2034, 512], [2034, 332], [1617, 332] , [1617, 252]]
            }

building = [[2094, 252], [1850, 512], [2094, 512], [2094, 778], [2060, 1248], [1617, 985], [1149, 746], [1007, 940], 
            [1149, 1253], [904, 1253], [1428, 1182], [260, 1098], [220, 800], [750, 570], [829, 377], [417, 570], [1065, 252],
            [1617, 252], [1428, 252]]

buildingName = ['EE', 'MA', 'T2', 'E2', 'IB', 'AD', 'E1', 'T4', 'RB', 'T1', 'LB',
                'TR', 'IA', 'S', 'T3', 'GYM', 'D1', 'D2', 'D3']

############ Process ##############
def addFolder(ID):
    path = './module/Map/'+ID
    if not os.path.isdir(path):
        os.mkdir(path)
        return 'add'
    return 'not yet'

def deleteFolder(ID):
    path = './module/Map/'+ID
    if ID == 'img':
        return 'system error'
    elif os.path.isdir(path):
        shutil.rmtree(path)
        return 'finished'
    else:
        return 'failed'
        
def getFile(ID, picType):
    folderPath = './module/Map/'+ID
    filePath = folderPath + '/'+ picType +'.jpg'

    if os.path.isdir(folderPath):
        return StreamingResponse(open(filePath , mode = 'rb') , media_type= 'image/jpeg')
    else:
        return 'no file'
#######################################


############ Picture editing ##############
def transform(latlng):
    global buildingName , building
    origin = [25.01390648525629 , 121.54461886896823 ]
    x_axis = [25.011100933885338 , 121.54117377377323925]
    y_axis = [25.01571636583346, 121.54266712547633]
    
    a = (x_axis[0] - origin[0])/(2560-128)
    #print(a)
    b = (x_axis[1] - origin[1])/(2560-128)
    #print(b)
    m = (y_axis[0] - origin[0])/(1440-128)
    #print(m)
    n = (y_axis[1] - origin[1])/(1440-128)
    #print(b)

    lat_c = latlng[0] - 25.01390648525629
    lng_c = latlng[1] - 121.54461886896823
    #to solve x and y
    x = Symbol('x')
    y = Symbol('y')

    f1 = x*a + y*m - lat_c
    f2 = x*b + y*n - lng_c


    sol = solve((f1, f2) , x, y)
  
    x = int(sol.get(x))
    y = int(sol.get(y))

    name = None
    val = None
    add = 0

    #find the shortest distance
    for i , j in building :
        if val == None or (math.sqrt((i-x)**2 + (j-y)**2) < val) :
            val = math.sqrt((i-x)**2 + (j-y)**2)
            name = buildingName[add]

        add += 1

    print('end tranform')
    return name
    
def route(start, end, img1):
    global thirdRest , firstRest , staffRest
    load = None

    """if end[0] == '[' and end[-1] == ']':
        print('list')
        end = end[1:-1].split(',') 
        end = list(map(float, end))
        print('change latlng in to building name')
        end = transform(end)"""

    if start ==1:
        load = firstRest
        for i  in range(1 , len(load[end])):
            cv2.line(img1,(load[end][i-1][0],load[end][i-1][1]),(load[end][i][0],load[end][i][1]),(0,0,255), 3)
    elif start == 3:
        load = thirdRest
        for i  in range(1 , len(load[end])):
            cv2.line(img1,(load[end][i-1][0],load[end][i-1][1]),(load[end][i][0],load[end][i][1]),(0,0,255), 3)
    elif start == 4:
        load = staffRest
        for i  in range(1 , len(load[end])):
            cv2.line(img1,(load[end][i-1][0],load[end][i-1][1]),(load[end][i][0],load[end][i][1]),(0,0,255), 3)
    else :
        print('error')

    return img1


def resize_img(img, scale_percent=25):

    width = int(img.shape[1] * scale_percent / 100) 
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resize_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)  
    
    return resize_img


def Deliver(position, img1 , img2):

    #resize the img2
    img2 = resize_img(img2, scale_percent = 25)
    img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 254, 255, cv2.THRESH_BINARY)

    #receive the sizeInfo from img2
    rows, cols, channels = img2.shape

    #linear transform
    origin = [25.01390648525629 , 121.54461886896823 ]
    x_axis = [25.011100933885338 , 121.54117377377323925]
    y_axis = [25.01571636583346, 121.54266712547633]
    
    a = (x_axis[0] - origin[0])/(2560-128)
    b = (x_axis[1] - origin[1])/(2560-128)
    m = (y_axis[0] - origin[0])/(1440-128)
    n = (y_axis[1] - origin[1])/(1440-128)

    lat_c = position[0] - 25.01390648525629
    lng_c = position[1] - 121.54461886896823
    x = Symbol('x')
    y = Symbol('y')

    f1 = x*a + y*m - lat_c
    f2 = x*b + y*n - lng_c
    sol = solve((f1, f2) , x, y)
  
    x = int(sol.get(x))
    y = int(sol.get(y))

    roi = img1[y:y+rows, x:x+cols]
    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi, roi, mask = mask)
    mask_inv = cv2.bitwise_not(mask)
    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(img2, img2, mask = mask_inv)
    # Put logo in ROI and modify the main image
    dst = cv2.add(img1_bg,img2_fg)
    img1[y:y+rows, x:x+cols] = dst

    #write file
    print( x, '  ', y)
    return img1

def Consumer(start,end ,img1 , img2):

    #resize the img2
    img2 = resize_img(img2, scale_percent = 25)

    img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 254, 255, cv2.THRESH_BINARY)

    #receive the sizeInfo from img2
    rows, cols, channels = img2.shape

    load = None
    if start ==1:
        load = firstRest
    elif start == 3:
        load = thirdRest
    elif start == 4:
        load = staffRest
    else :
        print('error')

    """if end[0] == '[' and end[-1] == ']':
        end = end[1:-1].split(',') 
        end = list(map(float, end))
        print('change latlng in to building name')
        end = transform(end)"""

    x = load[end][-1][0] -64
    y = load[end][-1][1] -128
    roi = img1[y:y+rows, x:x+cols]


    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi, roi, mask = mask)
    mask_inv = cv2.bitwise_not(mask)
    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(img2, img2, mask = mask_inv)
    # Put logo in ROI and modify the main image
    dst = cv2.add(img1_bg,img2_fg)
    img1[y:y+rows, x:x+cols] = dst

    #write file
    print( x, '  ', y)
    return img1

def produceMap(start : int , end , deliver , ID):

    #img1
    file_name = "./module/Map/img/ntust_map.png"
    img1 = cv2.imread(file_name)

    #img2
    file_name = "./module/Map/img/deliver.png"
    img2 = cv2.imread(file_name)

    #img3
    file_name = "./module/Map/img/consumer.png"
    img3 = cv2.imread(file_name)

    addFolder(ID)#add the folder for specific order

    if end[0] == '[' and end[-1] == ']':
        end = end[1:-1].split(',') 
        end = list(map(float, end))
        print('change latlng in to building name')
        end = transform(end)


    if deliver != None:
        deliver = deliver[1:-1].split(',') 
        if (deliver[0] != 'null' ):
            print('pin the position of deliver')
            deliver[0] = float(deliver[0])
            deliver[1] = float(deliver[1])
            img1 = Deliver(deliver, img1, img2)
            img1 = Consumer(start, end, img1, img3)
        cv2.imwrite(f'./module/Map/{ID}/deliver.jpg', img1)

    

    if(start != None) and (end != None):
        print('doing routing')
        img1 = route(start, end, img1)
        img1 = Consumer(start, end, img1, img3)
        cv2.imwrite(f'./module/Map/{ID}/route.jpg', img1)
    
    return 'finished'
    

