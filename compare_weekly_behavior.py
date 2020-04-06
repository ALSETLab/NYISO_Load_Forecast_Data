import calendar
import datetime
from get_start_end_day import*
from get_weekly_behavior import*
import matplotlib.pyplot as plt

def compare_weekly_behavior(date, comparison_year, zone, data_path):
    '''
    - start_day: start day of the week (i.e., monday)

    '''
    
    ####################################################
    ################ PROCESSING DATES ##################
    ####################################################

    if type(comparison_year) == "list":
        print("Hi")
        # Just one year is being compared
        comparison_year = comparison_year[0]
    
    # Getting start (Monday) and end day (Sunday) of the week with the given date
    start_day, end_day, week_number = get_start_end_day(date)
    
    # Getting start and end day of the comparison year
    
    d = f"{comparison_year}-W{week_number}" # date of the comparison year given the week number
    r = datetime.datetime.strptime(d + '-1', "%G-W%V-%u") # monday of the corresponding week

    start_day_comp, end_day_comp, _ = get_start_end_day(f"{r.month:02d}/{r.day:02d}/{r.year}")

    #print(calendar.monthcalendar(date.year, date.month))
    
    time_stamp_or, load_week_or, forecast_week_or, worst_forecast_week_or = \
    get_weekly_behavior(f"{start_day.month:02d}/{start_day.day:02d}/{start_day.year}", zone, data_path, False)
    
    
    time_stamp_comp, load_week_comp, forecast_week_comp, worst_forecast_week_comp = \
    get_weekly_behavior(f"{start_day_comp.month:02d}/{start_day_comp.day:02d}/{start_day_comp.year}", zone, data_path, False)
    
    fig, axes = plt.subplots(figsize = (16, 8), nrows = 1, ncols = 2)
    
    axes[0].plot(load_week_or, label = f"{start_day.year}: {start_day.month}/{start_day.day} - {end_day.month}/{end_day.day}")
    axes[0].plot(load_week_comp, label = f"{start_day_comp.year}: {start_day_comp.month}/{start_day_comp.day} - {end_day_comp.month}/{end_day_comp.day}")
    axes[0].legend()
    axes[0].set_title(f"Actual Load in {zone}")
    
    axes[1].plot(np.abs(np.array(load_week_or) - np.array(forecast_week_or)),
    label = f"{start_day.year}: {start_day.month}/{start_day.day} - {end_day.month}/{end_day.day}")
    axes[1].plot(np.abs(np.array(load_week_comp) - np.array(forecast_week_comp)), 
    label = f"{start_day_comp.year}: {start_day_comp.month}/{start_day_comp.day} - {end_day_comp.month}/{end_day_comp.day}")
    axes[1].legend()
    axes[1].set_title(f"Forecast Error in {zone}")