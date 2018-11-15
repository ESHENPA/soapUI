# coding: utf-8

import httplib
import xml.dom.minidom as dm
import time
import csv
import re


class BatgetAllinfo():
    def __init__(self):
        # 生成PG列表
        print """欢迎使用批量查询签约小工具\t1.请先定义手机号txt文件，以列模式创建\t2.再定义归属地txt文件，以列模式创建\t3.如果未定义上述文件请按crtl+c退出程序
        """
        self.soapPGList13x = ["10.14.60.4:8080", "10.14.59.3:8080", "10.14.60.5:8080"]
        self.soapPGList1718x = ["10.14.59.11:8080", "10.14.76.5:8080", "10.14.76.6:8080"]
        self.soapPGList1519x = ["10.214.116.53:8080", "10.214.116.55:8080", "10.214.117.51:8080"]
        self.MSISDNfile = str(raw_input("请输入手机号读取文件名不含86, .txt："))
        self.localfile = str(raw_input("请输入归属地读取文件名.txt："))
        self.searchResultfile = str(raw_input("请输入查询结果存储文件名.csv："))

    # 生成MSISDN列表
    def createMSISDNlist(self, MSISDNfile):

        MSISDNlist = []
        openfile = open(MSISDNfile, "r")

        while True:
            readfile = openfile.readline()
            if readfile:
                MSISDNlist.append("86" + readfile[0:11])
            else:
                break
        return MSISDNlist

    # 定义归属地生成函数
    def localhost(self, MSISDN, localfile):

        # 生成MSISDN对应归属地
        phoneNum = MSISDN.strip("86")
        city = "归属地未知"

        opennumlist = open(localfile, "r")

        while True:
            ReadLine = opennumlist.readline()
            if ReadLine == "":
                opennumlist.close()
                break
            locallist = ReadLine.split("\t")

            if locallist[0] == phoneNum[0:7]:
                city = locallist[1]
                opennumlist.close()
                break
        return city

    def createSuccesslist(self, MSISDN, city, soap_host,usrGrade,usrStatus,usrBillCycleDate,
                          PackageType,usrSessionPolicyCode,SessionPolicyStartDateTime,SessionPolicyEndDateTime):
        successlist = []

        successlist.append(MSISDN)
        successlist.append(city)
        successlist.append(soap_host)
        successlist.append(usrGrade)
        successlist.append(usrStatus)
        successlist.append(usrBillCycleDate)
        successlist.append(PackageType)
        successlist.append(usrSessionPolicyCode)
        successlist.append(SessionPolicyStartDateTime)
        successlist.append(SessionPolicyEndDateTime)
        return successlist

    def createFailedlist(self, MSISDN, city):
        failedlist = []
        failedlist.append(MSISDN)
        failedlist.append(city)
        failedlist.append("未签约")
        return failedlist

    def fileterfunction(self,attribute):

        if attribute == []:
            attribute = ""
            return attribute
        else:
            attribute = attribute[0]
            return attribute

    def resultStore(self, csvWr, MSISDN, city, soapPGList):
        responselist = []
        for soap_host in soapPGList:
            response = self.getSubscriberAllInfRes(soap_host, MSISDN)
            if "<resultCode>0</resultCode>" in response:
                #过滤返回值
                usrGrade_p = re.compile(r'<key>usrGrade</key>[\s\S]*?<value>([\s\S]*?)</value>')
                usrStatus_p = re.compile(r'<key>usrStatus</key>[\s\S]*?<value>([\s\S]*?)</value>')
                usrBillCycleDate_p = re.compile(r'<key>usrBillCycleDate</key>[\s\S]*?<value>([\s\S]*?)</value>')
                PackageType_p = re.compile(r'<key>PackageType</key>[\s\S]*?<value>([\s\S]*?)</value>')
                usrSessionPolicyCode_p = re.compile(r'<key>usrSessionPolicyCode</key>[\s\S]*?<value>([\s\S]*?)</value>')
                SessionPolicyStartDateTime_p = re.compile(r'<key>SessionPolicyStartDateTime</key>[\s\S]*?<value>([\s\S]*?)</value>')
                SessionPolicyEndDateTime_p = re.compile(r'<key>SessionPolicyEndDateTime</key>[\s\S]*?<value>([\s\S]*?)</value>')

                usrGrade = usrGrade_p.findall(response)
                usrStatus = usrStatus_p.findall(response)
                usrBillCycleDate = usrBillCycleDate_p.findall(response)
                PackageType = PackageType_p.findall(response)
                usrSessionPolicyCode = usrSessionPolicyCode_p.findall(response)
                SessionPolicyStartDateTime = SessionPolicyStartDateTime_p.findall(response)
                SessionPolicyEndDateTime = SessionPolicyEndDateTime_p.findall(response)

                #处理过滤后的列表
                usrGrade = self.fileterfunction(usrGrade)
                usrStatus = self.fileterfunction(usrStatus)
                usrBillCycleDate = self.fileterfunction(usrBillCycleDate)
                PackageType = self.fileterfunction(PackageType)


                replistsuccess = self.createSuccesslist(MSISDN, city, soap_host, usrGrade,usrStatus,usrBillCycleDate,
                                PackageType,usrSessionPolicyCode,SessionPolicyStartDateTime,SessionPolicyEndDateTime)
                csvWr.writerow(replistsuccess)
                responselist.append(True)
                break
            else:
                responselist.append(False)

        if True not in responselist:
            respfailedlist = self.createFailedlist(MSISDN, city)
            csvWr.writerow(respfailedlist)

    # 定义getSubscriberAllInf应答结果函数
    def getSubscriberAllInfRes(self, soap_host, MSISDN):
        soap_body = '''<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pcrf="http://www.chinamobile.com/PCRF/" xmlns:pcrf1="pcrf:soap">
           <soapenv:Header>
              <pcrf:Header>
                 <Address></Address>
                 <Username>admin</Username>
                 <Password>admin</Password>
                 <time>?</time>
                 <serial>?</serial>
              </pcrf:Header>
           </soapenv:Header>
           <soapenv:Body>
              <pcrf1:getSubscriberAllInf>
                 <inPara>
                    <subscriber>
                       <!--1 or more repetitions:-->
                       <attribute>
                          <key>usrIdentifier</key>
                          <value>{}</value>
                       </attribute>
                    </subscriber>
                 </inPara>
              </pcrf1:getSubscriberAllInf>
           </soapenv:Body>
        </soapenv:Envelope>
        '''.format(MSISDN)

        req_header = {'Content-Type': 'text/xml; charset=utf-8'}
        conn = httplib.HTTPConnection(soap_host, timeout=10)
        conn.request('POST', '/sapcPG/sapcPG', soap_body.encode('utf-8'), req_header)
        response = conn.getresponse()
        data = response.read()
        # 格式化xml文档
        xml = dm.parseString(data)
        responsexml = xml.toprettyxml()
        conn.close()
        time.sleep(1)
        return responsexml

    # 定义getSubscriberAllInf查询函数
    def getSubscriberAllInf(self):
        # 打开查询结果CSV文件，等待写入
        openfile = open(self.searchResultfile, "wb")
        csvWr = csv.writer(openfile)
        titlelist = ["手机号","归属地","归属PG","usrGrade","usrStatus","usrBillCycleDate","PackageType","usrSessionPolicyCode","SessionPolicyStartDateTime","SessionPolicyEndDateTime"]
        csvWr.writerow(titlelist)

        # 生成MSISN列表
        MSISDNlist = self.createMSISDNlist(self.MSISDNfile)

        # 查询任务入口
        for MSISDN in MSISDNlist:
            city = self.localhost(MSISDN, self.localfile)

            # 开始查询
            if MSISDN.startswith("8613"):
                self.resultStore(csvWr, MSISDN, city, self.soapPGList13x)

            if MSISDN.startswith("8617") or MSISDN.startswith("8618"):
                self.resultStore(csvWr, MSISDN, city, self.soapPGList1718x)

            if MSISDN.startswith("8615") or MSISDN.startswith("8619"):
                self.resultStore(csvWr, MSISDN, city, self.soapPGList1519x)
        openfile.close()
        print "查询结束请查看" + self.searchResultfile


if __name__ == "__main__":
    getinfo = BatgetAllinfo()
    getinfo.getSubscriberAllInf()
