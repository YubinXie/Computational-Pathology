import openslide
import os
#import matplotlib.pyplot as plt

#folder="../../../data/fuchs/projects/prostate/aeDict/"
#files = [file for file in os.listdir(folder) if "svs" in file]
#folder=""
#svs_path = "../Main/CMU-1-Small-Region.svs.tiff"
#"http://slides.mskcc.org/thumbnail/xiey@mskcc.org/aperio;" +SampleID + "/jpg/null/1280/1280"

def getdimension(svs):

	width,height = svs.dimensions
	print width,height
	mpp_x = float(svs.properties[openslide.PROPERTY_NAME_MPP_X])
	mpp_y = float(svs.properties[openslide.PROPERTY_NAME_MPP_Y])
	resolution = (mpp_x + mpp_y)/2
	print "mmp_x = ",mpp_x,"mmp_y = ",mpp_y
'''
for svs_path in files:
	print svs_path
	svs = openslide.OpenSlide(folder+svs_path)
	getdimension(svs)
'''



def getthumbnail():
	folder = "../../../data/fuchs/projects/prostate/yubin/"
	IDFile = "Selected.txt"
	with open (IDFile,"r") as OpenInput, open ("Output","w") as OpenOutput:
		for ID in OpenInput:
			ID = ID.strip("\n")
			print folder+ID
			svs = openslide.OpenSlide(folder+ID)
			mpp_x = float(svs.properties[openslide.PROPERTY_NAME_MPP_X])
			mpp_y = float(svs.properties[openslide.PROPERTY_NAME_MPP_Y])
			width,height = svs.dimensions
			image=svs.get_thumbnail((width/50.0,height/50.0))
			image.save("../data/input/"+str(ID.replace("svs",""))+"jpeg","JPEG")
			OpenOutput.writelines("%s\t%s\t%s\t%s\t%s\n" % (ID, mpp_x, mpp_y, width, height))
getthumbnail()
