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

library_path = r'C:\BRAutomation\AS\Library'

# KOD TO SZUKANIA PLIKÓW BIBLIOTEK
def find_modules(disk_path):
    for dirpath, dirnames, filenames in os.walk(disk_path):
        for dirname in dirnames:
            if dirname == "BRAutomation":
                dirname = os.path.join(dirpath, dirname)
                mypath = dirpath + r'BRAutomation/AS412/AS/Hardware/Modules'
                modules = [f for f in listdir(mypath) if isdir(join(mypath, f))]
                return modules,mypath



# KOD TO SZUKANIA PLIKÓW MODUŁU I BIBLIOTEK
def find_modules(disk_path):
    for dirpath, dirnames, filenames in os.walk(disk_path):
        for dirname in dirnames:
            if dirname == "BRAutomation":
                dirname = os.path.join(dirpath, dirname)
                BRAutomation_path = dirpath + r'BRAutomation/AS412/AS/Hardware/Modules'
                Library_path = dirpath + r'BRAutomation/AS/Library'
                modules = [f for f in listdir(BRAutomation_path) if isdir(join(BRAutomation_path, f))]
                libraries = [g for g in listdir(Library_path) if isdir(join(Library_path, g))]
                return modules,BRAutomation_path,libraries


def find_module_version(module,path):
    path = path + '/' + module
    version = [f for f in listdir(path) if isdir(join(path, f))]
    return version


def get_to_files(path, name):
    input_path = path + chr(92) + name
    pathHWL_fun = input_path + r'\Physical\Config1\Hardware.hwl'
    pathHW_fun = input_path + r'\Physical\Config1\Hardware.hw'
    pathL = input_path + r'\Logical\Libraries\Package.pkg'
    try:
        treeHWL_fun = etree.parse(pathHWL_fun)
        rootHWL_fun = treeHWL_fun.getroot()
    except:
        print('ERROR - Cannot get to file in destination:', pathHWL_fun)
        exit()
    try:
        treeHW_fun = etree.parse(pathHW_fun)
        rootHW_fun = treeHW_fun.getroot()
    except:
        print('ERROR - Cannot get to file in destination:', pathHW_fun)
        exit()
    try:
        treeL = etree.parse(pathL)
        rootL = treeL.getroot()
    except:
        print('ERROR - Cannot get to file in destination:', pathL)
        exit()
    return rootHW_fun, rootHWL_fun, rootL, pathHW_fun, pathHWL_fun, pathL


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

def add_library(root, path, name,descript):
    element = etree.SubElement(root, 'Object', Type="Library", Language="Binary", Description=descript)
    element.text = name
    root[0].append(element)
    etree.ElementTree(root).write(path)
    # shutil.move(src,dst)
    print(element.tag, element.attrib, element.tail)
    print(path)


if __name__ == '__main__':
    module_list,module_path,libraries = find_modules(which_disk_br) #lista modułów zainstalowanych na dysku C
    chosen_module = module_list[1753]
    module_version = find_module_version(chosen_module,module_path)
    chosen_module1 = module_list[1866]
    module_version1 = find_module_version(chosen_module1, module_path)
    chosen_module2 = module_list[1527]
    module_version2 = find_module_version(chosen_module2, module_path)

    rootHW, rootHWL, rootLib, pathHW, pathHWL, pathLib = get_to_files(as_project_path, filename)
    # add_element(rootHW, rootHWL, pathHW, pathHWL, chosen_module, module_version[0])
    # add_element(rootHW, rootHWL, pathHW, pathHWL, chosen_module1, module_version1[0])
    # add_element(rootHW, rootHWL, pathHW, pathHWL, chosen_module2, module_version2[0])
    lib_descript = 'program added library'
    add_library(rootLib, pathLib, libraries[72], lib_descript)
    print('END')
