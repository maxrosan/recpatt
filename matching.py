#!/bin/python

import sys
import re
import string
import scipy
import os

def read_coef(filen, nwl, nF):
	f = open(filen, 'r')

	print "Reading " + filen
	(rad, angle) = re.match('(\d+) (\d+)', f.readline()).groups()
	
	result = scipy.zeros((nwl, nF), float)

	for i in range(0, nwl):
		ln = f.readline()
		result[i] = [float(x) for x in string.split(ln, ' ')[:nF]]

	return result

def cross_corr(nW, nF, img1, img2): 
	result = 0

	m1 = scipy.mean(img1)
	m2 = scipy.mean(img2)

	d1 = scipy.std(img1)
	d2 = scipy.std(img2)

	for i in range(0, nW):
		for j in range(0, nF):
			result = result + (img1[i][j] - m1)*(img2[i][j] - m2)

	result = result/(nW*nF*d1*d2)

	return result

#file1 = sys.argv[1]
#file2 = sys.argv[2]

n_coef_wl = 40
n_coef_F  = 90

#img1 = read_coef(file1, n_coef_wl, n_coef_F)
#img2 = read_coef(file2, n_coef_wl, n_coef_F)

#print cross_corr(n_coef_wl, n_coef_F, img1, img2)

files = os.listdir('pics/')
f = open('output.html', 'w+')

f.write('<html><body><table>')
f.write('<tr>')
f.write('<td> - </td>')
for x in files:
	f.write('<td>' + x + '</td>')
f.write('</tr>')

for x in files:
	f.write('<tr>')
	f.write('<td>' + x  + '</td>')

	for y in files:
		if x != y:

			img1 = read_coef('db/aprox/pics_' + x + '.txt', n_coef_wl, n_coef_F)
			img2 = read_coef('db/aprox/pics_' + y + '.txt', n_coef_wl, n_coef_F)

			f.write('<td>' + str(cross_corr(n_coef_wl, n_coef_F, img1, img2)) + '</td>')

		else:
			
			f.write('<td> - </td>')

	f.write('</tr>')


f.write('</table></body></html>')

f.close()
