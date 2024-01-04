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

# CONSTANTS
BRAutomation_path = ''
IF6busy = False
last = ''
LIB_DESCRIPT = 'program added library'
project_path = as_project_path + chr(92) + filename

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
                global BRAutomation_path
                BRAutomation_path = dirpath + r'BRAutomation/AS412/AS/Hardware/Modules'
                Library_path = dirpath + r'BRAutomation/AS/Library'
                modules = [f for f in listdir(BRAutomation_path) if isdir(join(BRAutomation_path, f))]
                libraries = [g for g in listdir(Library_path) if isdir(join(Library_path, g))]
                return modules, BRAutomation_path, libraries


def find_module_version(module, path):
    path = path + '/' + module
    version = [f for f in listdir(path) if isdir(join(path, f))]
    return version


def get_to_files(path):
    pathHWL_fun = path + r'\Physical\Config1\Hardware.hwl'
    pathHW_fun = path + r'\Physical\Config1\Hardware.hw'
    pathL = path + r'\Logical\Libraries\Package.pkg'
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
    name = type + str
    element = etree.SubElement(root_hwl, 'Module', Name=name, Type=type, X='450', Y='450')
    root_hwl[1][0].append(element)
    etree.ElementTree(root_hwl).write(path_hwl)
    print(element.tag, element.attrib)

    element = etree.SubElement(root_hw, 'Module', Name=name, Type=type, Version=version[0])
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


def add_mapping(path, PLC):
    # WYRZUCA CAŁY PLIK I NADPISUJE
    text_file = open(path + "/Physical/Config1/" + PLC + "/IoMap.iom", "w")
    text_file.write('VAR_CONFIG\n')
    # NALEZY DODAC 4 INFORMACJE TUTAJ
    # Nazwa zmiennej - WE/WY - MODUŁ - Channel
    # text_file.write('::{0} AT %{1}X."{2}".{3};\n'.format(,,,)
    text_file.write('::ASEG1 AT %IX."X20AI4632P".StaleData; ::ASEG AT %IX."X20AI4632P".ModuleOk;\n')
    text_file.write('END_VAR\n')
    text_file.close()
    print('Mapping added')


def add_global_var(path, list_var):
    # DEKLARACJA STRUKTUR / VAR TYPE
    text_file = open(path + "/Logical/Global.typ", "w")
    text_file.write('TYPE\n')
    for a in list_var:
        text_file.write('{0}_type : STRUCT\n'.format(a))
#     text_file.write('''IOMODULE : STRUCT
# ModuleOK : BOOL;
# In1 : USINT;
# iN2 : USINT;
# in3 : USINT;
# END_STRUCT;\n''')
    text_file.write('END_TYPE\n')
    text_file.close()

    # DEKLARACJA ZMIENNYCH GLOBALNYCH STRUKTUR
    text_file = open(path + "/Logical/Global.var", "w")
    text_file.write('VAR\n')
    #TU WPISZ
    text_file.write('END_VAR\n')
    text_file.close()


def find_IO_VarType(path, modules, versions):
    i = 0
    f = 0
    var_list = []
    for module in modules:
        inputpath = path + r'/{0}/{1}/{2}.hwx'.format(module, (versions[i])[0], module)
        i = i + 1
        tree = etree.parse(inputpath)

        # Przestrzeń nazw XML
        ns = {'ns': 'http://br-automation.co.at/AS/HardwareModule'}

        # Wyszukanie elementów Channel dla parenta <Channels Target="SG3">
        channels_sg3 = tree.xpath('//ns:Channels[@Target="SG3"]/ns:Channel', namespaces=ns)

        # Wyświetlenie ilości Channel dla parenta <Channels Target="SG3">
        # print(f"{module} - Ilość: {len(channels_sg3)}")

        # Przeanalizowanie linii <Parameter ID="Type" Value="BOOL" Type="STRING" /> w każdym z pozyskanych Channel
        for channel in channels_sg3:
            type_parameter = channel.xpath('./ns:Parameter[@ID="Type"][@Type="STRING"]', namespaces=ns)

            if type_parameter:
                value = type_parameter[0].get('Value')
                channel_value = f"{module} {channel.get('ID')} {value}"
                # print(channel_value)
                var_list.append([module])
                var_list[f].append(channel.get('ID'))
                var_list[f].append(value)
                f = f + 1
            else:
                print(f"  Brak informacji {channel.get('ID')}")

    return var_list

if __name__ == '__main__':
    module_list, module_path, libraries = find_modules(which_disk_br)  # lista modułów zainstalowanych na dysku C

    # 0 - 951 STARSZE I ROZNE
    # 952  - 1455 ACOPOSY
    # 1480 - 1520 KAMERY WIZYJNE
    # 1520 - 2093 MODUŁY IO (NIEKONIECZNIE WSZYSTKIE SĄ IO)
    chosen_module = [module_list[1828],module_list[1864],module_list[1546],module_list[1529]]
    module_version = [find_module_version(chosen_module[0], module_path),find_module_version(chosen_module[1], module_path)
        ,find_module_version(chosen_module[2], module_path),find_module_version(chosen_module[3], module_path)]

    rootHW, rootHWL, rootLib, pathHW, pathHWL, pathLib, treeHW = get_to_files(project_path)

    for z in range(len(chosen_module)):
        add_IO(rootHW, rootHWL, pathHW, pathHWL, chosen_module[z-1], module_version[z-1], module_list, module_path, treeHW)

    packed_var = find_IO_VarType(BRAutomation_path, chosen_module, module_version)
    for a in packed_var:
        print(a)
    # add_global_var(project_path, packed_var)
    # add_mapping(project_path, PLCname)
    # add_library(rootLib, pathLib, libraries[105], LIB_DESCRIPT)

    # print(etree.tostring(root, pretty_print=True, encoding='unicode'))
    print('END')
