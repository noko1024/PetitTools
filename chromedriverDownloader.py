import os
import requests
import platform
import subprocess
import re
import io
import zipfile
import sys

base_path = os.path.split(os.path.realpath(__file__))[0]

def get_chrome_version_window() -> str:
    #クロームのバージョンを検出 (x86ユーザーもいたので…)
    try:
        res = subprocess.check_output('dir /B/O-N "C:\Program Files\Google\Chrome\Application" |findstr "^[0-9].*¥>',shell=True)
    except:
        res = subprocess.check_output('dir /B/O-N "C:\Program Files (x86)\Google\Chrome\Application" |findstr "^[0-9].*¥>',shell=True)
    version = re.search(r'[0-9]+',res.decode("utf-8"))[0]
    return version


def get_chrome_version_darwin() -> str:
    #クロームのバージョンを検出
    res = subprocess.check_output("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version",shell=True)
    version = re.search(r'[0-9]+',res.decode("utf-8"))[0]
    return version


def seleniumDownload(OS="mac64",version="104"):
    
    #クロームのバージョンに応じたseleniumの最新バージョンを取得
    seleniumVer = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version}").text
    seleniumVer = re.search(r'\d+.*',seleniumVer)
    
    if seleniumVer is None:
        print("Sorry! This version is not supported.")
        sys.exit(1)
    else:
        seleniumVer = seleniumVer[0]
    
    #zipをダウンロードしメモリ上に展開
    f = io.BytesIO()
    res = requests.get(f"https://chromedriver.storage.googleapis.com/{seleniumVer}/chromedriver_{OS}.zip")
    f.write(res.content)

    #解凍して書き込み
    with zipfile.ZipFile(f) as z:
        z.extractall(os.path.join(base_path,"lib"))
    
seleniumDownload()

def main():

    match platform.system():
        case "Windows":
            print("Platform:Windows")
            version = get_chrome_version_window()
            print(f"Chrome version:{version}")
            seleniumDownload("win32",version)

        case "Darwin":
            print("Platform:MacOS")
            version = get_chrome_version_darwin()
            print(f"Chrome version:{version}")
            seleniumDownload("mac64",version)

        case _:
            print("Sorry! This OS is not supported.")
            sys.exit(1)

    print("Chromedriver download completed successfully!")

main()