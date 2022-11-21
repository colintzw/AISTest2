import numpy as np
import glob
import os
import cv2


def projectOnAxis(inputImg, axisToProj):
	if len(inputImg.shape) == 3:
		# assume that its greyscale converted to rgb
		img = inputImg[:, :, 0]
	else:
		img = inputImg

	# this calculates the average pixel value for each col/row in percent from 255.
	proj = np.sum(img, axis=axisToProj) / (255 * img.shape[axisToProj])
	return proj


def segmentSingleAxis(projection):
	regions = []
	regionMinSize = 2
	regionSize = 1
	curr_start = 0
	for nn in range(1, len(projection)):
		if projection[nn] == 1:
			if regionSize >= regionMinSize:
				regions.append((curr_start, nn - 1))
			regionSize = 0
		elif (regionSize == 0):
			regionSize = 1
			curr_start = nn
		else:
			regionSize += 1

	if regionSize >= regionMinSize:
		regions.append((curr_start, len(projection) - 1))

	return regions


def segmentImg(img):
	xProj = projectOnAxis(img, 0)
	segLimits = segmentSingleAxis(xProj)
	# segments are already sorted from left to right
	segments = []
	for low, up in segLimits:
		segments.append(img[:, low:up])

	return segments


def trimAxis(img, axis=0):
	proj = projectOnAxis(img, axis)
	axisStart = np.argmax(proj != 1)
	axisEnd = len(proj) - np.argmax(proj[::-1] != 1)
	return (axisStart, axisEnd)


def trimImg(img):
	ax1l, ax1u = trimAxis(img, axis=0)
	ax0l, ax0u = trimAxis(img, axis=1)
	return img[ax0l:ax0u, ax1l:ax1u]


def dHash(inImg):
	# silly datatype issue as we load with cv2
	img = np.array(inImg, dtype='int')
	diff = img[1:, :] - img[:-1, :]
	# convert to tuple so that we can use set()
	return tuple(diff.reshape(-1))


def loadAndComputeHashes(segmentPath):
	fileList = glob.glob(segmentPath + "\\*.png")
	hashDict = dict()
	for file in fileList:
		img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
		computedHash = dHash(img)
		hashDict[computedHash] = os.path.basename(file).replace('.png', '')
	return hashDict


def readImg(file, hashDict):
	img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
	_, tImg = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
	trimmed = trimImg(tImg)
	segments = segmentImg(trimmed)
	readLetters = []
	for seg in segments:
		computedHash = dHash(seg)
		readLetters.append(hashDict[computedHash])

	return readLetters
