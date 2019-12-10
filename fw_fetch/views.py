from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from common.response import app_ok_p, app_err_p, app_ok, app_err
from common.error_code import Error
from common.utils.http_request import req_get_param_int, req_get_param
import common.config

from fw_fetch.firmware_db import FirmwareDB
firmware_db = FirmwareDB()

def index(request):
    return HttpResponse("Hello firmware fetch.")

def fwdownload(request):
    print("run into fwdownload")
    url = req_get_param(request, 'url')
    print(url)
    # http://127.0.0.1:8000/firmwarefetch/fwdownload/?url=http://www.luyoudashi.com/roms
    fwdownload = firmware_db.fwdownload(url)

    # if fwdownload is None:
    #     return app_err(Error.FAIL_QUERY)
    # else:
    return app_ok_p(fwdownload)


def test(request):
    print("run into test")
    return app_ok_p('Test OK.')