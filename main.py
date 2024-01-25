import lxml.etree as etree
import string
import random
import os
from os import listdir
from os.path import isfile, join, isdir

# INPUTS
which_disk_br = 'C:/'
as_project_path = r'C:\projects'
filename = r'TESTLD'
library_path = r'C:\BRAutomation\AS\Library'  # to chyba można usunac bo jest dysk
PLCname = 'X20CP1584'

# CONSTANTS
module_names = []
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


# # KOD TO SZUKANIA PARAMETRÓW MODUŁÓW
# def find_param_of_modules(path,module,ver):
#     path = path + '/' + module + '/' + ver[0]
#     print(path)
#     for dirpath, dirnames, filenames in os.walk(path):
#         for filename in filenames:
#             if filename.endswith(".hwx"):
#                 param_path = os.path.join(dirpath, filename)
#                 print(param_path)
#                 return param_path


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


# ----------------------------------------TU SKOŃCZYŁEM--------COS NIEDZIAŁA----------------------------------------
# def find_connector_info(path, module, ver):
#     path = path + '/' + module + '/' + ver[0] + '/' + module + '.hwx'
#     try:
#         tree = etree.parse(path)
#         root = tree.getroot()
#     except:
#         print('ERROR - Cannot get to file in destination:', path)
#         exit()
#
#     # Znalezienie elementów Connector pod Connectors
#     connector_elements = root.findall(".//Connectors/Connector")
#
#     connector_info_list = []
#
#     # Iteracja po znalezionych elementach Connector
#     for connector in connector_elements:
#         connector_name = connector.get("Name")
#         module_id = connector.find("./AutoConnect").get("ModuleID")
#         connector_name_autoconnect = connector.find("./AutoConnect").get("ConnectorName")
#
#         connector_info_list.append({
#             "ConnectorName": connector_name,
#             "ModuleID": module_id,
#             "ConnectorNameAutoConnect": connector_name_autoconnect
#         })
#
#     for connector_info in connector_elements:
#         print("ConnectorName:", connector_info["ConnectorName"])
#         print("ModuleID:", connector_info["ModuleID"])
#         print("ConnectorNameAutoConnect:", connector_info["ConnectorNameAutoConnect"])
#         print("-" * 30)
#
#     return connector_info_list

def extract_connector_and_classification_info(path, module, ver):
    # Parsowanie XML
    path = path + '/' + module + '/' + ver[0] + '/' + module + '.hwx'
    try:
        tree = etree.parse(path)
        root = tree.getroot()
    except:
        print('ERROR - Cannot get to file in destination:', path)
        exit()

    ns = {'hw': 'http://br-automation.co.at/AS/HardwareModule'}
    e = "//hw:Classification/*"
    classification_elements = root.xpath(e, namespaces=ns)

    connector_info = []
    connector_elements = root.xpath("//hw:Connectors/hw:Connector", namespaces=ns)
    for connector in connector_elements:
        connector_name = connector.get("Name")
        autoconnect_elements = connector.xpath("./hw:AutoConnect", namespaces=ns)
        for autoconnect in autoconnect_elements:
            module_id = autoconnect.get("ModuleID")
            connector_name_autoconnect = autoconnect.get("ConnectorName")
            connector_info.append(
                [['Name', connector_name], ['ModuleID', module_id], ['AutoConnect', connector_name_autoconnect]])

    classification_info = []
    for elem in classification_elements:
        classification_info.append([elem.tag.split('}')[1], elem.get("Value")])

    return classification_info, connector_info


# ----------------------------------------------------------------------------------------------------------

def add_IO(root_hw, root_hwl, path_hw, path_hwl, type, version, m_list, m_path, class_d, connection_d):
    global IF6busy
    global last
    global module_names
    str = get_random_string(1)
    name = type + str
    element = etree.SubElement(root_hwl, 'Module', Name=name, Type=type, X='450', Y='450')
    root_hwl[1][0].append(element)
    etree.ElementTree(root_hwl).write(path_hwl)
    # print(element.tag, element.attrib)

    element = etree.SubElement(root_hw, 'Module', Name=name, Type=type, Version=version[0])
    root_hw.append(element)
    # print(element.tag, element.attrib)
    module_names.append(name)

    if class_d and connection_d:
        typeTB = connection_d[0][1][1]
        typeBM = connection_d[1][1][1]
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
        etree.SubElement(element, 'Connection', Connector=connection_d[1][0][1], TargetModule=nameBM,
                         TargetConnector=connection_d[1][2][1])
        etree.SubElement(element, 'Connection', Connector=connection_d[0][0][1], TargetModule=nameTB,
                         TargetConnector=connection_d[0][2][1])

    if not IF6busy:
        etree.ElementTree(root_hw).write(path_hw)
        # CONNECTIONS - DODANIE CHILD DO BM (PODSTAWKA DO AKTUALNIE WOLNEGO SLOTA)
        ns = {'hw': 'http://br-automation.co.at/AS/Hardware'}
        a = "//hw:Module[@Name='{}']/hw:Connection/@TargetConnector".format(nameBM)
        checkIF6slot = root_hw.xpath(a, namespaces=ns)
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
    # print(element.tag, element.attrib, element.tail)
    # print(path)

    # DEKLARACJA STRUKTUR / GLOBAL VAR / IO MAP


def add_global_var(path, list_var, plc):
    i = 0
    module_names.sort()
    text_file_type = open(path + "/Logical/Global.typ", "w")
    text_file_var = open(path + "/Logical/Global.var", "w")
    text_file_mapp = open(path + "/Physical/Config1/" + plc + "/IoMap.iom", "w")
    text_file_type.write('TYPE\n')
    text_file_var.write('VAR\n')
    text_file_mapp.write('VAR_CONFIG\n')
    for name in list_var:
        name[0] = name[0].replace('-', '_')
        struct_type = '{0}_type'.format(name[0])
        struct_name = 'IO_{0}'.format(name[0])
        text_file_var.write('{0} : {1};\n'.format(struct_name, struct_type))
        text_file_type.write('{0} : STRUCT\n'.format(struct_type))
        for channel in list_var[i]:
            if channel == list_var[i][0]:
                continue
            text_file_type.write('{0} : {1};\n'.format(channel[0], channel[1]))

            letter_I_or_Q = 'I' if channel[2] == 'IN' else 'Q'
            letter_X_or_W_or_B_or_DW = 'X' if channel[1] == 'BOOL' else \
                'W' if channel[1] == 'INT' or channel[1] == 'UINT' or channel[1] == 'WORD' else \
                    'B' if channel[1] == 'USINT' or channel[1] == 'SINT' or channel[1] == 'BYTE' else \
                        'D' if channel[1] == 'DINT' or channel[1] == 'REAL' or channel[1] == 'DWORD' else None

            if (not letter_X_or_W_or_B_or_DW or not letter_I_or_Q):
                print('ERROR - IO DATA NOT FITTED THE CODE :((')
            # print('::{0}.{1} AT %{2}{3}."{4}".{5};\n'.format(struct_name, channel[0], letter_I_or_Q, letter_X_or_W , module_names[i], channel[0]))
            text_file_mapp.write(
                '::{0}.{1} AT %{2}{3}."{4}".{5};\n'.format(struct_name, channel[0], letter_I_or_Q, letter_X_or_W_or_B_or_DW,
                                                           module_names[i], channel[0]))
        text_file_type.write('END_STRUCT;\n')
        i = i + 1
    text_file_type.write('END_TYPE\n')  # TYPE
    text_file_type.close()
    text_file_var.write('END_VAR\n')  # VAR
    text_file_var.close()
    text_file_mapp.write('END_VAR\n')  # MAPP
    text_file_mapp.close()


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
        old = ''
        # Przeanalizowanie linii <Parameter ID="Type" Value="BOOL" Type="STRING" /> w każdym z pozyskanych Channel
        for channel in channels_sg3:
            type_parameter = channel.xpath('./ns:Parameter[@ID="Type"]', namespaces=ns)
            direction_parameter = channel.xpath('./ns:Parameter[@ID="Direction"]', namespaces=ns)
            if type_parameter and direction_parameter:
                value = type_parameter[0].get('Value')
                dir = direction_parameter[0].get('Value')
                # channel_value = f"{module} {channel.get('ID')} {value} {dir}"
                # print(channel.get('ID'))
                # print(value)
                if module != old:
                    var_list.append([module])
                    f = f + 1

                var_list[f - 1].append([channel.get('ID'), value, dir])
                old = module
            else:
                print(f"  Brak informacji {channel.get('ID')}")
    return var_list


if __name__ == '__main__':
    module_list, module_path, libraries = find_modules(which_disk_br)  # lista modułów zainstalowanych na dysku C

    # 0 - 951 STARSZE I ROZNE
    # 952  - 1455 ACOPOSY
    # 1480 - 1520 KAMERY WIZYJNE
    # 1520 - 2093 MODUŁY IO (NIEKONIECZNIE WSZYSTKIE SĄ IO)

    chosen_module = []
    module_version = []
    table = ['X20AI1744', 'X20AI4636', 'X20DOD322', 'X20DO4633']


    # ZMIEN TE DWA W JEDNO ---------------
    for name in table:
        try:
            chosen_module.append(module_list[module_list.index(name)])
            module_version.append(find_module_version(name, module_path))
        except:
            print('Module {} not found in files'.format(name))

    rootHW, rootHWL, rootLib, pathHW, pathHWL, pathLib, treeHW = get_to_files(project_path)

    for z in range(len(chosen_module)):
        class_data, connection_data = extract_connector_and_classification_info(module_path, chosen_module[z - 1],
                                                                                module_version[z - 1])
        add_IO(rootHW, rootHWL, pathHW, pathHWL, chosen_module[z - 1], module_version[z - 1], module_list, module_path,
               class_data, connection_data)
    packed_var = find_IO_VarType(BRAutomation_path, chosen_module, module_version)
    packed_var.sort()
    add_global_var(project_path, packed_var, PLCname)
    # add_library(rootLib, pathLib, libraries[105], LIB_DESCRIPT)

    # print(etree.tostring(root, pretty_print=True, encoding='unicode'))
    print('END')
