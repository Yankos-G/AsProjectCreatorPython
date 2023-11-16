import lxml.etree as etree
import string
import random
import os
from os import listdir
from os.path import isfile, join, isdir

which_disk_br = 'C:/'

# inputs
as_project_path = r'C:\projects'
filename = r'Clear'
#chosen_module

# KOD TO SZUKANIA PLIKÓW MODUŁU
def find_modules(disk_path):
    for dirpath, dirnames, filenames in os.walk(disk_path):
        for dirname in dirnames:
            if dirname == "BRAutomation":
                dirname = os.path.join(dirpath, dirname)
                mypath = dirpath + r'BRAutomation/AS412/AS/Hardware/Modules'
                modules = [f for f in listdir(mypath) if isdir(join(mypath, f))]
                return modules,mypath


def find_module_version(module,path):
    path = path + '/' + module
    version = [f for f in listdir(path) if isdir(join(path, f))]
    return version

def get_to_file(path, name):
    input_path = path + chr(92) + name + r'\Physical\Config1'
    pathHWL_fun = input_path + r'\Hardware.hwl'
    pathHW_fun = input_path + r'\Hardware.hw'
    try:
        treeHWL_fun = etree.parse(pathHWL_fun)
        rootHWL_fun = treeHWL_fun.getroot()
    except:
        print('Cannot get to file in destination:', pathHWL_fun)
        exit()
    try:
        treeHW_fun = etree.parse(pathHW_fun)
        rootHW_fun = treeHW_fun.getroot()
    except:
        print('ERROR - Cannot get to file in destination:', pathHW_fun)
        exit()
    return rootHW_fun, rootHWL_fun, pathHW_fun, pathHWL_fun, treeHW_fun, treeHWL_fun


def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def add_element(root_hw, root_hwl, path_hw, path_hwl, type, version):
    str = get_random_string(1)
    element = etree.SubElement(root_hwl, 'Module', Name=type + str, Type=type, X='450', Y='450')
    root_hwl[1][0].append(element)
    etree.ElementTree(root_hwl).write(path_hwl)
    print(element.tag, element.attrib)

    element = etree.SubElement(root_hw, 'Module', Name=type + str, Type=type, Version=version)
    root_hw.append(element)
    etree.ElementTree(root_hw).write(path_hw)
    print(element.tag, element.attrib)

if __name__ == '__main__':
    module_list,module_path = find_modules(which_disk_br) #lista modułów zainstalowanych na dysku C
    chosen_module = module_list[300]
    module_version = find_module_version(chosen_module,module_path)
    rootHW, rootHWL, pathHW, pathHWL, treeHW, treeHWL = get_to_file(as_project_path, filename)
    add_element(rootHW, rootHWL, pathHW, pathHWL, chosen_module, module_version[0])
    print('END')
