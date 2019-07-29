# author:  Bocheng Yin Date: 06/19/2019
#automate the STOMP
#shuffle between ZEN black, imageJ, and their macros

#%%%%%%%% some must known parameters %%%%%%%%%%%%%%%%%%%%%%%%%%%%
#################must change##########################
import os
posdir = "C:\\ZEN"
f = open(''.join([posdir, '\\','currentValue.txt']))

#where to resume the sikuli stomping
HostPath= f.readline()
HostPath = HostPath.replace('\n','')
picPath = ''.join([HostPath,'\\','workdir'])
nPosFile = f.readline() # index of the position file
nPosFile = int(nPosFile)
nTile = f.readline()#number of tile positions
nTile = int(nTile)
print("read by the becallde: "+str(nTile))
currentTile = f.readline()# the tile where you want to resume STOMP
currentTile = int(currentTile)
print("read by the becallde: "+str(currentTile))
laser = f.readline()
power = f.readline()
f.close()
######################################################
nPos = nTile - currentTile
Settings.MoveMouseDelay = 1
oriImg=''
mskPath=''
logPath=''

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def wMacroException(x):
    # x is the error code. 999 for errors, 1 for no error
    pathValueFile =''.join([HostPath, '\\','macroExceptionCode.txt'])
    if (os.path.isfile(pathValueFile)):
            os.remove(pathValueFile)
    wait(0.1)
    f = open(pathValueFile,"w")
    print >> f,x
    f.close()
    wait(0.1)
   #the end of function wMacroException
def rMacroException():
    f = open(''.join([HostPath, '\\','macroExceptionCode.txt']))
    ec = f.readline()#number of tile positions
    ec = int(ec)
    f.close()
    return ec
# the end of function rMacroException()
def wTile2beSTP(picPath,mskPath):# the information will be used by imageJ
    # x is the index of the position file
    import os
    #if currentValue file exists, delete
    txtpath =''.join(['C:\ZEN', '\\','currentTile.txt']) 
    if (os.path.isfile(txtpath)):
            os.remove(txtpath)
    wait(0.1)
    f = open(txtpath,"w")
    print >> f,picPath
    print >> f,mskPath
    f.close()
    #the end of function currentTileInfo
def wCurrentInfo2z(nPosFile,currentTile):
    import time
    ts = time.time()
    print ts
    import datetime
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print st
    pathValueFile1 =''.join(['C:\ZEN', '\\','currentInfo.txt'])
    pathValueFile2 =''.join(['Z:\Bocheng', '\\','currentInfo.txt'])
    
    tileInfo = ''.join(['curretPosFile: ', str(nPosFile),' currentTile: ',str(currentTile)])
    def wtxt(pathValueFile):
        if (os.path.isfile(pathValueFile)):
                os.remove(pathValueFile)
        wait(0.3)
        f = open(pathValueFile,"w")
        print >> f,ts
        print >> f,st
        print >> f,tileInfo
        f.close()
    wtxt(pathValueFile1)
    wtxt(pathValueFile2)
    wait(0.1)

def stpInTile():
    global currentTile
    global picPath
    global oriImg
    global mskPath
    global logPath
    try:
        wCurrentInfo2z(nPosFile,currentTile)
    except:
        pass
    currentTile +=1
    oriImg = ''.join([picPath,'\\',str(currentTile),'.czi'])
    mskPath = ''.join([picPath,'\\',str(currentTile),'-msk.txt'])
    logPath = ''.join([picPath,'\\','log.txt'])
    try:
        wTile2beSTP(picPath,mskPath)
    except:
        pass        

    #+++++++++++++ start autofocus++++++++++++++++++++++++++++
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    wait(5)
    click("1537097651269.png")
    wait(2)
    find("1537100470287.png")
    
    click("1537100470287.png")
        
    #++++++++++++define some functions++++++++++++++++++++++++++
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def doNothing():
        pass
    
    
    def savePic():
        global oriImg
        #find("1537099262131.png")
        while(1):
            if exists("1547265076633.png"):
                click(Pattern("1547310449106.png").targetOffset(-12,0))
                break
            else:
                wait(1)
        wait(2)
        #sometimes because the USB connection issue,the talk between PC and miscrocope is lagging and SaveAs window won't show up. 
        # thus halt the sikulix forever if the below comment is used
        #wait("1546882700588.png",FOREVER)
        while(1):
            if exists("1546869423394.png"):
                click("1546869478218.png")
                wait(1)
                break
            else:
                while(1):
                    if exists("1547265035418.png"):
                        click(find(Pattern("1537099262131.png").targetOffset(-11,1)))
                        break
                    else:
                        wait(1)
                wait(1)
        type(Key.DELETE)
        ####it is critically important to use [\\] instead of [\] for the path
        #find("1537105389619-1.png")
        #click(Pattern("1537105389619-1.png").targetOffset(368,-1))
        #type("a", KeyModifier.CTRL)
        #type(Key.DELETE)
        paste(oriImg)
        find("1537105834742-1.png")
        click("1537105834742-1.png")
    
    
    ####___close the images in open ______#################################
    
    def closeRoughPic():
        ### the high quality image will be saved will not be close ######
        #find("1537142778142-1.png")
        #find the rough image generated by autofocus
        click(find(Pattern("1537142778142-1.png").targetOffset(-90,-149)))
        #close the rough image
        click(find(Pattern("1537142778142-1.png").targetOffset(-47,1)))
        wait(1)
        wait("1537221764818.png",3)
        click(Pattern("1537221764818.png").targetOffset(20,49))

    def closePic():
        ### close the image ######
        click(find(Pattern("1537142778142-1.png").targetOffset(-47,3)))
        wait(1)
        while(1):
            if exists(Pattern("1561387713145.png").similar(0.69)):
                click(Pattern("1561387713145.png").similar(0.69).targetOffset(20,51))
            else:
                break



    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
    # after starting aufocus, wait for its finish. and save the captured pictures.    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++        
    wait("1537103643599.png",FOREVER)
    print("now focusing fine")

    #wait for autofocus to finish
    #this is not working for empty space that autofocus cannot be acheived. 
    #wait(Pattern("1537145981504.png").similar(0.89),FOREVER)
    #this is not working for empty space that autofocus cannot be acheived.
    waitCount =0
    while (1):
        if exists(Pattern("1537145981504-1.png").similar(0.89)):
            wait(17)
           #save the high quality image after autofocus 
            savePic()
            closeRoughPic()
            break
        elif exists("1551211583652.png"):
            wait(17)
           #save the high quality image after autofocus 
            savePic()
            closeRoughPic()
            break
        else:
            wait(20)
            waitCount+=1
            if waitCount>12:
                if exists("1546994015441.png"):
                    click("1546994015441.png")
                wait(4)
                click(find(Pattern("1546994763516.png").targetOffset(40,0)))
                wait(2)
                if exists(Pattern("1546995569942.png").targetOffset(18,46)):
                    click(Pattern("1546995569942.png").targetOffset(18,46))
                elif exists(Pattern("1563076003286.png").similar(0.67)):
                    click(Pattern("1563076003286.png").similar(0.67).targetOffset(308,225))
                else:
                    pass
                wait(2)
                click(find("1546994827531.png"))
                wait(3)
                while(1):
                    if exists("1546994015441.png"):
                        wait(2)
                    else:
                        savePic()
                        break
                print("times out for autofocus!still save an image")
                break
    
    print("timecount for autofocus: "+str(waitCount))
    
    
    
    
    #Don't save and Do close the low quality image generated by autofocus 
    #####the original image must open in ZEN black. Otherwise it will trigger#######
    #####_________the runtime error 91 of VBA in the STOMP2.0 macro________#########
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++begin to open the image in imageJ+++++++++++++++++++++++++++++++++++
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def closeConsoleImageJ():
        if exists("1537107917153-1.png"):
            click("1537107917153-1.png")
            wait(0.2)
        elif exists("1541458980205-1.png"):
            click("1541458980205-1.png")
            wait(0.2)
        while(1):
            if exists("console-2.png"):
                click("console-2.png")
                type(Key.F4, KeyModifier.ALT)
            else:
                break
            if exists("1537107917153-1.png"):
                click("1537107917153-1.png")
                wait(0.2)
            elif exists("1541458980205-1.png"):
                click("1541458980205-1.png")
                wait(0.2)
    #^^^^^ THE END OF FUNCTION closeConsoleImageJ():
    def showGUIimageJ ():
        while(1):
            if exists(Pattern("1537107840635-1.png").similar(0.60)):
                break
            else:
                if exists("1537107917153-1.png"):
                    click("1537107917153-1.png")
                    wait(0.2)
     
                elif exists("1541458980205-1.png"):
                    click("1541458980205-1.png")
                    wait(0.2)
    
                #else:
                #    break
                if exists("02252019cap-1.PNG"):
                    click("02252019cap-1.PNG")
                else:
                    pass
    #^^^^^^^^^^^^^^THE END OF FUNCTION showGUIimageJ ():            
    def callOpenImageJ():
        showGUIimageJ()
        wait(2)
        setFindFailedResponse(RETRY)
        reg = find(Pattern("1537216565113-1.png").similar(0.60).targetOffset(-24,-39))
        
        reg.click()
        #close any opened image if it exists
        type("w", KeyModifier.CTRL + KeyModifier.SHIFT)
        wait(0.5)
        type("o",KeyModifier.CTRL)
        while(1):
            if not exists("1537113055863.png"):
                click("1537112896608.png")
                paste(oriImg)
                find("1537112992985.png")
                click(Pattern("1537112992985.png").targetOffset(-1,-16))
            else:
                break
        
        wait("1537113055863.png")
        find("1537113072694.png")
        click(Pattern("1537113072694.png").targetOffset(-31,0))
        setFindFailedResponse(ABORT)
    # the end of the function callOpenImageJ()  
    callOpenImageJ()
    ##+++++++ try to open the macro in imagej+++++++ 
    #define the function for processing the image in imageJ
    def pickMacro(n):
        #n is the position of the macro under the "Macros" tab
        while(1):
            if exists(Pattern("1537216628985.png").similar(0.81)):
                click(Pattern("1537216628985.png").similar(0.81))
                break
            else:
                wait(1)
        wait(0.2)
        type(Key.DOWN)
        wait(0.2)
        type(Key.RIGHT)
        wait(0.2)
        for i in range(n):
            type(Key.DOWN)
            wait(0.2)
        type(Key.ENTER)
        wait(1)
        while(1):
            if exists ("1563917326976.png"):
                click(Pattern("1563917326976.png").targetOffset(-7,40))
            else:
                break
    #the end of the function, pickMacro(n)
    def imageJPro():
        wait(2)#wait for the image to be open
        while(1):
            if exists(Pattern("1547085783372.png").similar(0.75)):
                break
            else:
                wait(2)
        #put the open-macro steps into a while loop in case the zen software freezes at this step and 
        # arrest sikulix
        rp=0
        #only retry 20 times
        while(rp<20):
            if exists(Pattern("1547085783372.png").similar(0.75)):
                pickMacro(6)
                wait(5)
                #deal with ROI manager no selection problem
                while(1):
                    if exists ("1561940753732.png"):
                        click(Pattern("1561940753732.png").targetOffset(-1,45))
                        wait(0.2)
                        #then clean the windows opened in imageJ, i.e.cleanWindows
                        pickMacro(7)
                        #generate an empty mask, use the macro "EMTmask"
                        pickMacro(8)
                    else:
                        break
   
                #deal with macro exceptions
                if exists("1561233312354.png"):
                    click("1561233312354.png")
                    type(Key.F4, KeyModifier.ALT)
                    wait(0.5)
                    #999 for errors, 1 for no error
                    wMacroException(999)
                    if exists("1561233556516.png"):
                        click("1561233556516.png")
                        type(Key.F4, KeyModifier.ALT)
                        wait(0.5)
                    break
                else:
                    #999 for errors, 1 for no error
                    wMacroException(1)
                #end of the dealing with macro exception
                
                #deal with ROI manager "more than one item must be selected, or none"
                if exists ("1561556796439.png"):
                    click(Pattern("1561556796439.png").targetOffset(-4,41))
                    
                while(1):
                    if exists("1557966532054.png"):
                        click(Pattern("1557966532054-1.png").targetOffset(312,222))
                    else:
                        break
                rp=rp+1
                    
            else:
                break
        
        if exists("1546965871430.png"):
            click(Pattern("1546965871430.png").targetOffset(-1,45))
        #^^^^the end of function imageJPro() functions^^^^^^^^
### ++++++++++done !+++++++++++++++++++++++
    ### ++++++++++done !+++++++++++++++++++++++
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #+++++++ work in STOMP 2.0 macro++++++
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # the path of mask textImage file
    def isTPon():
        while(1):
            if exists("1560370331426.png"):
                break
            else:
                click(Pattern("1560370773059.png").targetOffset(187,0))
                click(Pattern("1560370773059.png").targetOffset(145,20))
                wait(4)
    # the end of function isTPon()
 
    def stpPreP():
        wait(4)
        setFindFailedResponse(RETRY)
        isTPon()
        reg = find(Pattern("1537137522045.png").similar(0.60))
        click(reg)
        wait(2)
        click(reg.find(Pattern("1537139094604.png").targetOffset(-62,25)))
        wait(1)
        #type("a", KeyModifier.CTRL)
        #type(Key. DELETE)
        paste(mskPath)
        wait(2)
        # enter the path of log file
        click(reg.find(Pattern("1537139134117.png").targetOffset(-38,30)))
        wait(1)
        #type("a", KeyModifier.CTRL)
        #type(Key. DELETE)
        paste(logPath)
        wait(2)
        # set up the photobleach parameters
        
        #if not reg.exists(Pattern("1537137909555.png").exact()):
                #click(reg.find(Pattern("1537139228797.png").targetOffset(38,-4)))
                #type("720")
        click(reg.find(Pattern("1537139228797.png").similar(0.72).targetOffset(38,-4)))
        type(laser)
        type(Key.ENTER)
        wait(2)
        click(reg.find(Pattern("1537139228797.png").similar(0.72).targetOffset(78,37)))
        type(power)
        wait(1)
        type(Key.ENTER)
        wait(2)
        setFindFailedResponse(ABORT)
        
    # the end of function, stpPreP()^^^^^^^^^^^^#
    
    # ready for STOMP
    #imageJPro()
    #stpPreP()
    def clickSTOMP():
        click("1537141286377.png")
        wait(2)
        while(1):
            if exists(Pattern("1537141143786.png").similar(0.60)):
                click(Pattern("1537141143786.png").similar(0.60).targetOffset(4,50))
            else:
                break
        wait(1)
        #sometime the macro error window will hide. pop it up
        def popMacroErrorWin():
            if exists("1559137050851-2.png"):
                if exists(Pattern("1560269797607.png").similar(0.68)):
                    pass
                else:
                    click("1559137050851-2.png")
         
         #the end of function popMacroErrorWin()
        popMacroErrorWin()                    
        #deal with runtime error9       
        while(1):
            if exists("1558982066789.png"):
                click(Pattern("1558982066789.png").targetOffset(-55,95)) # after click the button "end", the zen macro will close
                openZenMacro()
                closeConsoleImageJ()
                callOpenImageJ()
                imageJPro()
                stpPreP()
                click("1537141286377.png")
                wait(2)
                while(1):
                    if exists(Pattern("1537141143786.png").similar(0.60)):
                        click(Pattern("1537141143786.png").similar(0.60).targetOffset(4,50))
                    else:
                        break
                wait(1)
                popMacroErrorWin()
            else:         
                break
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        #deal with file name or path is not correct    
        while(1):
            if exists("1560267387485.png"):
                click(Pattern("1560267387485.png").targetOffset(81,78)) # after click the button "end", the zen macro will close
                wait(0.5)
                if exists(Pattern("1560260584207.png").similar(0.66)):
                    click(Pattern("1560260584207.png").similar(0.66).targetOffset(108,52))
                wait(0.5)
                if exists(Pattern("1560260743327.png").similar(0.69)):
                    click(Pattern("1560260743327.png").similar(0.69).targetOffset(-53,92))
                wait(0.5)
                #now the stomp macro should be also closed
                openZenMacro()
                #problem with the console window from imagej
                #the console will be closed in callOpenImageJ()
                closeConsoleImageJ()
                callOpenImageJ()
                imageJPro()
                stpPreP()
                click("1537141286377.png")
                wait(2)
                while(1):
                    if exists(Pattern("1537141143786.png").similar(0.60)):
                        click(Pattern("1537141143786.png").similar(0.60).targetOffset(4,50))
                    else:
                        break
                wait(1)
                popMacroErrorWin()
            else:         
                break
     # the end of function clickSTOMP()
    #clickSTOMP()
    ######confirm to do STOMP#########
    #sometime the STOMP macro will freeze. no response after clicking the "STOMP" button
    #

       

    #++++++++++++++++++++++++++++++++++++++
    #+++++++wait for STOMP to finish++++++++
    def finishSTP():
        setFindFailedResponse(RETRY)
        reg = find(Pattern("1539785202395.png").similar(0.60))
        if reg:
            setFindFailedResponse(ABORT)
            print("image found!")
            pass
    
        
        #reg.wait("1537209699809.png",FOREVER)
        reg.wait(Pattern("1537211285061.png").similar(0.90),FOREVER)
        reg.wait("1537211960407.png",FOREVER)
        wait(5)
        #close the original image in ZEN black at the end of STOMP
        closePic()
        print(''.join(['stomp ',str(currentTile),' finished']))
    #the end of function finishSTP()
    imageJPro()
    #read the macroExceptionCode
    macroE = rMacroException()
    if (macroE==999):
        pass
    else:
        stpPreP()
        clickSTOMP()
        finishSTP()
    
    #%%%%%%%%%%%%%%%%%%%%%%%%% the end of the function stpInTile()%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def openZenMacro():
    while(1):
        if not exists("1558982625101.png"):
            if not exists(Pattern("1558982393940.png").similar(0.80)):
                click(Location(1160, 20))
                wait(0.2)
            click(Pattern("1558982393940.png").similar(0.80))
            for i in range(2):
                type(Key.DOWN)
                wait(0.2)
            type(Key.ENTER)
            wait(0.2)
            
            t4= find("1542140074683.png")
            dragDrop(t4,Region(1936,226,10,10))
        else:
            break
## the end of function openZenMacro() ^^^^^^^^^^^^
#%%%%% begin to loop through the tiles %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def clickPos1():
    click(Pattern("1558133984152.png").targetOffset(-137,-10))
    #click move to 
    click(Pattern("1558133984152.png").targetOffset(-184,102))
def clickPos2():
    click(Pattern("1558134555833.png").targetOffset(-127,13))
    #click move to 
    click(Pattern("1558133984152.png").targetOffset(-184,102))    
def clickPos3():
    click(Pattern("1558134555833.png").targetOffset(-155,31))
    #click move to 
    click(Pattern("1558133984152.png").similar(0.69).targetOffset(-184,102))
def clickPos4():
    click(Pattern("1558134555833.png").targetOffset(-125,51))
    #click move to 
    click(Pattern("1558133984152.png").targetOffset(-184,102))    

#+++++++++++++++test movedown the position l++++++++++++++++++++++++++++
def clickForfirst4Pos(nTile):
    p = nTile
    #find("1558133984152.png")
    #++++++++++choose position 1+++++++++++++++++++++

    clickPos1()
    stpInTile()
    p=p-1
    
        #++++++++++choose position 2+++++++++++++++++++++
    if p>0: 
        clickPos2()
        stpInTile()
        p=p-1
    else:
        doNothing()
    
    #++++++++++choose position 3+++++++++++++++++++++
    if p>0:   
        clickPos3()
        stpInTile()
        p=p-1
    else:
        doNothing()
    #++++++++++choose position 4+++++++++++++++++++++
    if p>0:    
        clickPos4()
        stpInTile()
        p=p-1
    else:
        doNothing()
def clickForPosMT4(x):
    #x is the number of the leftover positions after position 4
    for i in range(x):
        #move the list down by one
        click(Pattern("1558134555833.png").similar(0.65).targetOffset(213,53))
        #select the new position
        click(Pattern("1558133984152.png").similar(0.65).targetOffset(-129,47))
        #click move to 
        click(Pattern("1558133984152.png").similar(0.65).targetOffset(-184,102))
        if (currentTile < nTile):
            stpInTile()
        else:
            break
# the end of function of clickForPosMT4()
if (nTile == nPos):
    if nTile < 4 or nTile ==4:
        clickForfirst4Pos(nTile)
    #+++++++++++after position 4+++++++++
    if nTile>4:
        #for the first 4 position
        clickForfirst4Pos(nTile)
        # from the 5th position
        clickForPosMT4(nTile-4)
else: #nPos is smaller than nTile
    #it resume the work from a new position (usually larger than 4)
    if currentTile ==1:
        clickPos2()
        stpInTile()
        clickPos3()
        stpInTile()
        clickPos4()
        stpInTile()
    if currentTile ==2:
        clickPos3()
        stpInTile()
        clickPos4()
        stpInTile()
    if currentTile ==3:
        clickPos4()
        stpInTile()
    if currentTile >3:
        clickForPosMT4(nPos)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


