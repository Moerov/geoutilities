__author__ = 'moerov'

import os
import sys
import geoutilities



def analyse_quad_grid(day):
	import geoutilquad

	partitions = geoutilquad.load_grid('./partitions/partitions.20.csv')
	time_meetings = geoutilquad.find_meetings_by_partition_on_day(
		'./geolife_data_1.3/filtered_by_week', partitions, day)
	count = 0
	for timestamp in time_meetings:
		if(len(time_meetings[timestamp]) > 1):
			count+=1
	print 'Quadratic grid, count = ', count


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
		column = 1
		for i, item in enumerate(time_meetings[timestamp]):
			column*=item[1][0]
		if(len(time_meetings[timestamp]) > 1 and column > 0):
			count+=1
	print 'Grid of circles, count = ', count

def analyse_shifted_circ_grid(day):
	import geoutilcirc2
	#geoutilcirc2.create_grid(100, 11.2838, './partitions/partitions.circ.shifted.20.csv')
	partitions = geoutilcirc2.load_grid('./partitions/partitions.circ.shifted.20.csv')

	# geoutilcirc2.find_partition_to_point(partitions, (40.3, 116.50))

	time_meetings = geoutilcirc2.find_meetings_by_partition_on_day(
		'./geolife_data_1.3/filtered_by_week', partitions, day)
	count = 0
	for timestamp in time_meetings:
		column = 1
		for i, item in enumerate(time_meetings[timestamp]):
			column*=item[1][0]
		if(len(time_meetings[timestamp]) > 1 and column > 0):
			count+=1
	print 'Grid of circles, count = ', count


if __name__ == "__main__":
	analyse_quad_grid(1)
	analyse_circ_grid(1)
	analyse_shifted_circ_grid(1)