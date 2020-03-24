# Importing required libraries
import urllib.request
import os
import datetime
import zipfile
import pandas as pd
import pickle

def download_nyiso_data(start_year = 1999, destination_folder = "00_Raw_Data", print_info = False):

    ######################################
    ###### CREATING DATA STRUCTURE #######
    ######################################

    # Creating destination folder if it does not exist yet
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Creating data organization structure inside destination folder
    load_forecast_path = os.path.join(destination_folder, "Load_Forecast")
    actual_load_path = os.path.join(destination_folder, "Actual_Load")

    if not os.path.exists(load_forecast_path):
        os.makedirs(load_forecast_path)

    if not os.path.exists(actual_load_path):
        os.makedirs(actual_load_path)

    # Folders for raw data
    raw_lf_data_path = os.path.join(load_forecast_path, "00_Raw_Data")
    raw_actual_load_path = os.path.join(actual_load_path, "00_Raw_Data")

    if not os.path.exists(raw_lf_data_path):
        os.makedirs(raw_lf_data_path)

    if not os.path.exists(raw_actual_load_path):
        os.makedirs(raw_actual_load_path)

    # Folders for processed data
    processed_lf_data_path = os.path.join(load_forecast_path, "01_Processed_Data")
    processed_actual_load_path = os.path.join(actual_load_path, "01_Processed_Data")

    if not os.path.exists(processed_lf_data_path):
        os.makedirs(processed_lf_data_path)

    if not os.path.exists(processed_actual_load_path):
        os.makedirs(processed_actual_load_path)

    ######################################
    ### DOWNLOADING LOAD FORECAST DATA ###
    ######################################

    # Getting actual date
    now = datetime.datetime.now()

    if start_year <= 2001:
        start_year = 2001

    # Download '.zip' files for monthly information
    for year in range(start_year, now.year + 1):

        download_folder = os.path.join(raw_lf_data_path, f"{year}")

        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        for month in range(1, 13):

            # Guaranteeing that the script downloads the data as given from NYISO records
            if year == 2001 and month < 6:
                continue

            # Stop downloading data at current year and month
            if year == now.year and month > now.month:
                break

            filename = f"{year}{month:02d}01isolf_csv.zip"
            url = f"http://mis.nyiso.com/public/csv/isolf/{filename}"
            file = os.path.join(download_folder, filename)

            # Skipping already downloaded files
            if not os.path.exists(file):
                urllib.request.urlretrieve(url, file)
                # Unzipping files
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall(file[0:-4])
                # Removing '.zip' file
                if file.endswith(".zip"):
                    os.remove(file)

    # Print info statement when all files have been downloaded
    if print_info:
        print(f"Load forecast '.zip' files download completed up to {now.month}/{now.year}")

    ######################################
    ###### DOWNLOADING ACTUAL DATA #######
    ######################################

    # Downloading data of actual load (with hourly time-stamp)
    for year in range(start_year, now.year + 1):

        # Download folder
        download_folder = os.path.join(raw_actual_load_path, f"{year}")

        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        for month in range(1, 13):
            
            if year == 2001 and month < 6:
                continue

            if year == now.year and month > now.month:
                break

            filename = f"{year}{month:02d}01palIntegrated_csv.zip"
            url = f"http://mis.nyiso.com/public/csv/palIntegrated/{filename}"
            file = os.path.join(download_folder, filename)
            
            # Skipping already downloaded files
            if not os.path.exists(file):
                urllib.request.urlretrieve(url, file)
                # Unzipping files
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall(file[0:-4])
                # Removing '.zip' file
                if file.endswith(".zip"):
                    os.remove(file)

    # ORGANIZING ACTUAL LOAD DATA PER ZONE
    organizing_actual_load_data_per_zone(raw_actual_load_path, processed_actual_load_path)

def organizing_actual_load_data_per_zone(raw_data_path, write_data_path):

    # Set to gather the info of the New York State power grid load zones
    nys_zones = set()

    # Getting subfolders
    year_subfolders = os.listdir(raw_data_path)

    for year_subfolder in year_subfolders:

        year_subfolder_path = os.path.join(raw_data_path, year_subfolder)
        
        # Path of the subfolder files containing the 'csv' files for each year   
        csv_subfolders = [os.path.join(year_subfolder_path, csv_subf) for csv_subf in os.listdir(year_subfolder_path)]

        for csv_subf in csv_subfolders:

            # Getting a list of the '.csv' files in each csv subfolder
            csv_files = [os.path.join(csv_subf, csv_file) for csv_file in os.listdir(csv_subf)]
            csv_files_names = os.listdir(csv_subf)

            # Clearing variables for auxiliary containers
            df_aux = None
            df_temp = None

            for n_csv_file, csv_file in enumerate(csv_files):

                # Loading '.csv' file in a Pandas dataframe
                df_aux = pd.read_csv(csv_file)

                zones_nys_ps = df_aux["Name"].unique()

                for zone in zones_nys_ps:
                    # Name of the target file
                    filename = csv_files_names[n_csv_file][:-17] + "_" + zone
                    
                    # Path of the target folder
                    target_path = os.path.join(os.path.join(write_data_path, year_subfolder), zone)

                    # Creating target folder if it does not exist
                    if not os.path.exists(target_path):
                        os.makedirs(target_path)
                
                    save_file_path = os.path.join(target_path, filename) + ".pkl"
                    
                    # Skip operations if the file already exists
                    if os.path.exists(save_file_path):
                        continue

                    # Adding a set to determine how many different zones are in NY grid
                    nys_zones.add(zone)

                    # Creating a temporary Pandas dataframe
                    df_temp = pd.DataFrame([], columns = ["Time Stamp", "Load"])

                    # Getting the load data
                    df_temp["Load"] = df_aux[df_aux["Name"] == zone]["Integrated Load"].values

                    # Filling the missing values using the next available values
                    df_temp.fillna(method = 'ffill')

                    # Convert time stamp to datetime format
                    df_temp["Time Stamp"] = df_aux[df_aux["Name"] == zone]["Time Stamp"].values

                    time_values = []
                    for date in df_temp["Time Stamp"]:
                        date_aux_1 = datetime.datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
                        time_values.append(date_aux_1)
                
                    df_temp.drop("Time Stamp", axis = 1, inplace = True)
                    df_temp["Time Stamp"] = time_values

                    with open(save_file_path, 'wb') as f:
                        pickle.dump(df_temp, f, pickle.HIGHEST_PROTOCOL)

                    # Cleaning pandas dataframe
                    if df_temp is not None:
                        df_temp = None

                # Cleaning pandas dataframe
                if df_aux is not None:
                    df_aux = None