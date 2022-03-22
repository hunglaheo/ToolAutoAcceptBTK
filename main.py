#!mitmdump -s
import requests
import http.client as pager
from logging import StringTemplateStyle, fatal
import queue
import mitmproxy
from mitmproxy import ctx, http,websocket
import json
import re
import asyncio
import random
import time
from datetime import datetime
employeeIds=["2e7oXtRDZ74NJdE9j", "8EQXJMuNRmhmMZsGo", "AcdEsdaiExqnQtxD8", "GsEbARAMKL39MckJW", "RnCLzibDqKfZ8DZCi", "WQ7F4GcpRsZ8ysqAa", "Z36QkasdQnzrym3jC", "hrKQ2D6gZFXCu6erC", "jQX5yMD5vNFa7bHPN", "qrLjuSCwwRt289JMW", "rmvb22PYnSdF8RAdB"]
curentEmployeeIds=5
from mitmproxy.proxy import protocol
#def websocket_message(flow:websocket.WebSocketFlow):
def websocket_message(flow: http.HTTPFlow): 
    global curentEmployeeIds
    #flow.messages[-1].content=""
    data=flow.messages[-1].content
    data=data.replace("'", "\"")
    data=data.replace("True", "\"True\"")
    data=data.replace("False", "\"False\"")
    data=data.replace("None", "\"None\"")
    data=data.replace("\n","")
    #print(vars(flow.messages[-1]))
    hopLe = False
    try:
        data=json.loads(data)
        hopLe = True
    except:
        flow.messages[-1].content=""
        print("Co loi xay ra:" + data)
    if hopLe:
        if("msg" in data.keys()):
            if "id" not in data.keys():
                #print(data)
                pass
            elif type(data["id"]) == str and data["msg"] == "result":
                try:
                    if int(data["id"]) > 14:
                        print(data)
                except:
                    pass
            else:
                print(data)
            isLate = False

            if((data["msg"]=="added") and ("acceptedTasker" not in data["fields"]) and("taskPlace" in data["fields"])):
                print("Co don moi")
                if data["fields"]["taskPlace"]["city"] == "Bình Dương":
                    if (data["fields"]["taskPlace"]["district"] != "Dĩ An") or (data["fields"]["taskPlace"]["district"] != "Thuận An") or (data["fields"]["taskPlace"]["district"] != "Thủ Dầu Một") :
                        isLate = True
                if "T6 19201 Riviera Point" in data["fields"]["address"]: #Block khách ngu
                    isLate = True
                if (data["fields"]["askerId"] == "x619d946cd08349862cb633e6") or( data["fields"]["askerId"] == "x61e7ab4d12f7b163a7af5709"):
                    isLate = True
                if "covidInfos" in data["fields"]:
                    if (data["fields"]["covidInfos"][0]["status"]== True ) or (data["fields"]["covidInfos"][1]["status"]==True):
                        isLate = True
                dt_object = datetime.fromtimestamp(data["fields"]["date"]["$date"]//1000)
                if ((data["fields"]["taskPlace"]["district"] == "Cần Giờ") or (data["fields"]["taskPlace"]["district"] == "Củ Chi")):
                    isLate = True
                if data["fields"]["serviceId"] == "QFPAZgMSejyMRgNWb":
                    if (dt_object.weekday()>4):
                        if (dt_object.hour >= 17) or (dt_object.hour < 8):
                            isLate = True
                    else:
                        if dt_object.hour == 17 and dt_object.minute > 30:
                            isLate = True
                        if dt_object.hour > 17:
                            isLate = True
                        if (dt_object.hour < 8):
                            isLate = True
                else:
                    if dt_object.hour == 18 and dt_object.minute > 0:
                        isLate = True
                    if dt_object.hour > 18:
                        isLate = True
                    if (dt_object.hour < 8):
                        isLate = True
                if dt_object.month == 4 and dt_object.day == 30:
                    isLate = True
                if dt_object.month == 5 and dt_object.day == 1:
                    isLate = True
                if dt_object.month == 9 and dt_object.day == 2:
                    isLate = True   
                if dt_object.month == 4 and dt_object.day == 10:
                    isLate = True
                if data["fields"]["askerId"] == "hc5WnW8RhaEwDgMbc":
                    isLate = True
                if data["fields"]["askerId"] == "tHveMDhY2CWycCbHe":
                    isLate = True
                if "masteri T2 block B floor 26 room 6" in json.dumps(data):
                    isLate = True
                if "Block P1 Apartment 12-05" in json.dumps(data):
                    isLate = True
                #if isLate == True:
                    #sendErrorPagerDyty("Đơn ở " + data["fields"]["taskPlace"]["district"] + " không hợp lệ","")
            # isQ2AndApartment = False
            # if((data["msg"]=="added") and ("acceptedTasker" not in data["fields"]) and("taskPlace" in data["fields"])):
                # if((data["fields"]["taskPlace"]["district"] == "Quận 2") and (data["fields"]["homeType"] == "APARTMENT")):
                    # isQ2AndApartment = True
            if(data["msg"]=="added") and ("acceptedTasker" not in data["fields"]) and("taskPlace" in data["fields"]) and (data["fields"]["cost"]>280000) and (isLate == False):
                a=random.uniform(900,1500)
                time.sleep(a/1000)
                bockID = data["id"]
                with open('data.json',encoding="utf-8") as f:
                    danhSachDonHang = f.readline()
                    danhSachDonHang = json.loads(danhSachDonHang)
                checkLoop = 0
                for x in danhSachDonHang:
                    if(employeeIds[curentEmployeeIds] == x["Nhan_vien"] and data["fields"]["date"]["$date"]//1000 <= x["Ngay_lam"]//1000+7200 and data["fields"]["date"]["$date"]//1000 >= x["Ngay_lam"]//1000-7200):
                        checkLoop += 1
                        curentEmployeeIds=curentEmployeeIds+1
                        if(curentEmployeeIds>=10):
                            curentEmployeeIds=0
                        if checkLoop >=10:
                            break
                if checkLoop >= 10:
                    sendErrorPagerDyty("Hết nhân viên nhận đơn","Không thể nhận đơn này do không còn nhân viên có thể nhận đơn")
                else:
                    taskerId = employeeIds[curentEmployeeIds] 
                    result = bookingTask(bockID,taskerId,data["fields"]["serviceId"])# đặt đơn
                    if result == 1:
                        employyDic={}
                        employyDic["GsEbARAMKL39MckJW"]="Trần Ngọc Đăng Khoa"
                        employyDic["AcdEsdaiExqnQtxD8"]="Nguyễn Anh Văn"
                        employyDic["WQ7F4GcpRsZ8ysqAa"]="Đỗ Anh Tiến"
                        employyDic["jQX5yMD5vNFa7bHPN"]="Trần Văn Hoàng"
                        employyDic["Z36QkasdQnzrym3jC"]="Nguyễn Lam Trường"
                        employyDic["rmvb22PYnSdF8RAdB"]="Nguyễn Thành Long"
                        #employyDic["bf6hmzckZr8Kbo3Yd"]="Nguyễn Hoàng Hải"
                        employyDic["RnCLzibDqKfZ8DZCi"]="Lữ Nguyễn Huy Hoàng"
                        #employyDic["cdTh3MRr58vEPRB6k"]="Huỳnh Anh Duy"
                        employyDic["hrKQ2D6gZFXCu6erC"]="Nguyễn Hoàng Tây"
                        employyDic["qrLjuSCwwRt289JMW"]="Lê Văn Hoàn"
                        #employyDic["ELX2PvFEQXjPubwfg"]="Nguyễn Minh Tuấn"
                        employyDic["2e7oXtRDZ74NJdE9j"]="Nguyễn Đức Tài"
                        employyDic["8EQXJMuNRmhmMZsGo"]="Bùi Quốc Trung"
                        f=open("data.txt","a",encoding='utf8')
                        content={}
                        content["Dia_chi"]=data["fields"]["address"]
                        content["Gia_tien"] = data["fields"]["cost"]
                        content["Nhan_vien"] = employyDic[employeeIds[curentEmployeeIds]]
                        contentDumps = json.dumps(content, ensure_ascii=False)
                        f.writelines(contentDumps+"\n")
                        f.close
                        danhSachDonHangMoi = []
                        ts = time.time()
                        for x in danhSachDonHang:
                            if not (x["Ngay_lam"]//1000 < ts):
                                danhSachDonHangMoi.append(x)
                        content1={}
                        ngayLam = datetime.fromtimestamp(data["fields"]["date"]["$date"]//1000)
                        content1["Ngay_lam"]=data["fields"]["date"]["$date"]
                        content1["Nhan_vien"] = employeeIds[curentEmployeeIds]
                        danhSachDonHangMoi.append(content1)
                        danhSachDonHangMoi=json.dumps(danhSachDonHangMoi)
                        with open('data.json','w') as f:
                            f.writelines(danhSachDonHangMoi)
                        curentEmployeeIds=curentEmployeeIds+1
                        if(curentEmployeeIds>=10):
                            curentEmployeeIds=0
            if((data["msg"]=="added") and ("acceptedTasker" in data["fields"]) and("taskPlace" in data["fields"]) and (data["fields"]["acceptedTasker"][0]["taskerId"] in employeeIds)):
                pagerDuty(data,data["fields"]["serviceId"])
            #if((data["msg"]=="added" or data["msg"]=="changed") and (data["collection"] == "chatMessage")):
                #sendMessage(data)
        try:
            if "washing" in data["fields"]["detailSofa"]["curtain"]:
                del data["fields"]["detailSofa"]["curtain"]["washing"]
                flow.messages[-1].content= json.dumps(data)
        except:
            pass
def bookingTask(bockId,taskerId,serviceId):
    if serviceId != "A4BieMZxbrtKeb6WEx1":
        url = "https://api.btaskee.com/api/v2/accept-booking/check-limit-accept-task"
        payload = json.dumps({
            "bookingId": bockId,
            "taskerId": taskerId
        })
        headers = {
        'user-agent': 'okhttp/3.12.1',
        'accept-encoding': 'gzip',
        'content-type': 'application/json',
        'accesskey': 'ZphFh0iUTaGLIYk1qR2vYQh4YcROIES3',
        'accept': 'application/json, text/plain, */*',
        'host': 'api.btaskee.com',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        url = "https://api.btaskee.com/api/v2/accept-booking/sofa"
        payload = json.dumps({
        "bookingId": bockId,
        "taskerId": taskerId,
        "companyId": "cdTh3MRr58vEPRB6k",
        "appVersion": "2.27.0"
        })
        headers = {
        'accept': 'application/json, text/plain, */*',
        'accesskey': 'ZphFh0iUTaGLIYk1qR2vYQh4YcROIES3',
        'content-type': 'application/json',
        'accept-encoding': 'gzip',
        'user-agent': 'okhttp/3.12.1'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            print("Lỗi nhận đơn Server")
            sendErrorPagerDyty("Lỗi nhận đơn server", response.text)
            print(response.text)
            return 0
        else:
             print("Nhận đơn thành công")
             return 1
    else:
        url = "https://api.btaskee.com/api/v2/accept-booking/check-limit-accept-task"
        payload = json.dumps({
            "bookingId": bockId,
            "taskerId": taskerId
        })
        headers = {
        'user-agent': 'okhttp/3.12.1',
        'accept-encoding': 'gzip',
        'content-type': 'application/json',
        'accesskey': 'ZphFh0iUTaGLIYk1qR2vYQh4YcROIES3',
        'accept': 'application/json, text/plain, */*',
        'host': 'api.btaskee.com',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        url = "https://api.btaskee.com/api/v2/accept-booking/disinfection"
        payload = json.dumps({
        "bookingId": bockId,
        "taskerId": taskerId,
        "companyId": "cdTh3MRr58vEPRB6k",
        "appVersion": "2.27.0"
        })
        headers = {
        'accept': 'application/json, text/plain, */*',
        'accesskey': 'ZphFh0iUTaGLIYk1qR2vYQh4YcROIES3',
        'content-type': 'application/json',
        'accept-encoding': 'gzip',
        'user-agent': 'okhttp/3.12.1'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            print("Lỗi nhận đơn Server")
            sendErrorPagerDyty("Lỗi nhận đơn server", response.text)
            print(response.text)
            return 0
        else:
            print("Nhận đơn thành công")
            return 1
def sendErrorPagerDyty(title,message):
    conn = pager.http.client.HTTPSConnection("events.pagerduty.com")
    tentieude = title
    data1={}
    message = message.replace('"',' ')
    message = message.replace('{',' ')
    message = message.replace('}',' ')
    message = message.replace(':',' ')
    data1["Nội dung"]= message
    payload = """{"payload":{"summary":\""""+tentieude+"""\","severity":"critical","source":"Client","custom_details":"""+json.dumps(data1)+"""},"routing_key":"610683d180d44e09c0d1aa66ba22ae32","event_action":"trigger\"}"""
    # Gui don len pager 
    #conn.request("POST", "/v2/enqueue", payload.encode('utf-8'))
    #res = conn.getresponse()
    #info=res.read()
    #print(info)
def pagerDuty(data,serviceID):
    if serviceID != "A4BieMZxbrtKeb6WEx1":
        with open('pagerDuty.json',encoding="utf-8") as f:
            listTask = f.readline()
            listTask = json.loads(listTask)
            dataSoSanh={}
            dataSoSanh["id"]=data["id"]
            dataSoSanh["time"]=data["fields"]["date"]["$date"]
        if dataSoSanh not in listTask:
            conn = pager.http.client.HTTPSConnection("events.pagerduty.com")
            data1={}
            data1["Nhân viên nhận đơn"]=data["fields"]["acceptedTasker"][0]["name"]
            if "houseNumber" in data["fields"]:
                data1["Địa điểm"]=data["fields"]["houseNumber"]+" "+data["fields"]["address"]
            else:
                data1["Địa điểm"]=data["fields"]["address"]
            data1["Giá tiền"]=str(+data["fields"]["cost"])+"VND"
            if "homeType" in data["fields"]:
                data1["Loại nhà"]=data["fields"]["homeType"]
            if "taskNote" in data["fields"]:
                data1["Ghi Chú"] = data["fields"]["taskNote"]
            data1["Tên khách"]=data["fields"]["contactName"]
            data1["STD khách"]=data["fields"]["phone"]
            data1["Hình thức thanh toán"]=data["fields"]["payment"]["method"]
            dt_object = datetime.fromtimestamp(data["fields"]["date"]["$date"]//1000)
            data1["Giờ làm việc"]=dt_object.strftime("%d-%b-%Y (%H:%M)")
            ban_do=f"""https://www.google.com/maps/place/{data["fields"]["lat"]},{data["fields"]["lng"]}"""
            strSofa=""
            if "sofa" in data["fields"]["detailSofa"]:
                for x in data["fields"]["detailSofa"]["sofa"]:
                    if "typeSofa" in x:
                        for y in x["typeSofa"]:
                            strSofa+=y["text"]["vi"] + ": Số lượng: "+str(y["quantity"])+" ,"
                    else:
                        for y in x["stool"]:
                            strSofa+=y["text"]["vi"] + ": Số lượng: "+str(y["quantity"])+" ,"
                data1["Sofa"] = strSofa
            strNem=""
            if "mattress" in data["fields"]["detailSofa"]:
                for x in data["fields"]["detailSofa"]["mattress"]:
                    strNem+=x["text"]["vi"] + ": Số lượng: "+str(x["quantity"])+" ,"
                data1["Nệm"] = strNem
            strRem=""
            if "curtain" in data["fields"]["detailSofa"]:
                if "dryclean" in data["fields"]["detailSofa"]["curtain"]:
                    for x in data["fields"]["detailSofa"]["curtain"]["dryclean"]:
                        strRem+=x["text"]["vi"] + ": Số lượng: "+str(x["quantity"])+" ,"
                if "washing" in data["fields"]["detailSofa"]["curtain"]:
                    for x in data["fields"]["detailSofa"]["curtain"]["washing"]:
                        if "vi" in x:
                            strRem+="Giặt nước: "+x["text"]["vi"] +" ,"
                        else:
                            strRem+="Giặt nước: "+x["text"]["en"] +" ,"
                data1["Rèm"] = strRem
            strTham=""
            if "carpet" in data["fields"]["detailSofa"]:
                for x in data["fields"]["detailSofa"]["carpet"]:
                    strTham+=x["text"]["vi"] + ": Số lượng: "+str(x["quantity"])+" ,"
                data1["Thảm"] = strTham
            tentieude = ""
            tentieude = "Có đơn sofa mới ở " + data["fields"]["taskPlace"]["district"]
            payload = """{"payload":{"summary":\""""+tentieude+"""\","severity":"critical","source":"Client","timestamp":\""""+dt_object.isoformat()+"""\","custom_details":"""+json.dumps(data1)+"""},"routing_key":"610683d180d44e09c0d1aa66ba22ae32","event_action":"trigger\""""
            payload+=""","links": [{"href": \""""+ban_do+"""\","text": "Click đây để xem bản đồ"}]}"""
            conn.request("POST", "/v2/enqueue", payload.encode('utf-8'))
            
            res = conn.getresponse()
            info=res.read()
            #print(payload)
            danhSachDonHangMoi = []
            ts = time.time()
            for x in listTask:
                if not (x["time"]//1000+7200 < ts):
                    danhSachDonHangMoi.append(x)
            danhSachDonHangMoi.append(dataSoSanh)
            with open('pagerDuty.json','w') as f:
                f.writelines(json.dumps(danhSachDonHangMoi))
    else:
        with open('pagerDuty.json',encoding="utf-8") as f:
            listTask = f.readline()
            listTask = json.loads(listTask)
            dataSoSanh={}
            dataSoSanh["id"]=data["id"]
            dataSoSanh["time"]=data["fields"]["date"]["$date"]
        if dataSoSanh not in listTask:
            conn = pager.http.client.HTTPSConnection("events.pagerduty.com")
            data1={}
            data1["Nhân viên nhận đơn"]=data["fields"]["acceptedTasker"][0]["name"]
            data1["Địa điểm"]=data["fields"]["houseNumber"]+" "+data["fields"]["address"]
            data1["Giá tiền"]=str(+data["fields"]["cost"])+"VND"
            data1["Loại nhà"]=data["fields"]["homeType"]
            if "taskNote" in data["fields"]:
                data1["Ghi Chú"] = data["fields"]["taskNote"]
            data1["Tên khách"]=data["fields"]["contactName"]
            data1["STD khách"]=data["fields"]["phone"]
            data1["Hình thức thanh toán"]=data["fields"]["payment"]["method"]
            dt_object = datetime.fromtimestamp(data["fields"]["date"]["$date"]//1000)
            data1["Giờ làm việc"]=dt_object.strftime("%d-%b-%Y (%H:%M)")
            ban_do=f"""https://www.google.com/maps/place/{data["fields"]["lat"]},{data["fields"]["lng"]}"""
            if "customArea" in json.dumps(data):
                data1["Khử khuẩn"] = data["fields"]["disinfectionDetail"]["spaceText"]["vi"] + " diện tích "+ str(data["fields"]["disinfectionDetail"]["customArea"])
            elif "option2" in json.dumps(data) or "option3" in json.dumps(data):
                data1["Khử khuẩn"] = data["fields"]["disinfectionDetail"]["area"]["name"] + " từ "+ str(data["fields"]["disinfectionDetail"]["area"]["from"]) +" đến " + str(data["fields"]["disinfectionDetail"]["area"]["to"])
            else:
                data1["Khử khuẩn"] = data["fields"]["disinfectionDetail"]["spaceText"]["vi"] + " từ "+ str(data["fields"]["disinfectionDetail"]["area"]["from"]) +" đến " + str(data["fields"]["disinfectionDetail"]["area"]["to"])
            tentieude = ""
            tentieude = "Có đơn khử khuẩn mới ở " + data["fields"]["taskPlace"]["district"]
            payload = """{"payload":{"summary":\""""+tentieude+"""\","severity":"critical","source":"Client","timestamp":\""""+dt_object.isoformat()+"""\","custom_details":"""+json.dumps(data1)+"""},"routing_key":"610683d180d44e09c0d1aa66ba22ae32","event_action":"trigger\""""
            payload+=""","links": [{"href": \""""+ban_do+"""\","text": "Click đây để xem bản đồ"}]}"""
            conn.request("POST", "/v2/enqueue", payload.encode('utf-8'))
            res = conn.getresponse()
            info=res.read()
            #print(payload)
            danhSachDonHangMoi = []
            ts = time.time()
            for x in listTask:
                if not (x["time"]//1000+7200 < ts):
                    danhSachDonHangMoi.append(x)
            danhSachDonHangMoi.append(dataSoSanh)
            with open('pagerDuty.json','w') as f:
                f.writelines(json.dumps(danhSachDonHangMoi))
def sendMessage(data):
    ts = time.time()
    if data["fields"]["messages"][-1]["from"]=="ASKER" and ts < data["fields"]["messages"][-1]["createdAt"]["$date"]//1000+5:
        data1={}
        data1["Tin nhắn"]=data["fields"]["messages"][-1]["message"]
        data1["Tên khách"] = data["fields"]["askerName"]
        payload = """{"payload":{"summary":"Có tin nhắn mới","severity":"critical","source":"Client","custom_details":"""+json.dumps(data1)+"""},"routing_key":"610683d180d44e09c0d1aa66ba22ae32","event_action":"trigger","client":"string"}"""
        conn = pager.http.client.HTTPSConnection("events.pagerduty.com")
        conn.request("POST", "/v2/enqueue", payload.encode('utf-8'))
        res = conn.getresponse()
        info=res.read()