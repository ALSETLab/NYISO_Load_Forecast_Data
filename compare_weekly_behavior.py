import datetime
from get_start_end_day import*

def compare_weekly_behavior(date, comparison_year):
	'''
	- start_day: start day of the week (i.e., monday)

	'''

	####################################################
	################ PROCESSING DATES ##################
	####################################################
	
	# Getting start and end day
	start_day, end_day, week_number = get_start_end_day(date)
	
	# Getting start and end day of the comparison year

	d = f"{comparison_year}-W{week_number}" # date of the comparison year given the week number
	r = datetime.datetime.strptime(d + '-1', "%G-W%V-%u") # monday of the corresponding week

	start_day_comp, end_day_comp, _ = get_start_end_day(f"{r.month:02d}/{r.day:02d}/{r.year}")

	



