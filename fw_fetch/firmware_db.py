from common.response import app_ok_p, app_err_p, app_ok, app_err
from common.error_code import Error
from common.utils.http_request import req_get_param_int, req_get_param, req_post_param, req_post_param_int, \
    req_post_param_dict
import common.config

from common.utils.general import SysUtils

import re
import requests
import urllib.request
import os
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

# firmware 集合
firmware_col = common.config.g_firmware_col


class Firmware():

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        # self.base_url = 'http://www.luyoudashi.com'
        self.base_url = 'http://www.luyoudashi.com/roms/vendor-13350-' #1.html'
        self.base_path = os.path.dirname(__file__)

    def makedir(self, name):
        path = os.path.join(self.base_path, name)
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            print("File has been created.")
        else:
            print('OK!The file is existed. You do not need create a new one.')
        os.chdir(path)

    def request(self, url):
        r = requests.get(url, headers=self.headers)
        return r

    def get_firmware(self, url_firmware, savepath):

        try:
            # self.makedir('firmware')

            # 获取网页的源代码
            # html = urllib.request.urlopen(self.base_url + str(page) + '.html')
            html = urllib.request.urlopen(url_firmware)
            content = html.read().decode('utf8')
            html.close()

            reg = r'<li class="rom_list"><a href="(.*)">(.*)</a>'  # 根据网站样式匹配的正则：(.* )可以匹配所有东西，加括号为我们需要的
            reg = re.compile(reg)
            urls = re.findall(reg, content)
            for url in urls:
                print(url[0])
                print(url[1])
                # http://www.luyoudashi.com/roms/romlist-m1823.html
                               # a href = "/roms/romlist-m1823.html"
                urlsub = 'http://www.luyoudashi.com' + url[0]
                # urlsub = url_firmware + url[0]
                html = urllib.request.urlopen(urlsub)
                content1 = html.read().decode('utf8')
                html.close()

                soup = BeautifulSoup(content1, "html.parser")
                ul = soup.find('ul', class_="rom_list_list")
                ul = str(ul)
                reg1 = r'<li><span>(.*)</span><a href="(.*)">(.*)</a>(.*)</li>'  # 根据网站样式匹配的正则：(.* )可以匹配所有东西，加括号为我们需要的
                reg1 = re.compile(reg1)
                targets = re.findall(reg1, ul)

                # for ul in soup.find_all("<li><span>[.*]</span>"):
                for ul in targets:
                    print(ul[0])
                    print(ul[1])
                    print(ul[2])
                    print(ul[3])

                    urldownload = 'http://www.luyoudashi.com' + ul[1]
                    html = urllib.request.urlopen(urldownload)
                    content2 = html.read().decode('utf8')
                    html.close()

                    soup = BeautifulSoup(content2, "html.parser")
                    rom_info_down = soup.find('div', class_="rom_info_down")
                    print(rom_info_down)

                    rom_info_down = str(rom_info_down)
                    reg = r'<a class="romdown" href="(.*)">立即下载固件</a>'  # 根据网站样式匹配的正则：(.* )可以匹配所有东西，加括号为我们需要的
                    reg = re.compile(reg)
                    urls = re.findall(reg, rom_info_down)
                    print(urls[0])

                    # filename = os.path.basename(urls[0])
                    # # readme = savepath + "\\" + filename + ".txt"
                    # readme = filename + ".txt"
                    # with open(readme, "wb") as f:
                    #     f.write(str(ul[0]))
                    #     f.write(ul[1])
                    #     f.write(ul[2])
                    #     f.write(ul[3])
                    # f.close()

                    def download(url, savepath='./'):
                        """
                        download file from internet
                        :param url: path to download from
                        :param savepath: path to save files
                        :return: None
                        """

                        def reporthook(a, b, c):
                            """
                            显示下载进度
                            :param a: 已经下载的数据块
                            :param b: 数据块的大小
                            :param c: 远程文件大小
                            :return: None
                            """
                            print("\rdownloading: %5.1f%%" % (a * b * 100.0 / c), end="")

                        filename = os.path.basename(url)
                        # 判断文件是否存在，如果不存在则下载
                        if not os.path.isfile(os.path.join(savepath, filename)):
                            print('Downloading data from %s' % url)
                            urlretrieve(url, os.path.join(savepath, filename), reporthook=reporthook)
                            print('\nDownload finished!')
                        else:
                            print('File already exsits!')
                        # 获取文件大小
                        filesize = os.path.getsize(os.path.join(savepath, filename))
                        # 文件大小默认以Bytes计， 转换为Mb
                        print('File size = %.2f Mb' % (filesize / 1024 / 1024))


                    # download(urls[0], savepath)
                    download(urls[0])
                    break #只下载一个固件 ，全部下载耗时且占用磁盘空间大
                break


        except Exception as e:
            print(e)

class FirmwareDB:

    def info_count(self):
        return firmware_col.count()

    # firmware_manufacturer = models.CharField(max_length=200)    #固件厂商
    # application_mode = models.CharField(max_length=128)         #适用机型
    # firmware_version = models.CharField(max_length=16)          #固件版本
    # firmware_size = models.CharField(max_length=8)              #文件大小
    # pub_date = models.DateTimeField('date published')           #发布日期
    # firmware_file_path = models.CharField(max_length=255)       #本地存放路径
    def savedb(self, firmware_manufacturer, application_mode, firmware_size, pub_date, firmware_file_path):
        test = SysUtils.makedir("test")
        return test

    def fwdownload(self, homepage):
        # firmware的XX数据总数
        # total = self.info_count()

        # 爬取下载固件
        firmware = Firmware()

        # 普联 TP-Link
        savepath = "TP-Link"
        firmware.makedir(savepath)
        url = homepage + "/roms/vendor-13350-"
        # html = urllib.request.urlopen(self.base_url + str(page) + '.html')
        for i in range(5):  # 控制爬取的页数
            # firmware.get_firmware(url, i+1)
            url = url + str(i+1) + ".html"
            firmware.get_firmware(url, savepath)
            break

        # 水星 Mercury
        savepath = "Mercury"
        firmware.makedir(savepath)
        # url = "http://www.luyoudashi.com/roms/vendor-8080-"
        url = homepage + "/roms/vendor-8080-"
        for i in range(2):  # 控制爬取的页数
            url = url + str(i+1) + ".html"
            firmware.get_firmware(url, savepath)
            break

        # 智能固件 OpenWRT
        # 迅捷 Fast
        savepath = "Fast"
        firmware.makedir(savepath)
        url = homepage + "/roms/vendor-4588.html"
        firmware.get_firmware(url, savepath)

        # 斐讯 Phicomm  http://www.luyoudashi.com/roms/vendor-11367.html
        savepath = "Phicomm"
        firmware.makedir(savepath)
        url = homepage + "/roms/vendor-11367-"
        for i in range(2):  # 控制爬取的页数
            url = url + str(i+1) + ".html"
            firmware.get_firmware(url, savepath)
            break

        # 腾达 Tenda
        savepath = "Tenda"
        firmware.makedir(savepath)
        url = homepage + "/roms/vendor-12997-"
        for i in range(4):  # 控制爬取的页数
            url = url + str(i+1) + ".html"
            firmware.get_firmware(url, savepath)
            break

        # 磊科 Netcore
        savepath = "Netcore"
        firmware.makedir(savepath)
        url = homepage + "/roms/vendor-8806-"
        for i in range(2):  # 控制爬取的页数
            url = url + str(i+1) + ".html"
            firmware.get_firmware(url, savepath)
            break

        # 网件 NETGEAR
        savepath = "NETGEAR"
        firmware.makedir(savepath)
        url = homepage + "/roms/vendor-8819-"
        for i in range(2):  # 控制爬取的页数
            url = url + str(i+1) + ".html"
            firmware.get_firmware(url, savepath)
            break

        # 小米 Xiaomi
        savepath = "Xiaomi"
        firmware.makedir(savepath)
        url = homepage + "/roms/vendor-14593.html"
        firmware.get_firmware(url, savepath)

        # D-Link   固件下载
        savepath = "D-Link"
        firmware.makedir(savepath)
        url = homepage + "/roms/vendor-3132-"
        for i in range(2):  # 控制爬取的页数
            url = url + str(i+1) + ".html"
            firmware.get_firmware(url, savepath)
            break

        # 极路由 HiWiFi
        savepath = "HiWiFi"
        firmware.makedir(savepath)
        url = homepage + "/roms/vendor-16501.html"
        for i in range(2):  # 控制爬取的页数
            url = url + str(i+1) + ".html"
            firmware.get_firmware(url, savepath)
            break

        # 新路由 Newifi
        savepath = "Newifi"
        firmware.makedir(savepath)
        url = homepage + "/roms/vendor-16502.html"
        firmware.get_firmware(url, savepath)

        # 华硕 ASUS
        savepath = "ASUS"
        firmware.makedir(savepath)
        url = homepage + "/roms/vendor-1130.html"
        firmware.get_firmware(url, savepath)

