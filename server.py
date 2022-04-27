from urllib.request import Request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from numpy import source
import requests
import json
import uvicorn
import pandas as pd
import array as arr  
import sys
import math
import requests


source_lat_lng = []
rental_lat_lng = []

app = FastAPI()
origins=["*"]
app.add_middleware(CORSMiddleware,allow_origins=origins)




@app.get("/")
def root():
    return {"hello world"}

@app.get("/locationresult")
def root(location:str):
    locationresult = k_mediod(location)
    return  locationresult

# @app.get("/distance")
# def root(lat_lng_list):
#     print(lat_lng_list)
#     return 1


    
@app.get("/havershine")
def root(location:str):
    locationresult = havershine(location)
    return  locationresult

def k_mediod(location):
    
    


    location = location.lower()
    location = location.replace(" " , "")
    city = location
    

    rental_data = pd.read_csv(r"Data/Rental_Data.csv",encoding='utf-8')
    atm_data = pd.read_csv(r"Data/Atm_Data.csv",encoding='utf-8')
    hospital_data = pd.read_csv(r"Data/Hospital_Data.csv",encoding='utf-8')
    restaurent_data = pd.read_csv(r"Data/Restaurent_Data.csv",encoding='utf-8')


    rental_data = rental_data[rental_data["City"] == city]
    atm_data = atm_data[atm_data["City"] == city]
    hospital_data = hospital_data[hospital_data["City"] == city]
    restaurent_data = restaurent_data[restaurent_data["City"] == city]




    ###############3 finding distance###############

    #Geoding location
    prime_lat_lng = []
    x = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+location+'&key=AIzaSyCl4IFUvzMQSDXl8jJdIn9BtX9b5Z8Gj2A')
    jsonresposne = json.loads(x.text)
    temp_lat_lng = jsonresposne['results'][0]['geometry']['location']
    source_lat_lng.append(temp_lat_lng)


    ## Extracting rental location latitude and longitude
    rental_lat_lng = rental_data[['Latitude' , 'Longitude']].values.tolist()
    slat = source_lat_lng[0]['lat']
    slng = source_lat_lng[0]['lng']
    url_string = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+str(slat)+"%2C"+str(slng)+"&destinations="
    for i in range(len(rental_lat_lng)):
        if i == len(rental_lat_lng)-1:
            url_string = url_string + str(rental_lat_lng[i][0])
            url_string = url_string + "%2C"
            url_string = url_string + str(rental_lat_lng[i][1])
        else :
            url_string = url_string + str(rental_lat_lng[i][0])
            url_string = url_string + "%2C"
            url_string = url_string + str(rental_lat_lng[i][1])
            url_string = url_string + "%7C"     

    url_string = url_string + "&key=AIzaSyCl4IFUvzMQSDXl8jJdIn9BtX9b5Z8Gj2A"
    payload={}
    headers = {}
    response = requests.request("GET", url_string, headers=headers, data=payload)
    rentalresposne = json.loads(response.text)
    rental_lat_lng = []
    for i in range(len(rentalresposne['rows'][0]['elements'])):
        dist = rentalresposne['rows'][0]['elements'][i]['distance']['text']
        duration = rentalresposne['rows'][0]['elements'][i]['duration']['text']
        rental_lat_lng.append([dist , duration])
    

    #############################

    # # concatinaitng data
    atm_data = atm_data[["Address" , "Latitude" , "Longitude","Easting" , "Northing" , "Type"]]
    hospital_data = hospital_data[["Address" , "Latitude" , "Longitude","Easting" , "Northing" , "Type"]]
    restaurent_data = restaurent_data[["Address" , "Latitude" , "Longitude","Easting" , "Northing" , "Type"]]
    data = pd.concat([atm_data, hospital_data , restaurent_data], axis=0, ignore_index=True)


    #colouring rental
    uniquecolor = len(rental_data)
    colorlist = []
    for i in range(uniquecolor):
        colorlist.append(i)
    rental_data['color'] = colorlist

    
   

    #filering latitude and longitude
    rental_list = rental_data[["Easting" , "Northing" , "color"]].values.tolist()
    data_list = data[["Easting" , "Northing"]].values.tolist()


    data_color_list = []
    dist = 1000000000
    for itr in data_list:
        east1 = itr[0]
        north1 =  itr[1]  
        dist = sys.maxsize
        c = -1
        for rooms in rental_list:
            east2 = rooms[0]
            north2 = rooms[1]
            color_type = int(rooms[2])
            currdist = math.sqrt((pow(abs((east1 - east2)) , 2) + pow(abs((north1 - north2)) , 2)))
            if currdist < dist:
                dist = currdist
                c = color_type
        data_color_list.append(c)
    data['color'] = data_color_list

    # print(data)

    datalist = data.values.tolist()
    rental_data_list = rental_data.values.tolist()

    for i in range(len(rental_data_list)):
        rental_data_list[i].append(rental_lat_lng[i][0])
        rental_data_list[i].append(rental_lat_lng[i][1])
        print(rental_lat_lng[i][1])

    datalist = rental_data_list + datalist
    datajson = json.dumps(datalist)

    

    return datajson    





def havershine(location):
    location = location.lower()
    location = location.replace(" " , "")
    city = location

    rental_data = pd.read_csv(r"Data/Rental_Data.csv",encoding='utf-8')
    atm_data = pd.read_csv(r"Data/Atm_Data.csv",encoding='utf-8')
    hospital_data = pd.read_csv(r"Data/Hospital_Data.csv",encoding='utf-8')
    restaurent_data = pd.read_csv(r"Data/Restaurent_Data.csv",encoding='utf-8')


    rental_data = rental_data[rental_data["City"] == city]
    atm_data = atm_data[atm_data["City"] == city]
    hospital_data = hospital_data[hospital_data["City"] == city]
    restaurent_data = restaurent_data[restaurent_data["City"] == city]


    atm_data = atm_data[["Address" , "Latitude" , "Longitude" "Type"]]
    hospital_data = hospital_data[["Address" , "Latitude" , "Longitude", "Type"]]
    restaurent_data = restaurent_data[["Address" , "Latitude" , "Longitude", "Type"]]

    locationlist = rental_data[["Latitude" , "Longitude"]].values.tolist()
    atmlist = atm_data[["Latitude" , "Longitude"]].values.tolist()
    restaurentlist = restaurent_data[["Latitude" , "Longitude"]].values.tolist()
    hospitallist = hospital_data[["Latitude" , "Longitude"]].values.tolist()
    

    restaurent_sum_list = []
    i = 0
    for location in locationlist:
        currlat = float(location[1])
        currlong = location[2]
        sum = 0
        counter = 0
        for restaurent in restaurentlist:
            curr_rest_lat = float(restaurent[1])
            curr_rest_long = float(restaurent[2])
            dLat = (currlat - curr_rest_lat) * math.pi / 180.0
            dLon = (currlong - curr_rest_long) * math.pi / 180.0
            # convert to radians
            lat1 = (currlat) * math.pi / 180.0
            lat2 = (curr_rest_lat) * math.pi / 180.0
            # apply formulae
            a = (pow(math.sin(dLat / 2), 2) +
                pow(math.sin(dLon / 2), 2) *
                    math.cos(lat1) * math.cos(lat2))
            rad = 6371
            c = 2 * math.asin(math.sqrt(a))
            if rad*c <= 2:
                sum = sum + rad*c
                counter += 1
        # print(rad*c , currlat , curr_rest_lat , currlong , curr_rest_long)
    if counter==0:
        restaurent_sum_list.append([currlat , currlong , sys.maxint , i])
    else:
        restaurent_sum_list.append([currlat , currlong , sum/counter , i])
    i += 1

    restaurent_sum_list = sorted(restaurent_sum_list, key = lambda x: float(x[2]))


    atm_sum_list = []
    i = 0
    for location in locationlist:
        currlat = float(location[1])
        currlong = location[2]
        sum = 0
        counter = 0
        for atm in atmlist:
            curr_rest_lat = atm[1]
            curr_rest_long = atm[2]
            dLat = (currlat - curr_rest_lat) * math.pi / 180.0
            dLon = (currlong - curr_rest_long) * math.pi / 180.0
            # convert to radians
            lat1 = (currlat) * math.pi / 180.0
            lat2 = (curr_rest_lat) * math.pi / 180.0
            # apply formulae
            a = (pow(math.sin(dLat / 2), 2) +
                pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat2))
            rad = 6371
            c = 2 * math.asin(math.sqrt(a))
            if rad*c <= 2:
                sum += rad*c
                counter += 1
    if counter==0:
        atm_sum_list.append([currlat , currlong , 10000 , i])
    else:
        atm_sum_list.append([currlat , currlong , sum/counter , i])
    i += 1

    atm_sum_list = sorted(atm_sum_list, key = lambda x: float(x[2]))

    hospital_sum_list = []
    i = 0
    for location in locationlist:
        currlat = float(location[1])
        currlong = location[2]
        sum = 0
        counter = 0
        for hospital in hospitallist:
            curr_rest_lat = hospital[1]
            curr_rest_long = hospital[2]
            dLat = (currlat - curr_rest_lat) * math.pi / 180.0
            dLon = (currlong - curr_rest_long) * math.pi / 180.0
            # convert to radians
            lat1 = (currlat) * math.pi / 180.0
            lat2 = (curr_rest_lat) * math.pi / 180.0
            # apply formulae
            a = (pow(math.sin(dLat / 2), 2) +
                pow(math.sin(dLon / 2), 2) *
                    math.cos(lat1) * math.cos(lat2))
            rad = 6371
            c = 2 * math.asin(math.sqrt(a))
            if rad*c <= 2:
                sum += rad*c
                counter += 1
    if counter == 0:
        hospital_sum_list.append([currlat , currlong , 1000 , i])
    else:
        hospital_sum_list.append([currlat , currlong , sum/counter , i])
    i += 1

    hospital_sum_list = sorted(hospital_sum_list, key = lambda x: float(x[2]))
    
    mydict = {}
    for k in range(len(restaurent_sum_list)):
        if restaurent_sum_list[k][3] in mydict :
            val = mydict[restaurent_sum_list[k][3]]
            mydict.update({restaurent_sum_list[k][3] : val+k})
        else:
            mydict.update({restaurent_sum_list[k][3] : k})
        
        if atm_sum_list[k][3] in mydict :
            val = mydict[atm_sum_list[k][3]]
            mydict.update({atm_sum_list[k][3] : val+k})
        else:
            mydict.update({atm_sum_list[k][3] : k})
        
        if hospital_sum_list[k][3] in mydict :
            val = mydict[hospital_sum_list[k][3]]
            mydict.update({hospital_sum_list[k][3] : val+k})
        else:
            mydict.update({hospital_sum_list[k][3] : k})
    sorted_dict = sorted(mydict.items(), key = lambda kv:(kv[1], kv[0]))
    for ele in sorted_dict:
        print(locationlist[ele[0]][2])

    print(locationlist)
uvicorn.run(app, host="0.0.0.0", port=8000)




