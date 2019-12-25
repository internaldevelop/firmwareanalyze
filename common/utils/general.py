from dateutil.relativedelta import relativedelta
import json
from datetime import date, datetime, timedelta

import os
import tarfile
import os.path
import zipfile
import rarfile
import patoolib
import py7zr
# from easy7zip import easy7zip
# from py7zr import pack_7zarchvie, unpack_7zarchive
from py7zr import unpack_7zarchive
import shutil


def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)


class SysUtils:

    # @staticmethod
    # def makedir(self, name):
    #     path = os.path.join(self.base_path, name)
    #     isExist = os.path.exists(path)
    #     if not isExist:
    #         os.makedirs(path)
    #         print("File has been created.")
    #     else:
    #         print('OK!The file is existed. You do not need create a new one.')
    #     os.chdir(path)

    @staticmethod
    def get_now_time():
        return datetime.now()

    @staticmethod
    def get_now_time_str():
        return SysUtils.get_now_time().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_time_delta_days(delta_days):
        now = datetime.now()
        new_time = now + timedelta(days=delta_days)
        return new_time

    @staticmethod
    def get_time_delta_years(delta_years):
        now = datetime.now()
        new_time = now + relativedelta(years=delta_years)
        return new_time

    @staticmethod
    def print_time(time):
        print(time)

    @staticmethod
    def copy_dict(src_dict, key_list):
        dest_dict = {}
        for key in key_list:
            if key in src_dict.keys():
                dest_dict[key] = src_dict[key]
            else:
                dest_dict[key] = ''
        return dest_dict

    @staticmethod
    def grid_out_to_dict(grid_out):
        if grid_out is None:
            return None
        dest_dict = {'filename': grid_out.filename, 'aliases': grid_out.aliases[0],
                     'content_type': grid_out.content_type, 'length': grid_out.length, 'name': grid_out.name}
        # dest_dict['content'] = grid_out.read()
        return dest_dict

    @staticmethod
    def match_convert(template, input):
        temp_src = []
        temp_dest = []
        for item in template:
            temp_src.append(item[0])
            temp_dest.append(item[1])
        try:
            index = temp_src.index(input)
        except ValueError:
            return None
        else:
            return temp_dest[index]

    @staticmethod
    def parse_file_suffix(file_path):
        parsed = os.path.splitext(file_path)
        name = parsed[0]
        suffix = parsed[1].lstrip('.').lower()
        return suffix

    @staticmethod
    def add_plain_text_file_suffix(file_path):
        not_plain_text_suffixs = ['docx', 'eml', 'exe', 'gz', 'ics', 'mid', 'pdf', 'pm', 'rar', 'sys', 'xsl', 'zip', ]
        suffix = SysUtils.parse_file_suffix(file_path)
        if suffix in not_plain_text_suffixs:
            return file_path + '.bin'
        return file_path + '.txt'

    @staticmethod
    def parse_file_type(file_path):
        suffix = SysUtils.parse_file_suffix(file_path)
        template = [['as', 'Action Script'], ['asc', 'Active Server Pages'], ['asm', 'ASM'],
                    ['asp', 'Active Server Pages'], ['bat', 'Batch'], ['c', 'C'], ['cfm', 'ColdFusion Markup'],
                    ['cpp', 'C++'], ['cob', 'COBOL'], ['cs', 'C#'], ['delphi', 'delphi'], ['docx', 'Word'],
                    ['eml', 'Email'], ['exe', 'Execute'], ['go', 'Golang'], ['gz', 'gzip'], ['htm', 'html'],
                    ['html', 'html'], ['ics', 'Calendar'], ['java', 'java'], ['js', 'Java Script'],
                    ['jsp', 'Java Server Page'], ['mid', 'MIDI'], ['md', 'Mark Down'], ['nasl', 'Nessus Script'],
                    ['nasm', 'ASM'], ['nse', 'Nmap Script'], ['pas', 'Pascal'], ['pdf', 'PDF'], ['php', 'PHP'],
                    ['pl', 'Perl'], ['pm', 'Perl Module'], ['py', 'python'], ['rar', 'rar'], ['rb', 'ruby'],
                    ['s', 'ASM'], ['sh', 'Shell Script'], ['sql', 'SQL'], ['sys', 'system'], ['tcsh', 'TCSH Script'],
                    ['txt', 'Text'], ['vb', 'Visual Basic'], ['vbs', 'VB Script'], ['wsf', 'Windows Script'],
                    ['xml', 'XML'], ['xhtml', 'XML html'], ['xsl', 'Excel'], ['zip', 'zip'], ]
        # template = [['pdf', 'PDF'], ]
        type = SysUtils.match_convert(template, suffix)
        if type is None:
            type = 'unknown'
        return type

    # 解压tgz压缩文件

    def un_tgz(filename):
        tar = tarfile.open(filename)
        # 判断同名文件夹是否存在，若不存在则创建同名文件夹
        if os.path.isdir(os.path.splitext(filename)[0]):
            pass
        else:
            os.mkdir(os.path.splitext(filename)[0])
        tar.extractall(os.path.splitext(filename)[0])
        tar.close()

    def un_tar(file_name):
        # untar zip file"""
        tar = tarfile.open(file_name)
        names = tar.getnames()
        if os.path.isdir(file_name + "_files"):
            pass
        else:
            os.mkdir(file_name + "_files")
        #由于解压后是许多文件，预先建立同名文件夹
        for name in names:
            tar.extract(name, file_name + "_files/")
        tar.close()

    #解压rar压缩包
    def un_rar(filename):
        rar = rarfile.RarFile(filename)
        #判断同名文件夹是否存在，若不存在则创建同名文件夹
        if os.path.isdir(os.path.splitext(filename)[0]):
            pass
        else:
            os.mkdir(os.path.splitext(filename)[0])
        rar.extractall(os.path.splitext(filename)[0])


    def un_zip(filename):
        # zip_file2_path = r'F:\tk_demo.zip'
        # zipfile提供的压缩方法有：
        # ZIP_STORED，ZIP_DEFLATED， ZIP_BZIP2和ZIP_LZMA
        # ZIP_STOREED：只是作为一种存储，实际上并未压缩
        # ZIP_DEFLATED：用的是gzip压缩算法
        # ZIP_BZIP2：用的是bzip2压缩算法
        # ZIP_LZMA：用的是lzma压缩算法
        unzip_files = zipfile.ZipFile(filename, mode='r', compression=zipfile.ZIP_STORED)
        unzip_files.extractall()
        unzip_files.close()

    def un_patool(filename):
        # patoolib.extract_archive(filename, outdir="/tmp")
        patoolib.extract_archive(filename)

    def un_py7zr(filename):
        extract_dir = os.getcwd() + "\\firmware"
        if os.path.isdir(extract_dir):
            pass
        else:
            os.mkdir(extract_dir)

        is7z = py7zr.is_7zfile(filename)
        py7zr.SevenZipFile
        if is7z:
            ret = py7zr.unpack_7zarchive(filename, extract_dir)
            print(ret)
        else:
            print('unknow file type')
        return extract_dir

    def un_7z(filename):
        # register file format at first.
        # shutil.register_archive_format('7zip', pack_7zarchive, description='7zip archive')
        shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
        # extraction
        shutil.unpack_archive(filename)


class TimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
