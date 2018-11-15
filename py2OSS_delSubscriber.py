# coding: utf-8

import httplib
import xml.dom.minidom as dm
import time

def delSubscriber(MSISDN,soap_host):

    soap_body = '''<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pcrf="http://www.chinamobile.com/PCRF/" xmlns:pcrf1="pcrf:soap">
       <soapenv:Header>
          <pcrf:Header>
             <Address>127.0.0.1</Address>
             <Username>admin</Username>
             <Password>admin</Password>
             <time>?</time>
             <serial>?</serial>
          </pcrf:Header>
       </soapenv:Header>
       <soapenv:Body>
          <pcrf1:delSubscriber>
             <inPara>
                <subscriber>
                   <attribute>
                      <key>usrIdentifier</key>
                      <value>{}</value>
                   </attribute>
                       <attribute>
                      <key>operateTime</key>
                      <value>20150402000000</value>
                   </attribute>
                </subscriber>
             </inPara>
          </pcrf1:delSubscriber>
       </soapenv:Body>
    </soapenv:Envelope>
    '''.format(MSISDN)

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
        MSISDN = str(raw_input("请输入需要删除的号码+86："))
        soap_host = str(raw_input("请输入用户所在PG的IP和端口:"))

        print delSubscriber(MSISDN,soap_host)
        print MSISDN+"已成功销户"
