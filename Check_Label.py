from scipy import misc
import sys
import PatchedPIL
from PatchedPIL import Image, ImageFile, BmpImagePlugin, ImagePalette


InputFolder = "Label/"
FileName= "l;432923.svs.bmp"
def main(InputFolder,FileName):
    Color ={}
    original_img=[]
    try:
        original_img = Image.open(InputFolder+FileName)
    except:
    	pass
    if original_img==[]:
    	sys.exit("no such file")
    img=original_img.load()
    w,l = original_img.size
    print w,l
    for i in range(w):
        for j in range(l):
            if (img[i,j]) != 0:
                print i,j
            if str(img[i,j]) not in Color:
                Color[str(img[i,j])]=1
            if str(img[i,j]) in Color:
                Color[str(img[i,j])]+=1

    print  FileName, Color



if __name__ == '__main__':
  main(InputFolder,FileName)
