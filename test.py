import urllib, cStringIO

img=None
URLlink="http://slides.mskcc.org/slides/mirsadrl@mskcc.org/19;l;432372/getLabelFileBMP"
try:
    
    img = Image.open(cStringIO.StringIO(urllib.urlopen(URLlink).read()))
except:
    pass
print img
