#!/bin/python

from scipy import misc, ndimage, spatial
import scipy
import pylab as pl
import matplotlib.pyplot as plt
import numpy
import math as m
import pywt
import sys
import os

filename = sys.argv[1]

if (len(filename) == 0): 
	print "Usage: <image file name>"
	exit()

if (not os.path.exists(filename)):
	print "The file ", filename, " doesn't exist"
	exit()

imgrgb = misc.imread(filename)

# Convert a RGB image into a gray-scale image
imggray = numpy.sum(imgrgb.astype(numpy.int), axis=2)/3
szimg = imggray.shape

N = max(szimg)
imgnewsz = misc.imresize(imggray, (N,N))

cm_img = ndimage.measurements.center_of_mass(imgnewsz)
print cm_img

euc = spatial.distance.euclidean

d = 0

for x in range(0, N):
	for y in range(0, N):
		if (imgnewsz[x][y] < 0xFF):
			d = max(euc([x,y], cm_img), d)
print d

size = int(m.ceil(d))+1

varrad = float(d)/float(N)
varang = 2.*m.pi/float(N)

var_g = scipy.zeros((size,360), int)

for i in range(0,size):
	for j in range(0,360):
		var_g[i][j] = 0xFF

radius = 0

for i in range(0,size):
	radius = float(i)
	for j in range(0,360):
		angle = m.radians(j)
		x = int(cm_img[0] + radius*m.cos(angle))
		y = int(cm_img[1] + radius*m.sin(angle))

		if (x >= 0 and x < N and y >= 0 and y < N and radius < size):
			#print (int(radius), int(m.degrees(angle)), x, y)
			var_g[int(radius)][int(m.degrees(angle))] = imgnewsz[x][y]


var_G_fft = numpy.fft.fft(var_g, 180)/size # transform on g along the axis of polar angle
var_G = scipy.zeros((size,180), float) # transform on g along the axis of polar angle

for r in range(0, size):
	for t in range(0, 180):
		val = abs(var_G_fft[r][t].real)
		var_G[r][t] = val

var_G_swap = numpy.swapaxes(var_G, 0, 1)
var_G_final_aprox = scipy.zeros((size/2,180), float) # transform on g along the axis of polar angle
var_G_final_detail = scipy.zeros((size/2,180), float) # transform on g along the axis of polar angle
var_G_plot = scipy.zeros((size/2,180), float) # transform on g along the axis of polar angle

val_max = 0
for t in range(0, 180):
	(aprox,detail) = pywt.dwt(var_G_swap[t], 'db4')
	for r in range(0, size/2): 
		var_G_final_aprox[r][t] = aprox[r]
		var_G_final_detail[r][t] = detail[r]
		var_G_plot[r][t] = int(aprox[r])
		val_max = max(val_max, aprox[r])

var_G_plot = ((var_G_plot/val_max)*255)

f = open('db/' + filename.replace('/','_') + '_aprox.txt', 'w+')
f.write(str(size/2) + ' ' + str(180) + '\n')
for r in range(0, size/2): 
	for t in range(0, 180):
		f.write(str(var_G_final_aprox[r][t]) + ' ')
	f.write('\n')
f.close()

f = open('db/' + filename.replace('/','_') + '_detail.txt', 'w+')
f.write(str(size/2) + ' ' + str(180) + '\n')
for r in range(0, size/2): 
	for t in range(0, 180):
		f.write(str(var_G_final_detail[r][t]) + ' ')
	f.write('\n')
f.close()
		
plt.figure()
plt.imshow(imggray, cmap = plt.cm.gray)
plt.show()

#plt.figure()
#plt.imshow(imgnewsz, cmap = plt.cm.gray)
#plt.show()

plt.figure()
plt.ylabel('Radius')
plt.xlabel('Angle')
plt.imshow(var_g, cmap = plt.cm.gray)
plt.show()

#
plt.figure()
plt.ylabel('Radius')
plt.xlabel('Angle')
plt.imshow(var_G_plot, cmap = plt.cm.gray)
plt.show()
#
#plt.figure()
#plt.ylabel('Radius')
#plt.xlabel('Angle')
#plt.imshow(var_G_plot, cmap = plt.cm.gray)
#plt.show()
