import os
import sys
import xlrd
import logging
import datetime
import xml.etree.ElementTree as ET
#import SourceCode.ReadInputResources.ReadInputResources as rir

#Methods
def getTimeStamp():
    timeStamp = datetime.datetime.now().timestamp().__str__()
    splitTimeStamp =timeStamp.split(".")
    return splitTimeStamp[0]

def getlogger():
    try:
        logging.basicConfig(filename="SessionLogs/"+"mmcXMLmapping"+getTimeStamp()+".log",level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    except FileNotFoundError as ex:
        os.mkdir("SessionLogs")
        logging.basicConfig(filename="SessionLogs/" + getTimeStamp() + "convertor.log", level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logger.debug("SessionLogs folder was missing, we have created it.")

    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    return logging

def getSheet():
    try:
        wb = xlrd.open_workbook(inputFilePath)
        sheet = wb.sheet_by_index(0)
        return sheet
    except FileNotFoundError as ex:
        logger.debug("Please make sure that Input Data is available at: InputResource\MasterCopyInputExcel.xlsx")
        logger.debug("SYSTEM MESSAGE: %s", ex)
        logger.debug("### Process Terminated ###")
        print("Please make sure that Input Data is available at: InputResource\MasterCopyInputExcel.xlsx")
        sys.exit()

#below code is to read all the tags name / Key Name
def getkeyTags():
    keyTags = getSheet().col_values(1)  #Note:- Here you will have to put column postion stating from 0.
    keyTags.pop(0)
    #print("TAGS", keyTags)
    return keyTags

#below code is to read all value in n column
#below method gives single XML values
def getxmlValueList():
    startCol = 2
    endCol = getSheet().ncols
    xmlValueList = []
    for i in range(startCol,endCol):
        eachXMLValue = getSheet().col_values(i)
        eachXMLValue.pop(0)
        xmlValueList.append(eachXMLValue)
    # print("XMLVALUES",xmlValueList)
    return xmlValueList

# creates & returns all sections in array named sections= ["eachSection1","eachSection1"]
def getmysectionstag(eachValue):

    # innermethod def
    # creates single section at a time.
    def getmysection(section):  # ^140~(D)~(D)
        subSectionPart = section.split("~")  # ["^140","(D)","(D)"]
        sectionPart = subSectionPart[0] #['^140']
        sectionPart = sectionPart[1:]  # 140 # sectionPart[1:] -> returns string

        subSectionPart.pop(0)  # ["D","D"]

        sectionTag = ET.Element('SECTION')

        sectionPartTag = ET.Element('SECTION_PART')
        sectionPartTag.text = sectionPart

        sectionTag.append(sectionPartTag)

        for eachSubSectionPart in subSectionPart:
            subSectionPartTag = ET.SubElement(sectionTag, 'SUB_SECTION_PART')
            subSectionPartTag.text = eachSubSectionPart
            # eachOutputFileData = ET.tostring(sectionTag, encoding="unicode")
            # print(eachOutputFileData)
            # tempName = "scratchXML{}.xml".format(lstSection.index(section))
            # eachOutputFile = open(tempName, "w")
            # eachOutputFile.write(eachOutputFileData)


        return sectionTag

    sections = eachValue
    lstSection = []
    lstSection = sections.split("#")
    lstSection.pop(0)  # [ '^140~(D)~(D)' , '^140~C' ]
    #sections = ET.ElementTree(element=None, file=None)
    sections = []
    for section in lstSection:
        sections.append(getmysection(section))  # ^140~(D)~(D)
        #print(sections)
    return sections

# creates unique xml file data & writes data to a output file
def getmyXML():
    # create the file structure
    xmlTag = ET.Element('XML')
    documentDetails = ET.SubElement(xmlTag, 'DOCUMENT_DETAILS')

    # Note:- xmlValueList  means XML values
    # Note:- Tags Values
    logger.debug("Total no. of XML data found from input file is: %s" ,len(getxmlValueList()))
    for eachXML in getxmlValueList():    #[['sagar','bbb','ccc'],[2,3,4],[3,4,5]]   ['A','B','C']
        fileName = ""
        count = 0
        sectionEL = ET.Element('')
        for eachValue in eachXML:
                eachKeyTag = ET.Element(getkeyTags()[count])
                try:
                    if isinstance(eachValue,float) or isinstance(eachValue,int) :
                        eachValue= str(int(eachValue))

                    eachKeyTag.text = eachValue
                except Exception as ex:
                    logger.debug("System Exception Message: %s", ex)
                    continue

                #if keyTags[count] == 'APPEAL_REF_NO':
                if getkeyTags()[count] == uniqueFileName:  #Note: This Should be unique else files will be replaced
                    if eachValue != '':
                        fileName = "{}.{}".format(eachValue,"xml")
                    else:
                        fileName = "noAppealRefNo{}.{}".format(getxmlValueList().index(eachXML),"xml")

                if getkeyTags()[count] == 'SECTIONS':
                    #print(ET.tostring(sectionEL))
                    sectionsinarray=[]
                    sectionsinarray = getmysectionstag(eachValue)
                    eachKeyTag.clear()
                    for everysection in sectionsinarray:
                        eachKeyTag.append(everysection) # Contains SECTIONS TAG

                (documentDetails).append(eachKeyTag)
                count += 1
        #creates our file counter format: [1/4]
        outputFileCounter = "[{}/{}]".format(getxmlValueList().index(eachXML) + 1, len(getxmlValueList()))
        # create a new XML file with the results
        try:
            #eachOutputFileData = ET.tostring(xmlTag,encoding="cp1252",xml_declaration=True) #cp1252 #unicode
            eachOutputFileData = ET.tostring(xmlTag, encoding='UTF-8', method='xml',xml_declaration=True).decode()
        except TypeError as ex:
            logger.debug("%s Output XML, was not created, due some numeric or decimal value, plz check the following erroneous value of this XML in Input File ",outputFileCounter)
            logger.debug("%s System Exception Message: %s",outputFileCounter,ex)
            continue

        eachOutputFile=''
        try:
            fileName = outFilePath + fileName
            eachOutputFile = open(fileName, "w")
        except FileNotFoundError as ex :
            os.mkdir("OutputResource")
            eachOutputFile = open(fileName, "w")
            logger.debug("OutputResource folder was missing, we have created it.")

        #actually create file
        #try:
        eachOutputFile.write(eachOutputFileData.__str__())
        #except Exception as ex :
        #    print(ex)
        #    continue

        #outputFileCounter = "[{}/{}]".format(getxmlValueList().index(eachXML) + 1,len(getxmlValueList()))
        #fileName = var + fileName
        logger.debug('%s %s was created.', outputFileCounter,fileName)
        documentDetails.clear()
    logger.debug('### Process Ends ###')



#Prints Msg on Console
def getConsoleMsg(outFilePath):
    print("++++++++++++++++++++++++++++++++++++ Welcome +++++++++++++++++++++++++++++++++++++++++++++++\n\n")
    print("\nConversion In Progress..." +
          "\nPlease check the output at " + outFilePath +
          "\n\nTips:\n1. This window will get close automatically as soon as the conversion of all files is completed." +
          "\n2. To Terminate the conversion proccess press: CTRL + C" +
          "\n\n++++++++++++++++++++++++++++++++++++ Thankyou +++++++++++++++++++++++++++++++++++++++++++++++")


#Varibles
logger = getlogger()

inputFilePath = "InputResource\MasterCopyInputExcel.xlsx" #Note:- Hardcoding the Input File Path
outFilePath = "OutputResource\\"                          #Note:- Hardcoding the Input File Path
# outFilePathOrg   = input("Please Enter Output File Path( Ex: \"C:\\User\\abc\" ):\t")
# outFilePath = outFilePathOrg.replace("\\","\\\\")
# outFilePath = outFilePath + "\\\\"

#uniqueFileName= input("Please Enter the \"Tag Name\" ,whose value will be used as \"Output Filename\" :\t")
uniqueFileName = "APPEAL_REF_NO"
#uniqueFileName = uniqueFileName.upper()

#Note:- This can be use for getting the input file dynamically
#inputFilePath = input("Please Enter Input File Path:\t")
logger.debug('### Process Begins ###')

# prints msg on console
getConsoleMsg(outFilePath)

# it sets starting point for reading the excel input file
getSheet().cell_value(0, 0)

# try:
#     # creates the xml data & writes to output
#     getmyXML()
# except Exception as ex:
#     logger.debug("System Exception Message: %s",ex)
#     logger.debug("Something is not as per requirement, plz refer the userGuide.md and follow all the prerequites mentioned in it.")
#     logger.debug("AND RE-RUN THE UTILITY")

getmyXML()