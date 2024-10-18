from dotenv import load_dotenv
load_dotenv()

import time
import os
import requests
from supabase import create_client
import json

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

#פונקציה שמקבלת את הפרמטרים ומכניסה אותם למאגר נתונים
def insert(timestamp,place):
    input = supabase.table("alert_db").insert({"time":time.ctime(timestamp),"place":place}).execute()

#חיבור לצבע אדום
def responce():
    return requests.get("https://api.tzevaadom.co.il/notifications")

#הכנסת הודעה התחלתית
test_json = [{'notificationId': '1ecd0595-2dc7-459b-a8a6-c0f2948045ae', 'time': 1729174158, 'threat': 0, 'isDrill': False, 'cities': ['קריית שמונה']}]
old_data = test_json[0]
old_id = old_data['notificationId']

## בדיקה האם יש קישור
condition = responce().status_code == 200

if condition:
    print("running")

#לולאה ראשית
while condition:
    data_json = json.loads(responce().text)
    #בדיקה אם יש צבע אדום
    if data_json != []:
        print("alert!")
        #יצירת משתנה לתוכו נזין את המידע מההתראה
        data = data_json[0]
        new_id = data['notificationId']
        is_drill = data['isDrill']

        #בדיקה שזו לא הזעקת תרגול
        if is_drill == False:
            
            #בדיקה שזה לא הודעה שהוכנסה כבר
            if new_id != old_id:
                old_id = new_id
                insert(data['time'],data['cities'])
                print("inserting")
                print(data_json)
    time.sleep(1)

print(responce.status_code)
