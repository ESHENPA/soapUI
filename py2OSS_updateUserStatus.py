# coding: utf-8

import httplib
import xml.dom.minidom as dm
import time

def updateSubscriber(MSISDN, UserStatus,soap_host):

    soap_body = '''<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pcrf="http://www.chinamobile.com/PCRF/" xmlns:pcrf1="pcrf:soap">
       <soapenv:Header>
          <pcrf:Header>
             <Address>127.0.0.1</Address>
             <Username>boss</Username>
             <Password>Ericss0n@</Password>
             <time>?</time>
             <serial>?</serial>
          </pcrf:Header>
       </soapenv:Header>
       <soapenv:Body>
          <pcrf1:updateSubscriber>
             <inPara>
                <subscriber>
                <attribute>
                      <key>usrIdentifier</key>
                      <value>{}</value>
                   </attribute>
                 <attribute>
                       <key>usrStatus</key>
                       <value>{}</value>
                   </attribute>
                      <attribute>
                      <key>operateTime</key>
                      <value>20150401000009</value>
                   </attribute>
                </subscriber>
             </inPara>
          </pcrf1:updateSubscriber>
       </soapenv:Body>
    </soapenv:Envelope>
    '''.format(MSISDN, UserStatus)

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

if __name__ == "__main__":
    while True:
        soapPGdict13x ={"13xPG":{"QDAPCRF01PG01BER":"10.14.60.4:8080","QDAPCRF02PG01BER":"10.14.59.3:8080","QDAPCRF03PG01BER":"10.14.60.5:8080"}}
        soapPGdict1718x = {"1718xPG":{"QDAPCRF06PG01BER":"10.14.59.11:8080","QDAPCRF07PG01BER":"10.14.76.5:8080","QDAPCRF08PG01BER":"10.14.76.6:8080"}}
        soapPGdict1519x = {"1519xPG":{"QDAPCRF14PG01BER":"10.214.116.53:8080","QDAPCRF15PG01BER":"10.214.116.55:8080","QDAPCRF16PG01BER":"10.214.117.51:8080"}}
        print soapPGdict13x,soapPGdict1718x,soapPGdict1519x

        MSISDN = str(raw_input("请输入需要更新的号码+86，Warning请先查询号码是否已经签约,输入exit退出程序:"))
        if MSISDN=="exit":
            print "updateUserStatus程序退出,再见"
            break
        UserStatus = str(raw_input("请输入UserStatus编码 1为正常速率，51为限速1M，52为限速128K:"))
        soap_host = str(raw_input("请输入用户所在PG的IP和端口例如 1.1.1.1:8080 :"))
        print MSISDN,UserStatus,soap_host

        print updateSubscriber(MSISDN,UserStatus,soap_host)
        print MSISDN+"UserStatus更新为："+ UserStatus
