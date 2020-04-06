import copy
import matplotlib.pyplot as plt
import numpy as np
import datetime
import platform
import copy
import calendar
from get_start_end_day import*
from visualize_load_forecast import*

def get_weekly_behavior(date, zone, data_path, show_plot = False):

    # Getting start and end day of the week from the given date
    start_day, end_day, _ = get_start_end_day(date)
    
    date_span = end_day - start_day
    
    load_week = []
    forecast_week = []
    worst_forecast_week = []
    time_stamp_week = []
    
    for i in range(date_span.days + 1):
    
        current_date = start_day + datetime.timedelta(days = i)
        
        date = f"{current_date.month:02d}/{current_date.day:02d}/{current_date.year}"
        
        time_stamp_day, load_day, forecast_day, worst_forecast_day = visualize_load_forecast(date, zone, data_path, False)
        
        time_stamp_week.extend(time_stamp_day)
        load_week.extend(load_day)
        forecast_week.extend(forecast_day)
        worst_forecast_week.extend(worst_forecast_day)
    
    if show_plot:
        
        # Selecting font for the plots
        if platform.system() == 'Windows':
            font_plot = "Times New Roman"
        else:
            font_plot = "liberation sans"
            
        color_load = 'indigo'
        color_forecast = 'lightsteelblue'
        color_worst_forecast = 'lightpink'
        color_error = 'darkblue'
        color_worst_error = 'lightskyblue'
            
        fig, axes = plt.subplots(figsize = (16,8), nrows = 1, ncols = 2)
        fig.suptitle(f"Weekly Behavior of Load and Forecast ({zone})", fontname = font_plot, fontsize = 22)
        
        plot_label = f"{start_day.month:02d}/{start_day.day:02d}/{start_day.year} - {end_day.month:02d}/{end_day.day:02d}/{end_day.year}"
        plot_label_save = f"{start_day.month:02d}{start_day.day:02d}{start_day.year}{end_day.month:02d}{end_day.day:02d}{end_day.year}"
        legend_label = f"({start_day.month:02d}/{start_day.day:02d} - {end_day.month:02d}/{end_day.day:02d})"
        
        for tick in axes[0].xaxis.get_major_ticks():
            tick.label.set_fontsize(0)
            tick.label.set_fontname(font_plot)

        for tick in axes[0].yaxis.get_major_ticks():
            tick.label.set_fontsize(14)
            tick.label.set_fontname(font_plot)
        
        axes[0].plot(load_week, color = color_load, label = 'Actual Load ' + legend_label)
        axes[0].plot(forecast_week, color = color_forecast, linestyle = '--', label = 'Best Forecast ' + legend_label)
        axes[0].plot(worst_forecast_week, color = color_worst_forecast, linestyle = '--', label = 'Worst Forecast ' + legend_label)
        axes[0].legend(loc = 'lower right', prop = {'size' : 12, 'family' : font_plot})
        
        axes[0].set_ylabel("MW", fontname = font_plot, fontsize = 18)
        axes[0].set_title(f"Actual Load and Forecast ({plot_label})", fontname = font_plot, fontsize = 20)
        
        axes[1].plot(np.abs(np.array(load_week) - np.array(forecast_week)), 
            label = 'Best Forecast Error ' + legend_label, color = color_error)
        axes[1].plot(np.abs(np.array(load_week) - np.array(worst_forecast_week)), 
            label = 'Worst Forecast Error ' + legend_label, color = color_worst_error)
        axes[1].legend(loc = 'lower right', prop = {'size' : 12, 'family' : font_plot})
        
        axes[1].set_ylabel("MW", fontname = font_plot, fontsize = 18)
        axes[1].set_title(f"Forecast Error ({plot_label})", fontname = font_plot, fontsize = 20)
        
        for tick in axes[1].xaxis.get_major_ticks():
            tick.label.set_fontsize(0)
            tick.label.set_fontname(font_plot)

        for tick in axes[1].yaxis.get_major_ticks():
            tick.label.set_fontsize(14)
            tick.label.set_fontname(font_plot)
        
        fig.tight_layout()
        fig.subplots_adjust(top = 0.90)

        # Saving figure
        save_path = os.path.join(data_path, "Figs")
        export_name = f"{zone}_{plot_label_save}_weekly.png"
        fig.savefig(os.path.join(save_path, export_name), dpi = 300)

        # Clearing figure and axes
        fig, axes = None, None
    
    return time_stamp_week, load_week, forecast_week, worst_forecast_week