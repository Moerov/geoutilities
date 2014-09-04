__author__ = 'moerov'

import os
import sys
import geoutilities
from math import sqrt, pi


def number_of_meetings(list_of_users, condition=2):
	ids_frequency = {}
	for user in list_of_users:
		if(user[1] in ids_frequency):
			ids_frequency[user[1]] += 1
		else:
			ids_frequency[user[1]] = 1
	number_of_meetings = 0
	for id, counter in ids_frequency.items():
		if counter >= condition and id != -42:
			number_of_meetings += 1
	return number_of_meetings	


def analyse_quad_grid(day):
	import geoutilquad
	#geoutilquad.create_grid(100, 11.2838, './partitions/partitions.circ.20.csv')
	partitions = geoutilquad.load_grid('./partitions/partitions.20.csv')
	time_meetings = geoutilquad.find_meetings_by_partition_on_day(
		'./geolife_data_1.3/filtered_by_week', partitions, day)
	count = 0
	for timestamp in time_meetings:
		#print timestamp, time_meetings[timestamp]
		count += number_of_meetings(time_meetings[timestamp])
	return count

def analyse_circ_grid(day):
	import geoutilcirc

	#partitions = geoutilcirc.create_partinioned_bounding_box(100, 11.2838)
	#geoutilcirc.create_grid(100, 11.2838, './partitions/partitions.circ.20.csv')
	partitions = geoutilcirc.load_grid('./partitions/partitions.circ.20.csv')
	#print geoutilcirc.find_partition_to_point(partitions, (40.15, 116))

	time_meetings = geoutilcirc.find_meetings_by_partition_on_day(
		'./geolife_data_1.3/filtered_by_week', partitions, day)
	count = 0
	for timestamp in time_meetings:
		#print timestamp, time_meetings[timestamp]
		count += number_of_meetings(time_meetings[timestamp])
	return count

def analyse_shifted_circ_grid(day):
	import geoutilcirc2

	#geoutilcirc2.create_grid(100, 11.2838, './partitions/partitions.circ.shifted.20.csv')
	partitions = geoutilcirc2.load_grid('./partitions/partitions.circ.shifted.20.csv')

	time_meetings = geoutilcirc2.find_meetings_by_partition_on_day(
		'./geolife_data_1.3/filtered_by_week', partitions, day)
	count = 0
	for timestamp in time_meetings:
		#print timestamp, time_meetings[timestamp]
		count += number_of_meetings(time_meetings[timestamp])
	return count


def analyse_triangles2(day):
	import geoutiltriangl2
	#geoutiltriangl2.create_grid(100, 30.3934, './partitions/partitions.triang2.20.csv')
	partitions = geoutiltriangl2.load_grid('./partitions/partitions.triang2.20.csv')
	

	time_meetings = geoutiltriangl2.find_meetings_by_partition_on_day(
		'./geolife_data_1.3/filtered_by_week', partitions, day)
	count = 0
	for timestamp in time_meetings:
		#print timestamp, time_meetings[timestamp]
		count += number_of_meetings(time_meetings[timestamp])
	return count


def compare_shapes():
	quad = circ = circ2 = rect = trian = 0
	for i in range(1, 8):
		quad += analyse_quad_grid(i)
		circ += analyse_circ_grid(i)
		circ2 += analyse_shifted_circ_grid(i)
		rect += analyse_rect_grid(i)
		trian += analyse_triangles2(i)
	print 'Grid of squares: ', quad, '(100%)' 
	print 'Grid of circles: ', circ, '(' + str(int(100*circ/quad))+'%)'
	print 'Grid of shifted circles: ', circ2, '(' + str(int(100*circ2/quad))+'%)'
	print 'Grid of rectangles: ', rect, '(' + str(int(100*rect/quad))+'%)'
	print 'Grid of traingles: ', trian, '(' + str(int(100*trian/quad))+'%)'

def analyse_rect_grid(day):
	import geoutilrect
	#geoutilrect.create_grid(100, 50, 8, './partitions/partitions.rect.20.csv')
	partitions = geoutilrect.load_grid('./partitions/partitions.rect.20.csv')
	time_meetings = geoutilrect.find_meetings_by_partition_on_day(
		'./geolife_data_1.3/filtered_by_week', partitions, day)
	count = 0
	
	for timestamp in time_meetings:
		#print timestamp, time_meetings[timestamp]
		count += number_of_meetings(time_meetings[timestamp])
	return count

def quad_to_other_shapes(partition_length):

	radius = partition_length / (sqrt(pi))
	rect_length = 2.5*partition_length
	rect_width = 0.4*partition_length
	trian_length = 2*partition_length/sqrt(sqrt(3))
	return radius, rect_length, rect_width, trian_length

if __name__ == "__main__":
	compare_shapes()
	#analyse_circ_grid(7)
	
