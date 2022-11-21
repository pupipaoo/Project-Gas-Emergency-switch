from machine import Pin, PWM, I2C, UART, ADC
import os, sys
import utime
import machine
import random

WiFi_SSID='My ASUS'
WiFi_PASSWD=''
Sever_IP='125.229.69.35'
Sever_port=1883

uart = machine.UART(1,tx=Pin(8),rx=Pin(9),baudrate=115200)

def sendCMD_waitResp(cmd,timeout=100):
    
    print("CMD: " + cmd)
    cmd+='\r\n'
    uart.write(cmd)  #cmd.encode('utf-8')
    return waitResp(timeout)

def connet_wifi(ssid, passwd):
    
    #waitResp() 
    sendCMD_waitResp("AT+RST") #reset the esp8266       #sendCMD是ESP8266的AT Command;RST是重開ESP8266
    sendCMD_waitResp("AT+CWMODE=3")   #set wifi mode 1:client(也就是者)2:AP(也就是基地台) 3: Both  #開啟wifi 模式
    sendCMD_waitResp('AT+CWJAP='+"My ASUS"+','+"jade1234",timeout=5000) #connecting,連接基地台
    sendCMD_waitResp("AT+CIPMUX=0")  # 0: single connection(自己去連別人); 1:multi user(多人連線，連很多serever,被別人連才用這個)
    resp=sendCMD_waitResp("AT+CIFSR")	#顯示對方(基地台或是使用者)的IP
    start=resp.find('"')+1
    end=resp.find('"',start)
    return resp[start:end]  #myip

def send_http_req(ip,port,url,method='GET'):            #HTTP訊息以get送出

    
    url=method+' '+url+' HTTP/1.1\r\n\r\n'	#字串GET帶入method，空一格，再填入/sensor?fire="ON"，再加HTTP/1.1\r\n\r\n
    sendCMD_waitResp('AT+CIPSTART="TCP","'+ip+'",'+str(port))	#建立TCP連線
    sendCMD_waitResp('AT+CIPSEND='+str(len(url)))       #算送了幾格byte,並送出
    sendCMD_waitResp(url)               #送url
    sendCMD_waitResp("AT+CIPCLOSE")


#以下開始
myip=connet_wifi(WiFi_SSID,WiFi_PASSWD)
#oled.fill(0)
#oled.text(myip,0,0)
#oled.show()
utime.sleep(5)


while (1):
	i="ON"
    url_path='/sensor?fire='+i
	send_http_req(Sever_IP,Sever_port,url_path)

	
	
	