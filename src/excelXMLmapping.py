import xlrd
import xml.etree.ElementTree as ET
import datetime
import logging.handlers
import sys
#import mmcXMLmapping. #SourceCode.ReadInputResources.ReadInputResources as rir
import SourceCode.ReadInputResources.ReadInputResources as rir

timeStamp = datetime.datetime.now().timestamp().__str__()
splitTimeStamp =timeStamp.split(".")
timeStamp = splitTimeStamp[0]

try:
    logging.basicConfig(filename="SessionLogs/"+timeStamp+"convertor.log",level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
except FileNotFoundError as ex:
    os.mkdir("SessionLogs")
    logging.basicConfig(filename="SessionLogs/" + timeStamp + "convertor.log", level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    print(ex)


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

print("++++++++++++++++++++++++++++++++++++ Welcome +++++++++++++++++++++++++++++++++++++++++++++++\n\n")
#Note:- This can be use for getting the input file dynamically
#inputFilePath = input("Please Enter Input File Path:\t")
logging.debug('### Process Begins ###',)

inputFilePath = "InputResource\MasterCopyInputExcel.xlsx" #Note:- Hardcoding the Input File Path
outFilePath   = "OutputResource\\"
# outFilePathOrg   = input("Please Enter Output File Path( Ex: \"C:\\User\\abc\" ):\t")
# outFilePath = outFilePathOrg.replace("\\","\\\\")
# outFilePath = outFilePath + "\\\\"


uniqueFileName= input("Please Enter the \"Tag Name\" ,whose value will be used as \"Output Filename\" :\t")
#uniqueFileName = "pan"
uniqueFileName = uniqueFileName.upper()


print("\nConversion In Progress..."+
"\nPlease check the output at "+outFilePath+
"\n\nTips:\n1. This window will get close automatically as soon as the conversion of all files is completed."+
"\n2. To Terminate the conversion proccess press: CTRL + C"+
"\n\n++++++++++++++++++++++++++++++++++++ Thankyou +++++++++++++++++++++++++++++++++++++++++++++++")
try:
    wb = xlrd.open_workbook(inputFilePath)
except FileNotFoundError as  ex:
    logging.debug("Please make sure that Input Data is available at: InputResource\MasterCopyInputExcel.xlsx")
    logging.debug("SYSTEM MESSAGE: %s", ex)
    logging.debug("### Process Terminated ###")
    print("Please make sure that Input Data is available at: InputResource\MasterCopyInputExcel.xlsx")
    sys.exit()

sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)




#below code is to read all the tags name / Key Name
noOfColumn = rir.getNoOfColumn()
print("No of Column -----> ",noOfColumn)
#noOfColumn = sheet.ncols
noOfRows = sheet.nrows
parentArray =[]
eachCase =[]
keyTags = []
eachCase = sheet.col_values(1)  #Note:- Here you will have to put column postion stating from 0.
eachCase.pop(0)
keyTags = eachCase
#print("TAGS")

#below code is to read all value in n column

eachXMLValue =[]
#print("nrows",sheet.nrows)
#print("ncols",sheet.ncols)
startCol = 2
endCol = sheet.ncols
endRow = sheet.nrows
xmlValueList = []
for i in range(startCol,endCol):
    eachXMLValue = sheet.col_values(i)
    eachXMLValue.pop(0)
    xmlValueList.append(eachXMLValue)
#print("XMLVALUES")

# create the file structure
xmlTag = ET.Element('XML')
documentDetails = ET.SubElement(xmlTag, 'DOCUMENT_DETAILS')

#Note:- xmlValueList XML values
#Note:- Tags Values

for eachXML in xmlValueList:    #[['sagar','bbb','ccc'],[2,3,4],[3,4,5]]   ['A','B','C']
    fileName = ""
    count = 0
    sectionEL = ET.Element('')
    for eachValue in eachXML:
            eachKeyTag = ET.Element(keyTags[count])
            eachKeyTag.text = eachValue
            #if keyTags[count] == 'PAN':
            if keyTags[count] == uniqueFileName:  #Note: This Should be unique else files will be replaced
                if eachValue != '':
                    fileName = "{}.{}".format(eachValue,"xml")
                else:
                    fileName = "noPAN{}.{}".format(xmlValueList.index(eachXML),"xml")
            if keyTags[count] == 'SECTION_PART' and count == 75:
                sectionEL = ET.Element('SECTION')
                sectionEL.append(eachKeyTag)
                #print(ET.tostring(sectionEL))
                count += 1
                continue
            if keyTags[count] == 'SUB_SECTION_PART' and count == 76:
                #print(ET.tostring(sectionEL))
                sectionEL.append(eachKeyTag)
                sectionsEL = ET.Element('SECTIONS')
                sectionsEL.append(sectionEL)
                eachKeyTag = sectionsEL
            (documentDetails).append(eachKeyTag)
            count += 1
    # create a new XML file with the results
    mydata = ET.tostring(xmlTag,xml_declaration=True,encoding="unicode")
    myfile=''
    try:
        fileName = outFilePath + fileName
        myfile = open(fileName, "w")
    except FileNotFoundError as ex:
        os.mkdir("OutputResource")
        myfile = open(fileName, "w")
        print(ex)

    myfile.write(mydata.__str__())
    var = "[{}/{}]".format(xmlValueList.index(eachXML) + 1,len(xmlValueList))
    #fileName = var + fileName
    logging.debug('%s %s was created.', var,fileName)
    documentDetails.clear()
logging.debug('### Process Ends ###')

