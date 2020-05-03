#!/usr/bin/python3
# EmreOvunc
# info@emreovunc.com
# 03.05.2020

from os         import path
from os         import mkdir
from os         import rmdir
from os         import getcwd
from os         import remove
from os 		import listdir
from sys        import argv
from sys        import exit
from time       import sleep
from socket     import socket
from socket     import AF_INET
from socket     import SOCK_STREAM
from datetime   import datetime as dt
from selenium   import webdriver
from argparse   import ArgumentParser
from warnings   import filterwarnings

filterwarnings('ignore')

folders = []

def removeempty(folders):
    if len(folders) != 0:
    	for folder in folders:
    		if len(listdir(folder) ) == 0:
    			rmdir(folder)


def getenv(ip, folders):
    date = str(dt.now()).split(' ')[0].split("-")[0] + str(dt.now()).split(' ')[0].split("-")[1] + str(dt.now()).split(' ')[0].split("-")[2]
    time = str(dt.now()).split(' ')[1].split(":")[0] + "_" + \
           str(dt.now()).split(' ')[1].split(":")[1] + "_" + \
           str(dt.now()).split(' ')[1].split(":")[2].split('.')[0]
    foldername = ip + "_" + date + "_" + time

    if not path.exists("scans"):
    	mkdir("scans")

    fullpath = "scans/" + foldername

    if path.exists(fullpath):
        rmdir(fullpath)
    else:
        mkdir(fullpath)

    folders.append(fullpath)

    return fullpath


def portcheck(ip, folder):
    portlist = [80, 443, 8000, 8080, 8443, 10000]
    for port in portlist:
        try:
            soc_port = socket(AF_INET, SOCK_STREAM)
            soc_port.settimeout(1)
            soc_port.connect((ip, port))
            soc_port.close()
            sleep(0.05)
            result = 1
        except:
            result = 0
        finally:
            if result == 1:
                ss(ip, port, folder)


def save_ss(driver, ip, port, folder, ssl):
    if ssl == 0:
        try:        
            ss_url = "http://" + ip + ":" + str(port)
            driver.get(ss_url)
            screenshot_name = str(ip) + ":" + str(port) + "-http.png"
            driver.save_screenshot(folder + "/" + screenshot_name)

            if path.exists(folder + "/" + screenshot_name) and path.getsize(folder + "/" + screenshot_name) < 14000:
                remove(folder + "/" + screenshot_name)

            save_ss(driver, ip, port, folder, 1)

        except:
            save_ss(driver, ip, port, folder, 1)

    else:
        try:
            ss_url = "https://" + ip + ":" + str(port)
            driver.get(ss_url)
            screenshot_name = str(ip) + ":" + str(port) + "-https.png"
            driver.save_screenshot(folder + "/" + screenshot_name)

            if path.exists(folder + "/" + screenshot_name) and path.getsize(folder + "/" + screenshot_name) < 14000:
                remove(folder + "/" + screenshot_name)

            driver.quit()
        
        except:
            pass


def ss(ip, port, folder):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--headless")

    cwd = getcwd()
    driver_path = cwd + "/chromedriver"
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    ssl = 0
    save_ss(driver, ip, port, folder, ssl)


def menu():
    parser = ArgumentParser()
    parser.add_argument("IP")
    if len(argv) == 1:
        parser.print_help()
        exit(1)
    args = parser.parse_args()
    portcheck(args.IP, getenv(args.IP, folders))
    removeempty(folders)


menu()
