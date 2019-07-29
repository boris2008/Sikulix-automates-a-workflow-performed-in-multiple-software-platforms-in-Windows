###                #Input parameters               ##### author:  Bocheng Yin Date: 06/19/2019
####################################################
currentPosFile = 0 #default is 0 #which position file you want to resume your work, i.e. 3 is tilePos-4
currentTile = 3#default is 0 # which position you want to resume in the list of the position file chosen above, count from 0
#%%%%%%%assume we have 4 filePosition here%%%%%%
numPosFile = 5# numbers of .pos files
##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
numTileF1 = 120 # numbers of tiles in #1 position file
currentTilein1 = 0 # no change
listF = []
listTile =[]
listF.append(numTileF1)
listTile.append(currentTilein1)
##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
numTileF2= 120 # the #2 positon file
currentTilein2 = 0 # no change
listF.append(numTileF2)
listTile.append(currentTilein2)
##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
numTileF3= 120 # the #3 positon file
currentTilein3 = 0 # no change
listF.append(numTileF3)
listTile.append(currentTilein3)
##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
numTileF4= 87 #4 positon file
currentTilein4 = 0 # no change
listF.append(numTileF4)
listTile.append(currentTilein4)
##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
numTileF5= 0 #5 positon file
currentTilein5 = 0 # no change
listF.append(numTileF5)
listTile.append(currentTilein5)
##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
hostPath = "D:\\Bocheng\\07-25-2019_stp_toxo_ifnr"
laser = "720"
power = "3"  ######P/I/D =3/1/1
posdir = "C:\\ZEN"
#script2beCall = "./stp_beCalledTest.sikuli"
script2beCall = "./stp_becalled_oneChannel.sikuli"
#######################################################
###           END OF INPUT PARAMETERS              ####
#######################################################
# author:  Bocheng Yin Date: 05/17/2019
#cannot load too many position per time to zen black
# different position files
#cannot load too many position per time to zen black
# otherwise, it will numb the software
#now each time only load 120 positions

#save the input parameters as a text file
#pass the parameters to the beCalled script
for i in listF:
    print(i)
for i in listTile:
    print(i)

#replace currentTiles in the list
listTile[currentPosFile]= currentTile
print("resume the work, how the list looks like now?")
for i in listTile:
    print(i)
print("the one has been changed")
print(listTile[currentPosFile])
def exportValue(x,listF,listTile):
    # x is the index of the position file
    import os
    #if currentValue file exists, delete
    pathValueFile =''.join([posdir, '\\','currentValue.txt'])
    if (os.path.isfile(pathValueFile)):
            os.remove(pathValueFile)
    wait(0.1)
    f = open(pathValueFile,"w")
    print >> f,hostPath
    print >> f,str(x)
    print >> f,str(listF[x])
    print >> f,str(listTile[x])
    print >> f,str(laser)
    print >> f,str(power)
    f.close()


#####################################################
def sendMessage(title,message):
    while(1):
        if not exists("1552253461334-3.png"):
            click(find("1552253486910-3.png"))
            wait(1)
        else:
            break
    click("1552253551038-3.png")
    wait(1)
    def writeMessage():
        setFindFailedResponse(RETRY)
        reg = find("1559300826156-1.png")
        if reg:
            setFindFailedResponse(ABORT)
            print("Gmail Dialogue window found!")
            #pass
        setFindFailedResponse(RETRY)
        toReg = reg.find("1552254458079-3.png")
        if toReg:
            setFindFailedResponse(ABORT)
            print("reipient box found!")
            #pass
        click(toReg.offset(5,50))
        receiptE= "yincool2008@gmail.com"
        paste(receiptE)
        setFindFailedResponse(RETRY)
        subjectReg = reg.find("1552253952296-3.png")
        if subjectReg:
            setFindFailedResponse(ABORT)
            print("subject box found!")
            #pass
        click(subjectReg.offset(43,0))
        titleE= title
        paste(titleE)
        click(subjectReg.offset(157,37))
        contentE= message
        paste(contentE)
        setFindFailedResponse(RETRY)
        sendReg = find("1552254204200-3.png")
        if sendReg:
            setFindFailedResponse(ABORT)
            print("send button found!")
            #pass
        click(sendReg)
        wait(4)
       #the end of the function, write message. 
    writeMessage()
    while(1):
        if exists ("1559302052182.png"):
            #click()
            writeMessage()
        else:
            break
    #minimize the webpage
    while(1):
        if exists("1552253461334-3.png"):
            click(find("1552253486910-3.png"))
            wait(1)
        else:
            break

def loadPosFile(posdir, n):
    #n starts from 0
    wait(0.5)
    posFile = ''.join([posdir,'\\','tilePos-',str(n+1),'.pos'])
    #remove all the current positions
    click(Pattern("1557922358162.png").targetOffset(152,160))
    wait(0.5)
    if exists("1557922477004.png"):
        click(Pattern("1557922477004.png").targetOffset(-29,38))
    #load new posFile
    while (1):
        if not exists("1557922697301.png"):
            click(Pattern("1558142138135.png").similar(0.72).targetOffset(147,93))
            wait(0.5)
        else:
            while(1):
                if not exists("1557923810995.png"):
                    #click(Pattern("1557922697301.png").similar(0.67).targetOffset(-89,192))
                    click(Pattern("1564111440321.png").targetOffset(22,-17))
                    type(posFile)
                    type(Key.ENTER)
                    wait(5)
                else:
                    break
            break
#the end of the loadPosFile() function
def moveD2cPos(currentTile):
    for i in range(currentTile-4):
        #move the list down by one
        click(Pattern("1558134555833.png").similar(0.65).targetOffset(213,53))
        wait(0.2)
## the end of currentTile function
def empty(src):#empty a folder
    for c in os.listdir(src):
        full_path = os.path.join(src, c)
        if os.path.isfile(full_path):
            os.remove(full_path)
## the end of empty() function

def wrapFile2folder(hostPath,n):
    # n starts from 0
    import os
    import shutil
    src = ''.join([hostPath,'\\workdir'])
    dst = ''.join([hostPath,'\\',str(n+1)])
    #The destination directory, named by dst, must not already exist
    shutil.copytree(src, dst, symlinks=False, ignore=None)
    wait(8)
    #shutil.rmtree(src,ignore_errors=True)
    #wait(5)
    #if not os.path.exists(src):
    #    os.mkdir(src)# it is easy to cause permission access is denied.
    empty(src)
    wait(5)
#the end of the wrapFile2folder() function

j = currentPosFile
pwd= ''.join([hostPath,'\\workdir'])
if not os.path.exists(pwd):
    os.mkdir(pwd)
for i in range(numPosFile-currentPosFile):
    loadPosFile(posdir, j)
    moveD2cPos(listTile[j])
    exportValue(j,listF,listTile)
    exitValue = runScript(script2beCall)
    #exitValue = runScript("./testClick.sikuli")
    titleF= ''.join(["sikuli crashes!!!!", "is ",str(j+1)])
    messageF=''.join(["sikuli crashes!!!!", "is ",str(j+1)])
    titleS =''.join(['congradulation!', '#',str(j+1),'finishes'])
    messageS= ''.join(['congradulation!', '#',str(j+1),'finishes'])
        
    if exitValue == 1:
        sendMessage(titleF,messageF)    
        print "there was an exception"
        exit(1)
        
    else:
        sendMessage(titleS,messageS)    
        print "ran with success"
        wrapFile2folder(hostPath,j)
        #exit(exitValue)
    j=j+1
# the end of the for loop