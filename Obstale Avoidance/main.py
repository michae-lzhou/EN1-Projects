import time
from Subs.CreateLib import Create
import requests
import os

APIKey = 'keyBGBJH9U4l7kKyv'
BaseID = 'appuRZnz832l9JERD'
TableName = 'Robot'
RecID_X = 'recyIlQvT1F5Jd1ny'
RecID_Y = 'recfKerOIa8C9rkF3'
RecID_Theta = 'receOe10qgy8r7CH8'
IDs = [RecID_X,RecID_Y,RecID_Theta]

def AskAirtable():
    URL = 'https://api.airtable.com/v0/' + BaseID + '/' + TableName + '?api_key=' + APIKey
    values = [0.0,0.0,0.0]
    names = ['','','']

    try:
        r = requests.get(url = URL, params = {})
        data = r.json()
        for command in data['records']:
            values[IDs.index(command['fields']['RecordID'])] = command['fields']['Value']    
            names[IDs.index(command['fields']['RecordID'])] = command['fields']['Name']
        return values
    except:
        return None

def main():
    motion = Create('/PotatoHead')

    speed = 1.0
    turn = 1.0
    (x, y, z, th) = (0.0,0.0,0.0,0.0)

    try:
        print('ready to drive',end='')
        
        while True:
            key = AskAirtable()
            if key:  #make sure you read data
                x = key[0]
                y = key[1]
                z = 0.0
                th = key[2]
                
                motion.twist(x, y, z, th, speed, turn)
                print('.',end='')
                
            else:
                (x, y, z, th) = (0.0,0.0,0.0,0.0)
            time.sleep(0.1)
                    
    except Exception as e:
        print(e)

    finally:
        motion.twist(0.0, 0.0, 0.0, 0.0, 0.5, 1.0)

os.environ['ROS_DOMAIN_ID']="14"
main()
