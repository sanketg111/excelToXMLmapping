print( isinstance(3.6,float) )
print(str(int(3.4)))
print( isinstance(3.6,int) )

# import xml.etree.ElementTree as ET
#
#
#
#
#
#
#
# def getmysectionstag(eachValue):
#     # innermethod def
#     def getmysection(section):  # ^140~(D)~(D)
#         subSectionPart = section.split("~")  # ["^140","(D)","(D)"]
#         sectionPart = subSectionPart[0] #['^140']
#         sectionPart = sectionPart[1:]  # 140
#
#         subSectionPart.pop(0)  # ["D","D"]
#
#         sectionTag = ET.Element('SECTION')
#
#         sectionPartTag = ET.Element('SECTION_PART')
#         sectionPartTag.text = sectionPart
#
#         sectionTag.append(sectionPartTag)
#
#         for eachSubSectionPart in subSectionPart:
#             subSectionPartTag = ET.SubElement(sectionTag, 'SUB_SECTION_PART')
#             subSectionPartTag.text = eachSubSectionPart
#             # eachOutputFileData = ET.tostring(sectionTag, encoding="unicode")
#             # print(eachOutputFileData)
#             # tempName = "scratchXML{}.xml".format(lstSection.index(section))
#             # eachOutputFile = open(tempName, "w")
#             # eachOutputFile.write(eachOutputFileData)
#
#
#         return sectionTag
#
#     print(eachValue)
#     #sections = "#^240~(D)~(D)#^930~(C)"
#     sections = eachValue
#     lstSection = []
#     lstSection = sections.split("#")
#     lstSection.pop(0)  # [ '^140~(D)~(D)' , '^140~C' ]
#     #sections = ET.ElementTree(element=None, file=None)
#     sections = []
#     for section in lstSection:
#         sections.append(getmysection(section))  # ^140~(D)~(D)
#         print(sections)
#     return sections
#
# #eachOutputFileData = ET.tostring(getmysectionstag("#^240~(D)~(D)#^930~(C)"), encoding="unicode")
# #print(eachOutputFileData)
#
# eachOutputFileData = getmysectionstag("#^240~(D)~(D)#^930~(C)")
#
# for vertEl in eachOutputFileData:
#     print(ET.tostring(vertEl, encoding="unicode"))