from dateutil.relativedelta import relativedelta
import json
from datetime import date, datetime, timedelta
import os.path


def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)


class SysUtils:

    @staticmethod
    def makedir(self, name):
        path = os.path.join(self.base_path, name)
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            print("File has been created.")
        else:
            print('OK!The file is existed. You do not need create a new one.')
        os.chdir(path)

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


class TimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
