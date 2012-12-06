#!/bin/python

import sys
import re
import string
import scipy

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

file1 = sys.argv[1]
file2 = sys.argv[2]

n_coef_wl = 40
n_coef_F  = 180

img1 = read_coef(file1, n_coef_wl, n_coef_F)
img2 = read_coef(file2, n_coef_wl, n_coef_F)

print cross_corr(n_coef_wl, n_coef_F, img1, img2)
