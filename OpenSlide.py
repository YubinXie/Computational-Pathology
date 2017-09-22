import openslide
import os
import matplotlib.pyplot as plt

folder="../../../data/fuchs/projects/prostate/aeDict/"
files = [file for file in os.listdir(folder) if "svs" in file]
print files


#svs_path = "../Main/CMU-1-Small-Region.svs.tiff"
#"http://slides.mskcc.org/thumbnail/xiey@mskcc.org/aperio;" +SampleID + "/jpg/null/1280/1280"

def getdimension(svs):
	width,height = svs.dimensions
	print width,height
	mpp_x = float(svs.properties[openslide.PROPERTY_NAME_MPP_X])
	mpp_y = float(svs.properties[openslide.PROPERTY_NAME_MPP_Y])
	resolution = (mpp_x + mpp_y)/2
	print "mmp_x = ",mpp_x,"mmp_y = ",mpp_y

for svs_path in files:
	print svs_path
	svs = openslide.OpenSlide(folder+svs_path)
	getdimension(svs)


	#print "mmp_x = ",mpp_x,"mmp_y = ",mpp_y,resolution
	#print 'The slide\'s objective power is', svs.properties[openslide.PROPERTY_NAME_OBJECTIVE_POWER]
#a=svs.get_thumbnail((100,100))
#plt.imshow(a)
#plt.show()
#svs.close()
