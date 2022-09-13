import requests as rq
import json
import pandas as pd
from fastapi import FastAPI
import matplotlib.pyplot as plt
import xlsxwriter
from fastapi.responses import StreamingResponse , FileResponse
from io import BytesIO


def dict_to_list(diction):
    temp = list()
    for key , value in diction.items():
        tmp = list()
        tmp.append(key)
        for i in value:
            tmp.append(i)
        temp.append(tmp)
    return temp

#format : "2022-08-01T12:08:38.477Z"
def timeAnalysis(timeAna, time : str):
    
    hr = time[11:13]
    for i in timeAna.keys():
        if i == hr:
            timeAna[hr][0] += 1

    return timeAna

def timeRange(start:str, end:str , time :str ):

    temp = time[0:4]+time[5:7]+time[8:10]
    temp , start , end  = int(temp) , int(start) , int(end)
    if temp > end or temp < start:
        return False
    else:
        return True

def dataWriter(storename , start  , end):

    #####local data#########
    path = './module/Data/jsondata.json'
    file = open(path)
    content = json.load(file)['msg']
    file.close()

    ############get order list########
    """url = 'http://140.118.122.148:30307/getallorder'
    content = json.loads(rq.get(url).text)['msg']"""
    
    print(content)
    ##################################

    name = storename

    #####common variable#####
    #output = BytesIO()
    writer = pd.ExcelWriter('output.xlsx', engine= 'xlsxwriter')
    item = dict()
    #itemlist = list()
    timeAna = {
        '06':[0],
        '07':[0],
        '08':[0],
        '09':[0],
        '10':[0],
        '11':[0],
        '12':[0],
        '13':[0],
        '14':[0],
        '15':[0],
        '16':[0],
        '17':[0],
        '18':[0],
        '19':[0]
    }
    
    #################calculate amount##################
    for i in content:#per order
        
        #if order-create time not in the specific date range
        if  start !=  None and end != None and not timeRange(start , end  , i['CreatedAt']) :
            continue
        
        timeAna = timeAnalysis(timeAna , i['CreateAt'])
        if  i['Storename'] == name and i['Status'] == 'finished':
            for k in i['Dishes']:#per dish
                if not k['Name'] in item.keys():
                    item[k['Name']] = [0, 0]
                    item[k['Name']].append(k['Price'])
                print(item)
                item[k['Name']][0] = int(k['Quantity']) + item[k['Name']][0] #amount of each item
                item[k['Name']][1] = k['Price']*int(k['Quantity']) + item[k['Name']][1] #revenue of each item
            
    #############################################

    #dict to list
    itemlist = dict_to_list(item)
    timeAnalist = dict_to_list(timeAna)

    ######inset product sales info################
    data1 = pd.DataFrame(itemlist, columns=['商品', '數量', '金額', '單價' ])
    data1.to_excel(writer, sheet_name='sheet1' , index = False)

    #####declare workbook and worksheet1#########
    workbook = writer.book
    worksheet1 = writer.sheets['sheet1']

    #####total sales number of each product##########
    chart1 = workbook.add_chart({'type' : 'column'})
    maxRow , maxCol = data1.shape
    chart1.add_series({'values' : ['sheet1', 1 , 1 , maxRow , 1],
                        'name' : '銷售數',
                        'categories': ['sheet1', 1, 0, maxRow, 0]})

    chart1.set_title({'name':'商品銷售數量'})
    chart1.set_x_axis({'name' : '商品名稱'})
    chart1.set_y_axis({'name' : '銷售數量'})
    chart1.set_style(11)


    ########total income####################
    chart2 = workbook.add_chart({'type': 'column'})
    chart2.add_series({'values': ['sheet1' , 1, 2 , maxRow , 2],
                        'name': '商品銷售額',
                        'categories' : ['sheet1', 1, 0, maxRow, 0]})

    chart2.set_title({'name':'商品銷售總額'})
    chart2.set_x_axis({'name':'商品名稱'})
    chart2.set_y_axis({'name' : '銷售金額'})
    chart2.set_style(10)

    ########time Analyze######################
    data2 = pd.DataFrame(timeAnalist , columns = ['時間', '訂單數'])
    data2.to_excel(writer , sheet_name = 'sheet2' , index= False)
    worksheet2 = writer.sheets['sheet2']

    maxRow, maxCol = data2.shape
    chart3 = workbook.add_chart({'type':'column'})
    chart3.add_series({
        'values': ['sheet2' , 1 ,1 , maxRow , 1],
        'name' : '訂單數',
        'categories':['sheet2', 1, 0, maxRow, 0]
    })

    chart3.set_title({'name':'分時訂單數量'})
    chart3.set_x_axis({'name':'時段'})
    chart3.set_y_axis({'name':'訂單數目'})
    chart3.set_style(10)

    #########insert the charts into worksheet#######
    worksheet1.insert_chart('E2', chart1, {'x_offset': 25, 'y_offset': 10})
    worksheet1.insert_chart('E20', chart2, {'x_offset': 25, 'y_offset': 10})
    worksheet2.insert_chart('E2', chart3, {'x_offset': 25, 'y_offset': 10})
    workbook.close()

    
    head = {
        'Content-Disposition': 'attachment; filename="financial_statement.xlsx"'
    }
    
    print(timeAna)
    return FileResponse('output.xlsx' , headers = head)

def hello():
    print('hello')