import xml.etree.ElementTree as ET

route = 'C:\projects\Clear\Physical\Config1\Hardware.hwl'
mytree = ET.parse(route)
myroot = mytree.getroot()
#
# # print(myroot[1].tag)
# for x in myroot[1]:
#     a=print(x.attrib)
#
# # for x in myroot.iter(myroot[0].tag):
# #     print(x.attrib)
#

print(myroot[1][0].attrib.keys())
print(myroot[1][0].attrib.values())
print(myroot[1][0].attrib.get('Type')) #szuka w keys
print(myroot[1][0].attrib)

print('=================OLD=============================')
file = open(route,'r')
print(file.read())

myroot[1][0].set('Name','AAAAAa')

mytree.write(route)
print('=================NEW=============================')
file = open(route,'r')
print(file.read())



if __name__ == '__main__':
    print('')
    input()

