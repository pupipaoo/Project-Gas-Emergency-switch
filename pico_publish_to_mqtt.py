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
    sendCMD_waitResp("AT+RST") #reset the esp8266       #sendCMD是ESP8266的AT Command
    sendCMD_waitResp("AT+CWMODE=0")   #set wifi mode 1:client 2:AP 3: Both  #開啟wifi 模式
    sendCMD_waitResp('AT+CWJAP='+"My ASUS"+','+"jade1234",timeout=5000) #connecting
    sendCMD_waitResp("AT+CIPMUX=0")  # 0: single connection(自己去連別人); 1:multi user(多人連線，連很多serever,被別人連才用這個)
    resp=sendCMD_waitResp("AT+CIFSR")
    start=resp.find('"')+1
    end=resp.find('"',start)
    return resp[start:end]  #myip

def send_http_req(ip,port,url,method='GET'):            #HTTP訊息以get送出

    #GET /sensor?temp=28 HTTP/1.1\r\n\r\n'
    url=method+' '+url+' HTTP/1.1\r\n\r\n'
    sendCMD_waitResp('AT+CIPSTART="TCP","'+ip+'",'+str(port))
    sendCMD_waitResp('AT+CIPSEND='+str(len(url)))       #算送了幾格byte,並送出
    sendCMD_waitResp(url)               #送url
    sendCMD_waitResp("AT+CIPCLOSE")

myip=connet_wifi(WiFi_SSID,WiFi_PASSWD)
#oled.fill(0)
#oled.text(myip,0,0)
#oled.show()
utime.sleep(5)


while (1):
	send_http_req(Sever_IP,Sever_port,"ON")

	
	
	