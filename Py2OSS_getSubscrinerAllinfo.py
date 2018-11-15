# coding: utf-8

import httplib
import xml.dom.minidom as dm
import time

class getSubsAllinfo():
    def __init__(self,MSISDN):
        self.soapPGList13x = ["10.14.60.4:8080","10.14.59.3:8080","10.14.60.5:8080"]
        self.soapPGList1718x = ["10.14.59.11:8080","10.14.76.5:8080", "10.14.76.6:8080"]
        self.soapPGList1519x = ["10.214.116.53:8080","10.214.116.55:8080","10.214.117.51:8080"]
        self.MSISDN = MSISDN

    def getAllinfoRes(self,soap_host):
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
        '''.format(self.MSISDN)

        req_header = {'Content-Type': 'text/xml; charset=utf-8'}
        conn = httplib.HTTPConnection(soap_host, timeout=10)
        conn.request('POST', '/sapcPG/sapcPG', soap_body.encode('utf-8'), req_header)
        response = conn.getresponse()
        data = response.read()
        # 格式化打印xml文档
        xml = dm.parseString(data)
        # print xml.toprettyxml()
        responsexml = xml.toprettyxml()
        conn.close()
        time.sleep(1)
        return responsexml

    def localhost(self, MSISDN):

        # 生成MSISDN对应归属地
        phoneNum = MSISDN.strip("86")
        city = "归属地未知"

        opennumlist = open("numlist.txt", "r")

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

    def xmlfilter(self,xmlstr):
        data = dm.parseString(xmlstr)

        keylist = data.getElementsByTagName('key')
        valuelist = data.getElementsByTagName('value')

        for (i, x) in zip(range(100), range(100)):

            try:
                print keylist[i].firstChild.data + ":   " + valuelist[x].firstChild.data
            except IndexError:
                break

    def filterFunction(self,soapPGlist):
        city = self.localhost(self.MSISDN)
        responsehost = ""
        for soap_host in soapPGlist:
            Res = self.getAllinfoRes(soap_host)
            if "<resultCode>0</resultCode>" in Res:
                print self.MSISDN
                print city
                print soap_host
                print self.xmlfilter(Res)
                responsehost = soap_host
                break

        if responsehost:
            print self.MSISDN + "查询成功"
            return responsehost
        else:
            print self.MSISDN + " " + city + " " + "未查询到签约"
            return False

    def getSubscriberAllinfo(self):

        if self.MSISDN.startswith("8613"):
            self.filterFunction(self.soapPGList13x)
        elif self.MSISDN.startswith("8617") or self.MSISDN.startswith("8618"):
            self.filterFunction(self.soapPGList1718x)
        elif self.MSISDN.startswith("8615") or self.MSISDN.startswith("8619"):
            self.filterFunction(self.soapPGList1519x)

if __name__ == "__main__":
    print "欢迎进入单用户查询签约小程序"
    while True:
        MSISDN = str(raw_input("请输入查询号码+86,输入exit退出程序:"))
        if MSISDN == "exit":
            print "查询结束再见"
            break
        getinfo = getSubsAllinfo(MSISDN)
        print "正在查询请耐心等待......"
        getinfo.getSubscriberAllinfo()
