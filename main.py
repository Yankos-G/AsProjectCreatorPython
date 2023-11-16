import xml.etree.ElementTree as ET

# inputs
as_project_path = r'C:\projects'
filename = r'Clear'


def get_to_file(path, name):
    input_path = path + chr(92) + name + r'\Physical\Config1'
    pathHWL = input_path + r'\Hardware.hwl'
    pathHW = input_path + r'\Hardware.hw'
    rootHWL=3
    # try:
    #     treeHWL = ET.parse(pathHWL)
    #     rootHWL = treeHWL.getroot()
    # except:
    #     print('Cannot get to file in destination:', pathHWL)
    #     exit()
    try:
        treeHW = ET.parse(pathHW)
        rootHW = treeHW.getroot()

    except:
        print('Cannot get to file in destination:', pathHW)
        exit()

    return rootHW, rootHWL


def show_attrib(root):
    for x in root:
        print(x.tag[40:])
        print(x.attrib)


# for x in rootHW.iter(rootHW[0].tag):
#     print(x.tag[40:])
#     print(x.attrib)
#
#
# print(myroot[1][0].attrib.keys())
# print(myroot[1][0].attrib.values())
# print(myroot[1][0].attrib.get('Type')) #szuka w keys
# print(myroot[1][0].attrib)
#

# #SPRAWDZANIE ZMIAN - NIEKONIECZNE
# print('=================OLD=============================')
# file = open(route,'r')
# print(file.read())

# myroot[1][3].set('Name','AAAA')
# rootHW.makeelement('tag', a)
# ET.SubElement(rootHW[1][0], 'AAAAAAAAAAAAAA', a)
# #
#
# treeHW.write(pathHW)
# print('=================NEW=============================')
# file = open(route,'r')
# print(file.read())
#
#
#
if __name__ == '__main__':
    rootHW, rootHWL = get_to_file(as_project_path, filename)
    show_attrib(rootHW)

