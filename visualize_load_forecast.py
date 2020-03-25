import pandas as pd
import matplotlib.pyplot as plt
import os
import pickle
import datetime
import platform
import numpy as np

def visualize_load_forecast(date, region, data_path = os.getcwd()):

	given_date = datetime.datetime.strptime(date, '%m/%d/%Y')

	# Extract year and month from given date
	year = given_date.year
	month = given_date.month
	day = given_date.day

	# Getting path to processed data folders
	processed_actual_load_data_path = os.path.join(os.path.join(data_path, "Actual_Load"), "01_Processed_Data")
	processed_forecast_load_data_path = os.path.join(os.path.join(data_path, "Load_Forecast"), "01_Processed_Data")

	# Paths to commanded files
	filename = f"{year}{month:02d}{day:02d}_{region}.pkl" # Common for both

	actual_load_data_file = os.path.join(os.path.join(os.path.join(processed_actual_load_data_path, 
		str(year)), region), filename)
	forecast_load_data_file = os.path.join(os.path.join(os.path.join(processed_forecast_load_data_path, 
		str(year)), region), filename)

	infile = open(actual_load_data_file, 'rb')
	actual_load = pickle.load(infile)

	infile = open(forecast_load_data_file, 'rb')
	forecast_load = pickle.load(infile)

	# Increasing given date by one day to filter the time stamp of the forecast data
	given_date += datetime.timedelta(days=1) 

	# Filtering the forecasted load up to the given date
	forecast_load_filtered = forecast_load[forecast_load["Time Stamp"] < given_date]

	hour_minute = []

	for date in actual_load["Time Stamp"]:
		hour_minute.append(f"{date.hour:02d}:{date.minute:02d}")

	fig, axes = plt.subplots(figsize = (16,8), nrows = 1, ncols = 2)

	if platform.system() == 'Windows':
		font_plot = "Times New Roman"
	else:
		font_plot = "liberation sans"

	fig.suptitle(f"{region} - {month:02d}/{day:02d}/{year}", fontname = font_plot, fontsize = 22)

	axes[0].plot(hour_minute, actual_load["Load"].values, 
		label = "Actual Load", color = 'indigo', marker = 'o', linestyle = '--')
	axes[0].legend(prop = {'size' : 16, 'family' : font_plot})
	axes[0].plot(hour_minute, forecast_load_filtered["Load Forecast"].values, 
		label = "Load Forecast", color = 'salmon', marker = 'o', linestyle = '--')
	axes[0].legend(prop = {'size' : 16, 'family' : font_plot})
	axes[0].set_ylabel("MW", fontname = font_plot, fontsize = 18)
	axes[0].set_title("Actual Load and Forecast", fontname = font_plot, fontsize = 20)


	for tick in axes[0].get_xmajorticklabels():
		tick.set_rotation(90)

	for tick in axes[0].xaxis.get_major_ticks():
		tick.label.set_fontsize(14)
		tick.label.set_fontname(font_plot)

	for tick in axes[0].yaxis.get_major_ticks():
		tick.label.set_fontsize(14)
		tick.label.set_fontname(font_plot)

	axes[1].plot(hour_minute, np.abs(actual_load["Load"].values - forecast_load_filtered["Load Forecast"].values), 
		label = "Forecast Absolute Error", color = 'darkblue', marker = 'o', linestyle = '--')
	axes[1].legend(prop = {'size' : 16, 'family' : font_plot})
	axes[1].set_ylabel("MW", fontname = font_plot, fontsize = 18)
	axes[1].set_title("Forecast Error", fontname = font_plot, fontsize = 20)

	for tick in axes[1].get_xmajorticklabels():
		tick.set_rotation(90)

	for tick in axes[1].xaxis.get_major_ticks():
		tick.label.set_fontsize(14)
		tick.label.set_fontname(font_plot)

	for tick in axes[1].yaxis.get_major_ticks():
		tick.label.set_fontsize(14)
		tick.label.set_fontname(font_plot)

	fig.tight_layout()
	fig.subplots_adjust(top = 0.90)

	# Saving figure
	save_path = os.path.join(data_path, "Figs")

	if not os.path.exists(save_path):
		os.makedirs(save_path)

	export_name = f"{month:02d}{day:02d}{year}_{region}.png"

	fig.savefig(os.path.join(save_path, export_name), dpi = 300)

	return actual_load["Time Stamp"], actual_load["Load"].values, forecast_load_filtered["Load Forecast"].values