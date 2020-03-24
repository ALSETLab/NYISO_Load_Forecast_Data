# Importing required libraries
import urllib.request
import os
import datetime
import zipfile

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