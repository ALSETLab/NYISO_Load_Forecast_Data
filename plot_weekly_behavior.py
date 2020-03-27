import copy
import matplotlib.pyplot as plt
import numpy as np
import datetime
import platform
import copy

def plot_weekly_behavior(zones, data_path):

	# Plotting data on a weekly basis
	now = datetime.datetime.now()

	# Number of weeks in the current month
	n_weeks = list(range(1, int((now.day-1)/8) + 1))

	# Load/forecast data containers
	load_data = dict.fromkeys(zones)
	for zone in load_data:
	    load_data[zone] = dict.fromkeys(n_weeks)

	forecast_data = copy.deepcopy(load_data)
	time_stamp_data = copy.deepcopy(load_data)

	dates = set()

	for zone in zones:
	    n_week = 1
	    start_week = True
	    
	    for day in range(1, now.day):
	        
	        # Validation to limitate the number of weeks
	        if n_week > max(n_weeks):
	            break
	        
	        date = f"{now.month:02d}/{day:02d}/2020"
	        
	        # Getting load and forecast data
	        time_stamp, load, forecast = visualize_load_forecast(date, zone, data_path = "00_NYISO_Data", show_plot = False)
	        
	        # Organizing data per week
	        if start_week:
	            start_date = f"{now.month:02d}/{day:02d}"
	            load_data[zone][n_week] = load
	            forecast_data[zone][n_week] = forecast
	            time_stamp_data[zone][n_week] = time_stamp
	            start_week = False
	        else:
	            load_data[zone][n_week].extend(load)
	            forecast_data[zone][n_week].extend(forecast) 
	            time_stamp_data[zone][n_week].extend(time_stamp)
	        if day % 8 == 0:            
	            dates.add(start_date + f"-{now.month:02d}/{day:02d}")
	            n_week += 1
	            start_week = True
	            
	        del time_stamp, load, forecast
	            
	dates = list(dates)
	            
	if platform.system() == 'Windows':
	    font_plot = "Times New Roman"
	else:
	    font_plot = "liberation sans"
	    
	for zone in zones:
	    fig, axes = plt.subplots(figsize = (16,16), nrows = 3, ncols = 2)            
	    fig.suptitle(f"Weekly Behavior of Load and Forecast ({zone})", fontname = font_plot, fontsize = 22)

	    color_load = 'indigo'
	    color_forecast = 'salmon'
	    color_error = 'darkblue'

	    for week in load_data[zone]:
	        axes[week-1][0].plot(load_data[zone][week], 
	        label = f"Actual Load ({dates[week-1]})", color = color_load, linestyle = '-')
	        axes[week-1][0].plot(forecast_data[zone][week], 
	        label = f"Load Forecast ({dates[week-1]})", color = color_forecast, linestyle = '-')
	        axes[week-1][0].legend(loc = 'lower left', prop = {'size' : 12, 'family' : font_plot})

	        for tick in axes[week-1][0].get_xmajorticklabels():
	            tick.set_rotation(90)

	        for tick in axes[week-1][0].xaxis.get_major_ticks():
	            tick.label.set_fontsize(0)
	            tick.label.set_fontname(font_plot)

	        for tick in axes[week-1][0].yaxis.get_major_ticks():
	            tick.label.set_fontsize(14)
	            tick.label.set_fontname(font_plot)

	        axes[week-1][0].set_ylabel("MW", fontname = font_plot, fontsize = 18)
	        axes[week-1][0].set_title("Actual Load and Forecast", fontname = font_plot, fontsize = 20)

	        axes[week-1][1].plot(np.abs(np.array(load_data[zone][week])-np.array(forecast_data[zone][week])), 
	        label = f"Forecast Error ({dates[week-1]})", color = color_error, linestyle = '-')
	        axes[week-1][1].legend(loc = 'lower left', prop = {'size' : 12, 'family' : font_plot})

	        for tick in axes[week-1][1].get_xmajorticklabels():
	            tick.set_rotation(90)

	        for tick in axes[week-1][1].xaxis.get_major_ticks():
	            tick.label.set_fontsize(0)
	            tick.label.set_fontname(font_plot)

	        for tick in axes[week-1][1].yaxis.get_major_ticks():
	            tick.label.set_fontsize(14)
	            tick.label.set_fontname(font_plot)    

	        axes[week-1][1].set_ylabel("MW", fontname = font_plot, fontsize = 18)
	        axes[week-1][1].set_title("Forecast Error", fontname = font_plot, fontsize = 20)

	    fig.tight_layout()
	    fig.subplots_adjust(top = 0.93)

	    # Saving figure
	    save_path = os.path.join(data_path, "Figs")
	    export_name = f"{zone}_weekly.png"
	    fig.savefig(os.path.join(save_path, export_name), dpi = 300)
	    
	    # Clearing figure and axes
	    fig, axes = None, None

