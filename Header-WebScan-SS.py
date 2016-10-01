####### Requirements ########
# pip install selenium	    #
# apt-get install phantomjs #
#############################

import httplib,time
import sys,os
from selenium import webdriver
import argparse

## Emre Ovunc  ##
## Simge Ozger ##
## info@emreovunc.com ##
## simgee.ozger@gmail.com ##

def Server_Header(host_IP):
    try:
        conn = httplib.HTTPSConnection(host_IP)
        conn.request("HEAD", "/index.html")
        res = conn.getresponse()
        x = res.getheaders()[:1]
        HeaderFile = open (str(host_IP)+"-Header.txt","w")
        HeaderFile.write(str(x))
        HeaderFile.close()
    except:
        try:
            conn = httplib.HTTPConnection(host_IP)
            conn.request("HEAD", "/index.html")
            res = conn.getresponse()
            x = res.getheaders()[:1]
            HeaderFile = open (str(host_IP)+"-Header.txt","w")
            HeaderFile.write(str(x))
            HeaderFile.close()
        except:
            pass
    if (os.path.exists(str(host_IP)+"-Header.txt")):
        with open(str(host_IP)+"-Header.txt", 'r') as TextFile:
                lines=TextFile.read()
        if not lines.startswith("[('set-cookie'"):
            os.system("rm -rf "+str(host_IP)+"-Header.txt")
        TextFile.close()

def HostControl(host_IP,parser):
    if (len(host_IP.split("/"))>1):
        print "[INPUT ERROR] IP usage: 192.168.1.1-255\n"
        time.sleep(1)
        Menu()
    else:
        try:
            splitterUsta =  host_IP.split("-")
            ip_v3 = host_IP.split(".")
            ip_v = ip_v3[0]+"."+ip_v3[1]+"."+ip_v3[2]+"."
            splinterUsta = host_IP.split(".")[3]
            splinterCell = int(splinterUsta.split("-")[0])
            if (len(splitterUsta) > 2):
                print "[INPUT ERROR] IP usage: 192.168.1.1-255\n"   
            else:
                while True:
                    if( int(splitterUsta[1]) < int(splinterCell) ):
                        break
                    else:
                        ip_v2 = str(ip_v) + str(splinterCell)
                        Nmap_SS(ip_v2)
                        splinterCell = int(splinterCell) + 1
        except:
            parser.print_help()
            sys.exit(1)
def Menu():
    parser = argparse.ArgumentParser()
    parser.add_argument("IP")
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    host_IP = HostControl(args.IP,parser)

def Nmap_SS(host_IP):
    print ("Scan is starting for "+str(host_IP)+"...")
    port_List=[80,443]
    os.system("nmap -p 80,443 "+ host_IP + " > "+ host_IP +"-Nmap.txt")
    with open(str(host_IP)+"-Nmap.txt", 'r') as TextFile:
        lines=TextFile.read()
    if "Host seems down." in lines:
        os.system("rm -rf "+str(host_IP)+"-Nmap.txt")
    else:
        Server_Header(host_IP)
        for port in port_List:
            if (str(port) in lines):
                driver = webdriver.PhantomJS() 
                driver.set_window_size(1024, 768)
                Screenshot_Url = "http://"+host_IP+":"+str(port)
                Screenshot_Url_s = "https://"+host_IP+":"+str(port)
                Http_Url = host_IP+":"+str(port)
                try:
                    conn = httplib.HTTPConnection(Http_Url)
                    conn.request("GET","/")
                    r1=conn.getresponse()
                    if (r1.status==200):
                        conn.close()
                        driver.get(Screenshot_Url)
                        Screenshot_name = host_IP+":"+str(port)+"-HTTP.png"
                        driver.save_screenshot(Screenshot_name)
                        driver.quit()
                except:
                    try:
                        conn = httplib.HTTPSConnection(Http_Url)
                        conn.request("GET","/")
                        r1=conn.getresponse()
                        if (r1.status==200):
                            conn1 = httplib.HTTPSConnection(Http_Url)
                            conn1.request("GET","/")
                            r2=conn1.getresponse()
                            if (r2.status==200):
                                conn1.close()
                                driver.get(Screenshot_Url_s)
                                Screenshot_name_s = host_IP+":"+str(port)+"-HTTPS.png"
                                driver.save_screenshot(Screenshot_name_s)
                                driver.quit()
                    except:
                           pass
                driver.quit()
    TextFile.close()
    print ("\nScan is finished for "+str(host_IP)+" !!!\n")
    if (os.path.exists("ghostdriver.log")):
        os.system("rm ghostdriver.log")
Menu()
