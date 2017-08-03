from scipy import misc

with open ("Sample_List.txt") as OpenSampleList:
    for line in OpenSampleList:
    	Color={}
    	original_img=[]
        if "k" in line or "l" in line:
            FileName= "../RawInput/Label/" + line.strip("\n") + ".bmp"
            try:
            	original_img = misc.imread(FileName)
            except:
            	print "no such file", FileName
            	pass
            if original_img==[]:
            	continue
            w,l,h = original_img.shape
           
            
            for i in range(w):
                for j in range(l):
                    if original_img[i,j,0] != 255 or original_img[i,j,1] != 255 or original_img[i,j,2] != 255:
                        if str(original_img[i,j,:]) not in Color:
                            Color[str(original_img[i,j,:])]=1
            print  line.strip("\n"), Color
