import datetime

def get_start_end_day(date):
	'''
	This function gets the start day (corresponding Monday) and the end day (Sunday) 
	of a specific week given the date of an arbitrary day
	'''

	# Current date
	now = datetime.datetime.now() 

	# Converting 'date' to datetime format
	given_date = datetime.datetime.strptime(date, '%m/%d/%Y')

	# Getting the date in ISO format to catch the information of year, week_number and weekday
	year, week_number, weekday = datetime.date(given_date.year, given_date.month, given_date.day).isocalendar()

	# Getting the starting day of that week
	start_day = datetime.datetime.strptime(f"{year}-W{week_number}-1", "%G-W%V-%u")

	end_day = start_day + datetime.timedelta(days = 6.9)
	
	# If the end_day of the week is in the future (or is today), set it to the previous day so that all NYISO data is available
	if end_day > now:
		end_day = now
		end_day += datetime.timedelta(days=-1)

	return start_day, end_day, week_number