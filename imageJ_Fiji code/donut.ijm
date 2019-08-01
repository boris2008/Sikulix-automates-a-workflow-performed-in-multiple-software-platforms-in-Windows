macro "toxoDonut"{
	//{
//only 488 channel is imaged here
//while (nImages>0) { 
//	selectImage(nImages); 
//	close(); 
//} 

dir= getDirectory("image");//get the directory of current active image
title=getTitle;// here name includes the extension
Index = indexOf(title, ".czi"); 
name1 = substring(title, 0, Index); //exclude extension
run("Duplicate...", "duplicate channels=1 frames=1");
//extrac the zeiss file ".czi" with airyscan mode ON. 
//only 488 is imaged here.
NewName = dir+name1+"-1"+".tif";//the name of the extracted image, directory+name+extension
NewTitle = name1+"-1"+".tif";//only the name+extension
saveAs("Tiff", NewName);
selectWindow(title);//select the .czi file
close();//close the .czi file
//the end of the extract of aryscan image}

selectWindow(NewTitle);//select the extract image
run("8-bit");
//setAutoThreshold("Default dark");
//setAutoThreshold("IsoData dark");
//setAutoThreshold("IJ_IsoData dark");
//setAutoThreshold("MaxEntropy dark");
//setAutoThreshold("Yen dark");
//setAutoThreshold("Intermodes dark");
//setAutoThreshold("Huang dark");
//setAutoThreshold("IsoData dark");
//setAutoThreshold("MinError dark");
//setAutoThreshold("Otsu dark");
//setAutoThreshold("Mean dark");
//setAutoThreshold("Minimum dark");
//setAutoThreshold("Triangle dark");
//setAutoThreshold("Default dark");
//setAutoThreshold("Shanbhag dark");

////////////////////////////////////
//try all the threshold methods
////////////////////////////////////

run("Auto Threshold", "method=[Try all] ignore_black ignore_white show");
close();
logString =getInfo("log");
lines=split(logString, "\n"); 
thrArray= newArray(7);
//different autothreshold methods
thrArray[0]=lines[0];//default
thrArray[1]=lines[4];//isoData
thrArray[2]=lines[6];//maxentropy
thrArray[3]=lines[10];//moments
thrArray[4]=lines[11];//otsu
thrArray[5]=lines[13];//Renyientropy
thrArray[6]=lines[16];//yen
print("the chosen ones");
Array.print(thrArray);
thrValArray = newArray(7);
for(i=0; i<thrArray.length; i++) {
	val = split(thrArray[i],": ");
	val = parseInt(val[1]);
	thrValArray[i]=val;
	}
print("extract the value");
Array.print(thrValArray);
//remove non-numeric value from the list
thrValArray=Array.deleteValue(thrValArray, NaN);

Array.getStatistics(thrValArray, min, max, mean, std);
  print("stats");
  print("   min: "+min);
  print("   max: "+max);
  print("   mean: "+mean);
  print("   std dev: "+std);

//get the geometricMean
  function GeometricMean(array1) {
  	x = array1[0];
  	n=array1.length;
  	for(i=1; i<n; i++) {
  		x=x*array1[i];
  		}
  	x=pow(x,1/n);
      return x;
  }
  geomean = GeometricMean(thrValArray);
  print("	geometric mean:	"+geomean);

  //sort the array from the lowest to highest
Array.sort(thrValArray);
//get the median
median =thrValArray[3];
 print("	median: "+median);
Array.print(thrValArray);

run("Threshold..."); 
//choose one threshold
// we can choose min max mean geomean median
//setThreshold((geomean+median)/2,255);
//setThreshold(median,255);
//setThreshold(geomean,255);
setThreshold((median+thrValArray[4])/2,255);
getThreshold(minInUse,maxInUse);
print("the used threshold is: "+minInUse+ " & "+maxInUse);
selectWindow("Threshold");
run("Close");

//waitForUser("set the threshold and press OK, or cancel to exit macro"); 
//run("Close");
//run("Make Binary", "thresholded remaining black");
run("Convert to Mask");
run("Fill Holes");
run("Watershed");

// to remove the small pixel dots process->noise-> despeckle OR
//it looks like the median filter works better for me. process-> filters-> median
run("Median...", "radius=1");
Name2 = dir+name1+"-oriBi"+".tif";//the name of the extracted image, directory+name+extension
Title2 = name1+"-oriBi"+".tif";//only the name+extension
saveAs("Tiff", Name2);
//choose the particle size
run("Analyze Particles...", "size=3-150.00 circularity=0.1-1 show=Masks display add");
//the mask window
maskWindowTitle = "Mask of "+Title2;
selectWindow(maskWindowTitle);

run("Close-");
//////remove the frame of the image
getDimensions(width, height, channels, slices, frames);
xmax=width-1;
ymax=height-1;
setColor(0);
drawLine(0,0,0,ymax);
drawLine(0,0,xmax,0);
drawLine(xmax,0,xmax,ymax);
drawLine(0,ymax,xmax,ymax);
//////
run("Convert to Mask");
run("Fill Holes");
Name3 = dir+name1+"-binary"+".tif";//the name of the extracted image, directory+name+extension
Title3 = name1+"-binary"+".tif";//only the name+extension
saveAs("Tiff", Name3);

selectWindow(Title3);
//2 pixels = 1.3 um for 25x lens 512x512 image
nOfDilate =2; // numbers of dilate
for (i=0; i<nOfDilate; i++) {
   run("Dilate");
   }

Name4 = dir+name1+"-dilate"+".tif";//the name of the extracted image, directory+name+extension
Title4 = name1+"-dilate"+".tif";//only the name+extension
saveAs("Tiff", Name4);
selectWindow(Title4);
open(Name3);
imageCalculator("XOR create", Title4, Title3);
//remove small speckle
//run("Median...", "radius=2");
Title5= "Result of "+name1+"-dilate"+".tif";
selectWindow(Title5);
MaskName = dir+name1+"-msk"+".tif";//the mask image directory+name+extension
TxtName = dir+name1+"-msk"+".txt";//the txt image directory+name+extension
saveAs("Tiff", MaskName);
saveAs("Text Image", TxtName);


// Closes all image windows.
close("*");


if(isOpen("Log")){
	selectWindow("Log");
	run("Close");
	}
if(isOpen("Results")){
selectWindow("Results");
run("Close");
}
if(isOpen("ROI Manager")){
selectWindow("ROI Manager");
run("Close");
}

run("Close All");
	}//extract the airy scan image from .czi file

macro "cleanWindows" {
      	if(isOpen("ROI Manager")){
			selectWindow("ROI Manager");
			run("Close");
		}
		close("*");//close all active image
		if(isOpen("Log")){
			selectWindow("Log");
			run("Close");
		}
		if (isOpen("Results")){
			selectWindow("Results");
			run("Close");
		}
  }
  macro "EMTmask" {
		s1= File.openAsString("C:/ZEN/currentTile.txt");
		lines=split(s1,"\n");
		print(lines.length);
		print(lines[0]);//the directory to store the image
		print(lines[1]);// the path of the empty mask file
		close("*")
		newImage("fakemask", "8-bit black", 512, 512, 1);	
  		saveAs("Text Image", lines[1]);
  		close("*")
  		      	if(isOpen("ROI Manager")){
			selectWindow("ROI Manager");
			run("Close");
		}
		close("*");//close all active image
		if(isOpen("Log")){
			selectWindow("Log");
			run("Close");
		}
		if (isOpen("Results")){
			selectWindow("Results");
			run("Close");
		}
		if(isOpen("ROI Manager")){
			selectWindow("ROI Manager");
			run("Close");
		}
  }
