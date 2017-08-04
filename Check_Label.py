from scipy import misc
import sys




def main():
    Color ={}
    original_img=[]
    FileName= "k;427076.svs.bmp"
    try:
        original_img = misc.imread(FileName)
    except:
    	print "no such file", FileName
    	pass
    if original_img==[]:
    	sys.exit("no such file")
    w,l,h = original_img.shape
    print w,l,h
    print original_img[1,1,:]
    for i in range(w):
        for j in range(l):
            if original_img[i,j,0] != 255 or original_img[i,j,1] != 255 or original_img[i,j,2] != 255:
                if str(original_img[i,j,:]) not in Color:
                    Color[str(original_img[i,j,:])]=1
    print  line.strip("\n"), Color



if __name__ == '__main__':
  main()
