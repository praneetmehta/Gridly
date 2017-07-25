import sys
from PIL import Image
from os import walk, path, makedirs
from mutagen import File
import imghdr
from random import shuffle
import math
import shutil

#size of each individual thumbnail
size = int(sys.argv[1])

#filelist that hold the mp3filepaths
filelist = []
filepath = raw_input('Enter the directory you want to use(abs path): ')

#read the directory and populate the filelist
for dirpath, dirname, files in walk(filepath):
	for file in files:
		if path.splitext(file)[1] == '.mp3':
			filelist.append([path.join(dirpath, file), path.splitext(file)[0]])

#temporary filelist holder for images temp folder
tempfilelist = []

thumbsize = size, size
temppath = 'temp'

#create the temporary directory in the folder to hold the extracted thumbnails
if not path.exists(temppath):
	makedirs(temppath)

#extract the albumart from the mp3 files and reduce the size to thumbnail size
for file in filelist:
	try:
		im_file = File(file[0])
		artwork = im_file.tags['APIC:'].data
		with open(path.join('temp', file[1])+'.jpg', 'wb') as img:
			img.write(artwork)
			tempfilelist.append(path.join('temp', file[1]+'.jpg'))
	except:
		pass
for file in tempfilelist:
	im = Image.open(file)
	im.thumbnail(thumbsize)
	im.save(file, imghdr.what(file))

#shuffle the list for random order of imagegrid
shuffle(tempfilelist)
sqroot = int(math.floor(math.sqrt(len(tempfilelist))))
newquant = int(math.pow(sqroot, 2))

#blank new image to hold the grid 
newimg = Image.new('RGB', (sqroot*size,sqroot*size))

#open all the thumnail images
images = map(Image.open, tempfilelist)

width = size
height = size

#offset variables
x_offset = 0
y_offset = 0
counter = 0

#paste the thumbnail images on the newimage as per the offset
for im in images:
  newimg.paste(im, (x_offset,y_offset))
  x_offset += width
  counter+=1
  if(counter == sqroot):
  	y_offset += height
  	counter = 0
  	x_offset = 0

#remove the temporary folder
shutil.rmtree('temp')
#save the newimage
newimg.save(raw_input('Enter the name for final image: '))