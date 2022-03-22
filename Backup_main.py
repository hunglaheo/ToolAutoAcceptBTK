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
employeeIds=["ELX2PvFEQXjPubwfg","GsEbARAMKL39MckJW","RnCLzibDqKfZ8DZCi","bf6hmzckZr8Kbo3Yd","cdTh3MRr58vEPRB6k","hrKQ2D6gZFXCu6erC","qrLjuSCwwRt289JMW","rmvb22PYnSdF8RAdB"]
curentEmployeeIds=5
from mitmproxy.proxy import protocol
def websocket_message(flow:websocket.WebSocketFlow):
    
    global curentEmployeeIds
    data=flow.messages[-1].content
    data=data.replace("'", "\"")
    data=data.replace("True", "\"True\"")
    data=data.replace("False", "\"False\"")
    data=data.replace("None", "\"None\"")
    data=json.loads(data)
    if("msg" in data.keys()):
        print(data)
        isLate = False
        if((data["msg"]=="added") and ("acceptedTasker" in data["fields"]) and("taskPlace" in data["fields"])):
            pagerDuty(data)
        if((data["msg"]=="added") and ("acceptedTasker" not in data["fields"]) and("taskPlace" in data["fields"])):
            dt_object = datetime.fromtimestamp(data["fields"]["date"]["$date"]//1000)
            if ((data["fields"]["taskPlace"]["district"] == "Bình Chánh") or (data["fields"]["taskPlace"]["district"] == "Nhà Bè") or (data["fields"]["taskPlace"]["district"] == "Quận 7") or (data["fields"]["taskPlace"]["district"] == "Củ Chi")):
                if (dt_object.hour > 16 and dt_object.minute > 30):
                    isLate = True
        # isQ2AndApartment = False
        # if((data["msg"]=="added") and ("acceptedTasker" not in data["fields"]) and("taskPlace" in data["fields"])):
            # if((data["fields"]["taskPlace"]["district"] == "Quận 2") and (data["fields"]["homeType"] == "APARTMENT")):
                # isQ2AndApartment = True
        if((data["msg"]=="added") and ("acceptedTasker" not in data["fields"]) and("taskPlace" in data["fields"]) and (data["fields"]["cost"]>290000) and (data["fields"]["taskPlace"]["district"] != "Gò Vấp") and (isLate == False)):
            a=random.uniform(900,1500)
            time.sleep(a/1000)
            bockID = data["id"]
            with open('data.json',encoding="utf-8") as f:
                danhSachDonHang = f.readline()
                danhSachDonHang = json.loads(danhSachDonHang)
            for x in danhSachDonHang:
                if(employeeIds[curentEmployeeIds] == x["Nhan_vien"] and data["fields"]["date"]["$date"]//1000 <= x["Ngay_lam"]//1000+3600 and data["fields"]["date"]["$date"]//1000 >= x["Ngay_lam"]//1000-3600):
                    curentEmployeeIds=curentEmployeeIds+1
            taskerId = employeeIds[curentEmployeeIds]
            url = "https://api.btaskee.com/api/v2/accept-booking/check-limit-accept-task"
            payload = json.dumps({
                "bookingId": bockID,
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
            "bookingId": bockID,
            "taskerId": taskerId,
            "companyId": "cdTh3MRr58vEPRB6k",
            "appVersion": "2.23.0"
            })
            headers = {
            'accept': 'application/json, text/plain, */*',
            'accesskey': 'ZphFh0iUTaGLIYk1qR2vYQh4YcROIES3',
            'content-type': 'application/json',
            'accept-encoding': 'gzip',
            'user-agent': 'okhttp/3.12.1'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            employyDic={}
            employyDic["GsEbARAMKL39MckJW"]="Trần Ngọc Đăng Khoa"
            employyDic["rmvb22PYnSdF8RAdB"]="Nguyễn Thành Long"
            employyDic["bf6hmzckZr8Kbo3Yd"]="Nguyễn Hoàng Hải"
            employyDic["ELX2PvFEQXjPubwfg"]="Nguyễn Minh Tuấn"
            employyDic["RnCLzibDqKfZ8DZCi"]="Lữ Nguyễn Huy Hoàng"
            employyDic["cdTh3MRr58vEPRB6k"]="Huỳnh Anh Duy"
            employyDic["hrKQ2D6gZFXCu6erC"]="Nguyễn Hoàng Tây "
            employyDic["qrLjuSCwwRt289JMW"]="Lê Văn Hoàn"
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
            print("Nhận đơn thành công")
            curentEmployeeIds=curentEmployeeIds+1
            if(curentEmployeeIds==8):
                curentEmployeeIds=0
            

def pagerDuty(data):
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
        data1["Tên khách"]=data["fields"]["contactName"]
        data1["STD khách"]=data["fields"]["phone"]
        data1["Hình thức thanh toán"]=data["fields"]["payment"]["method"]
        dt_object = datetime.fromtimestamp(data["fields"]["date"]["$date"]//1000)
        data1["Giờ làm việc"]=dt_object.strftime("%d-%b-%Y (%H:%M)")
        data1["Bản đồ"]=f"""https://www.google.com/maps/place/{data["fields"]["lat"]},{data["fields"]["lng"]}"""
        strSofa=""
        if "sofa" in data["fields"]["detailSofa"]:
            for x in data["fields"]["detailSofa"]["sofa"]:
                for y in x["typeSofa"]:
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
                data1["Rèm"] = strRem
        strTham=""
        if "carpet" in data["fields"]["detailSofa"]:
            for x in data["fields"]["detailSofa"]["carpet"]:
                strTham+=x["text"]["vi"] + ": Số lượng: "+str(x["quantity"])+" ,"
            data1["Thảm"] = strTham
        payload = """{"payload":{"summary":"Có đơn mới","severity":"critical","source":"Client","custom_details":"""+json.dumps(data1)+"""},"routing_key":"610683d180d44e09c0d1aa66ba22ae32","event_action":"trigger","client":"string"}"""
        conn.request("POST", "/v2/enqueue", payload.encode('utf-8'))
        res = conn.getresponse()
        info=res.read()
        danhSachDonHangMoi = []
        ts = time.time()
        for x in listTask:
            if not (x["time"]//1000+3600 < ts):
                danhSachDonHangMoi.append(x)
        danhSachDonHangMoi.append(dataSoSanh)
        with open('pagerDuty.json','w') as f:
            f.writelines(json.dumps(danhSachDonHangMoi))
