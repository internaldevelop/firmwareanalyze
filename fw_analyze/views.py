from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from common.utils.http_request import req_get_param
from common.response import app_ok_p, app_err
from common.error_code import Error
import binwalk


def index(request):
    return HttpResponse("Hello firmware analyze.")

def binwalk_scan_signature(request):
    filename = req_get_param(request, 'filename')
    try:
        for module in binwalk.scan(filename, signature=True, quiet=True):
            print("%s Results:" % module.name)
            for result in module.results:
                print("\t%s    0x%.8X    %s" % (result.file.path, result.offset, result.description))
    except binwalk.ModuleException as e:
        print("Critical failure:", e)
    return app_ok_p('binwalk OK.')

# 架构识别
def binwalk_scan_opcodes(request):
    filename = req_get_param(request, 'filename')
    #print(filename)
    # filename = "D:/code/work/firmwareanalyze/HC5611.bin"
    structure = '';
    try:
        for module in binwalk.scan(filename, opcodes=True, quiet=True):
            print("%s Results:" % module.name)
            for result in module.results:
                print("\t%s    0x%.8X    %s" % (result.file.path, result.offset, result.description))
                if ("X86" in result.description):
                    structure = 'X86'
                    break;
                elif ("ARM" in result.description):
                    structure = "ARM"
                    break;
                elif ("MIPS" in result.description):
                    structure = "MIPS"
                    break;
                else:
                    structure = "PowerPC"
                    break;
    except binwalk.ModuleException as e:
        print("Critical failure:", e)
        return app_err(Error.INTERNAL_EXCEPT)
    return app_ok_p({'structure': structure,})

# 抽取文件
def binwalk_file_extract(request):
    filename = req_get_param(request, 'filename')
    try:
        for module in binwalk.scan(filename, signature=True, quiet=True, extract=True):
            for result in module.results:
                if result.file.path in module.extractor.output:
                    # These are files that binwalk carved out of the original firmware image, a la dd
                    if result.offset in module.extractor.output[result.file.path].carved:
                        print
                        "Carved data from offset 0x%X to %s" % (
                        result.offset, module.extractor.output[result.file.path].carved[result.offset])
                    # These are files/directories created by extraction utilities (gunzip, tar, unsquashfs, etc)
                    if result.offset in module.extractor.output[result.file.path].extracted:
                        print
                        "Extracted %d files from offset 0x%X to '%s' using '%s'" % (
                        len(module.extractor.output[result.file.path].extracted[result.offset].files),
                        result.offset,
                        module.extractor.output[result.file.path].extracted[result.offset].files[0],
                        module.extractor.output[result.file.path].extracted[result.offset].command)
    except binwalk.ModuleException as e:
        print("Critical failure:", e)
        return app_err(Error.INTERNAL_EXCEPT)
    return app_ok_p({'extract': 'ok',})