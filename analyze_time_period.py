__author__ = 'moerov'

import os
import sys
import geoutilities
from math import sqrt, pi
from random import Random


def number_of_meetings(list_of_users, condition=2):
	ids_frequency = {}
	for user in list_of_users:
		if (user[1] == -42):
			continue
		for id in user[1]:
			if(id in ids_frequency):
				ids_frequency[id] += 1
			else:
				ids_frequency[id] = 1
	number_of_meetings = 0
	for id, counter in ids_frequency.items():
		if counter >= condition and id != -42:
			number_of_meetings += 1
	return number_of_meetings	


def number_of_meetings_per_day_quad(day, pattern_size, number_of_runs):
	import geoutilquad
	#geoutilquad.create_grid(100, 11.2838, './partitions/partitions.circ.20.csv')
	partitions = geoutilquad.load_grid('./partitions/partitions.20.csv')
	count = 0
	for _ in range(number_of_runs):
		time_meetings = geoutilquad.find_meetings_by_partition_on_day('./geolife_data_1.3/filtered_by_week', partitions, day, pattern_size)
		for timestamp in time_meetings:
			#print timestamp, time_meetings[timestamp]
			count += number_of_meetings(time_meetings[timestamp])
		if pattern_size == 1:
			return count
	return float(count/number_of_runs)

def number_of_meetings_per_day_circ(day, pattern_size, number_of_runs):
	import geoutilcirc
	#geoutilcirc.create_grid(100, 11.2838, './partitions/partitions.circ.20.csv')
	partitions = geoutilcirc.load_grid('./partitions/partitions.circ.20.csv')
	count = 0
	for _ in range(number_of_runs):
		time_meetings = geoutilcirc.find_meetings_by_partition_on_day('./geolife_data_1.3/filtered_by_week', partitions, day, pattern_size)
		for timestamp in time_meetings:
			#print timestamp, time_meetings[timestamp]
			count += number_of_meetings(time_meetings[timestamp])
		if pattern_size == 1:
			return count
	return float(count/number_of_runs)

def number_of_meetings_per_day_shifted_circ(day, pattern_size, number_of_runs):
	import geoutilcirc2

	#geoutilcirc2.create_grid(100, 11.2838, './partitions/partitions.circ.shifted.20.csv')
	partitions = geoutilcirc2.load_grid('./partitions/partitions.circ.shifted.20.csv')
	count = 0
	for _ in range(number_of_runs):
		time_meetings = geoutilcirc2.find_meetings_by_partition_on_day('./geolife_data_1.3/filtered_by_week', partitions, day, pattern_size)
		for timestamp in time_meetings:
			#print timestamp, time_meetings[timestamp]
			count += number_of_meetings(time_meetings[timestamp])
		if pattern_size == 1:
			return count
	return float(count/number_of_runs)


def number_of_meetings_per_day_triangles(day, pattern_size, number_of_runs):
	import geoutiltriangl2
	#geoutiltriangl2.create_grid(100, 30.3934, './partitions/partitions.triang2.20.csv')
	partitions = geoutiltriangl2.load_grid('./partitions/partitions.triang2.20.csv')
	count = 0
	for _ in range(number_of_runs):
		time_meetings = geoutiltriangl2.find_meetings_by_partition_on_day('./geolife_data_1.3/filtered_by_week', partitions, day, pattern_size)
		for timestamp in time_meetings:
			#print timestamp, time_meetings[timestamp]
			count += number_of_meetings(time_meetings[timestamp])
		if pattern_size == 1:
			return count
	return float(count/number_of_runs)

def number_of_meetings_per_day_rect(day, pattern_size, number_of_runs):
	import geoutilrect
	#geoutilrect.create_grid(100, 50, 8, './partitions/partitions.rect.20.csv')
	partitions = geoutilrect.load_grid('./partitions/partitions.rect.20.csv')
	count = 0
	for _ in range(number_of_runs):
		time_meetings = geoutilrect.find_meetings_by_partition_on_day('./geolife_data_1.3/filtered_by_week', partitions, day, pattern_size)
		for timestamp in time_meetings:
			#print timestamp, time_meetings[timestamp]
			count += number_of_meetings(time_meetings[timestamp])
		if pattern_size == 1:
			return count
	return float(count/number_of_runs)

def average_number_per_week(pattern_size, number_of_runs):
	quad = circ = circ2 = rect = trian = 0
	for day in range(1, 8):

		progress = float(day) / 8 * 100
		sys.stdout.write("\rProgress: %6.2f%%" % progress)
		sys.stdout.flush()
		quad += number_of_meetings_per_day_quad(day, pattern_size, number_of_runs)
		circ += number_of_meetings_per_day_circ(day, pattern_size, number_of_runs)
		circ2 += number_of_meetings_per_day_shifted_circ(day, pattern_size, number_of_runs)
		rect += number_of_meetings_per_day_rect(day, pattern_size, number_of_runs)
		trian += number_of_meetings_per_day_triangles(day, pattern_size, number_of_runs)
		if day == 7:
			progress = 100
			sys.stdout.write("\rProgress: %6.2f%%" % progress)
			sys.stdout.flush()
	print ''
	print '________________________________________________________'
	print 'Grid of squares: ', quad, '(100%)' 
	print 'Grid of circles: ', circ, '(' + str(int(100*circ/quad))+'%)'
	print 'Grid of shifted circles: ', circ2, '(' + str(int(100*circ2/quad))+'%)'
	print 'Grid of rectangles: ', rect, '(' + str(int(100*rect/quad))+'%)'
	print 'Grid of traingles: ', trian, '(' + str(int(100*trian/quad))+'%)'


def quad_to_other_shapes(partition_length):

	radius = partition_length / (sqrt(pi))
	rect_length = 2.5*partition_length
	rect_width = 0.4*partition_length
	trian_length = 2*partition_length/sqrt(sqrt(3))
	return radius, rect_length, rect_width, trian_length

def create_all_shapes():
	import geoutilquad, geoutilcirc, geoutilcirc2, geoutilrect, geoutiltriangl2



if __name__ == "__main__":
	
	average_number_per_week(8, 50)
	
