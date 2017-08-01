import urllib, cStringIO

URLlink="www.apple.com"
try:
    files = cStringIO.StringIO(urllib.urlopen(URLlink).read())
except:
    pass
print 1
