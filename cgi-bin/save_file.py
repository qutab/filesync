import os, cgi
fs = cgi.FieldStorage()
fileitem = fs['userfile']

# Test if the file was uploaded
if fileitem.filename:
   fn = os.path.basename(fileitem.filename)
   open('./' + fn, 'wb').write(fileitem.file.read())
   message = 'The file "' + fn + '" was uploaded successfully'
else:
   message = 'No file was uploaded'
