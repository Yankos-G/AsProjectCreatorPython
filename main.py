import lxml.etree as etree
from lxml import objectify
import string
import random
import os
from os import listdir
from os.path import isfile, join, isdir
import sys

# a=sys.argv[1]

# INPUTS
which_disk_br = 'C:/'


as_project_path = r'C:\projects'
filename = r'TESTLD'

library_path = r'C:\BRAutomation\AS\Library'

PLCname = 'X20CP1584'

# CONSTANT
IF6busy = False
last = ''
LIB_DESCRIPT = 'program added library'

# # KOD TO SZUKANIA PLIKÓW BIBLIOTEK
# def find_modules(disk_path):
#     for dirpath, dirnames, filenames in os.walk(disk_path):
#         for dirname in dirnames:
#             if dirname == "BRAutomation":
#                 dirname = os.path.join(dirpath, dirname)
#                 mypath = dirpath + r'BRAutomation/AS412/AS/Hardware/Modules'
#                 modules = [f for f in listdir(mypath) if isdir(join(mypath, f))]
#                 return modules,mypath


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
                return modules, BRAutomation_path, libraries


def find_module_version(module, path):
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
    return rootHW_fun, rootHWL_fun, rootL, pathHW_fun, pathHWL_fun, pathL, treeHW_fun


def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def add_IO(root_hw, root_hwl, path_hw, path_hwl, type, version, m_list, m_path, tree_hw):
    global IF6busy
    global last
    str = get_random_string(1)
    element = etree.SubElement(root_hwl, 'Module', Name=type + str, Type=type, X='450', Y='450')
    root_hwl[1][0].append(element)
    etree.ElementTree(root_hwl).write(path_hwl)
    print(element.tag, element.attrib)

    element = etree.SubElement(root_hw, 'Module', Name=type + str, Type=type, Version=version)
    root_hw.append(element)
    print(element.tag, element.attrib)

    typeTB = m_list[m_list.index('X20TB12')]
    typeBM = m_list[m_list.index('X20BM11')]
    m_verTB = find_module_version(typeTB, m_path)
    m_verBM = find_module_version(typeBM, m_path)
    nameBM = typeBM + str
    nameTB = typeTB + str
    print(nameBM)
    print(nameTB)
    elementTB = etree.SubElement(root_hw, 'Module', Name=nameTB, Type=typeTB, Version=m_verTB[0])
    root_hw.append(elementTB)
    elementBM = etree.SubElement(root_hw, 'Module', Name=nameBM, Type=typeBM, Version=m_verBM[0])
    root_hw.append(elementBM)

    # CONNECTIONS - DODANIE CHILD DO ELEMENTU (MODUŁ GŁOWNY Z POMOCNYMI)
    etree.SubElement(element, 'Connection', Connector='SL', TargetModule=nameBM,
                     TargetConnector='SL1')
    etree.SubElement(element, 'Connection', Connector='SS1', TargetModule=nameTB,
                     TargetConnector='SS')
    if not IF6busy:
        etree.ElementTree(root_hw).write(path_hw)
        # CONNECTIONS - DODANIE CHILD DO BM (PODSTAWKA DO AKTUALNIE WOLNEGO SLOTA)
        ns = {'hw': 'http://br-automation.co.at/AS/Hardware'}
        a = "//hw:Module[@Name='{}']/hw:Connection/@TargetConnector".format(nameBM)
        checkIF6slot = rootHW.xpath(a, namespaces=ns)
        print(checkIF6slot)

        print(last)
        etree.SubElement(elementBM, 'Connection', Connector='X2X1', TargetModule=PLCname,
                         TargetConnector='IF6')
        last = nameBM
        IF6busy = True
    else:
        print(last)
        etree.SubElement(elementBM, 'Connection', Connector='X2X1', TargetModule=last,
                         TargetConnector='X2X2')
        last = nameBM

    # ZAPIS DO PLIKU HW
    etree.ElementTree(root_hw).write(path_hw)

    return last


def add_library(root, path, name, descript):
    element = etree.SubElement(root, 'Object', Type="Library", Language="Binary", Description=descript)
    element.text = name
    root[0].append(element)
    etree.ElementTree(root).write(path)
    # shutil.move(src,dst)
    print(element.tag, element.attrib, element.tail)
    print(path)


if __name__ == '__main__':
    module_list, module_path, libraries = find_modules(which_disk_br)  # lista modułów zainstalowanych na dysku C

    # 0 - 951 STARSZE I ROZNE
    # 952  - 1455 ACOPOSY
    # 1480 - 1520 KAMERY WIZYJNE
    # 1520 - 2093 MODUŁY IO
    chosen_module = module_list[1530]
    module_version = find_module_version(chosen_module, module_path)

    rootHW, rootHWL, rootLib, pathHW, pathHWL, pathLib, treeHW = get_to_files(as_project_path, filename)

    add_IO(rootHW, rootHWL, pathHW, pathHWL, chosen_module, module_version[0], module_list, module_path, treeHW)
    add_IO(rootHW, rootHWL, pathHW, pathHWL, chosen_module, module_version[0], module_list, module_path, treeHW)

    # print(rootHW.find('Hardware'))
    # a = treeHW.findall('{http://br-automation.co.at/AS/Hardware}Module')
    # print(a)
    # print(type(a))

    # for neighbor in rootHW.iter():
    #     print(neighbor.attrib)

    # add_library(rootLib, pathLib, libraries[105], LIB_DESCRIPT)
    # print(etree.tostring(rootHW, pretty_print=True, encoding='unicode'))
    print('END')
