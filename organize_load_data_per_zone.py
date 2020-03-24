import pandas as pd
import pickle
import os

def organize_data_per_zone(data_directory):
	'''
	
	'''


	nys_zones = set()

	# Getting the list of folders
	folders = os.listdir(directory)

	for folder in folders:
    
	    if folder in ["01_Load_Raw_Info_5_Minute_Basis", "02_Load_Raw_Info_Hourly_Basis"]:
	        # Getting the list of csv files inside each folder
	        csv_subfolders = os.listdir(directory + folder)
	        for subfolder in csv_subfolders:
	            csv_files = os.listdir(directory + folder + "/" + subfolder)
	            for file in csv_files:
	                # Loading csv file in a Pandas dataframe
	                df_aux = pd.read_csv(directory + folder + "/" + subfolder + "/" + file)
	                zones_nys_ps = df_aux["Name"].unique()
	                # Getting the information about each zone
	                for zone in zones_nys_ps:
	                    # Adding to a set to determine how many different zones are
	                    nys_zones.add(zone)

	                    # Creating a temporary Pandas dataframe
	                    df_temp = pd.DataFrame([], columns = ["Time Stamp", "Load"])

	                    # Normalizing the data
	                    if folder == "01_Load_Raw_Info_5_Minute_Basis":
	                        df_temp["Load"] = df_aux[df_aux["Name"] == zone]["Load"].values / df_aux[df_aux["Name"] == zone]["Load"].max()
	                    else:
	                        df_temp["Load"] = df_aux[df_aux["Name"] == zone]["Integrated Load"].values / df_aux[df_aux["Name"] == zone]["Integrated Load"].max()
	                    
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

	                    # Saving the data

	                    # Name of the file
	                    filename = file[:-7] + "_" + zone + "_normalized"
	                    
	                    # Folder to save the data
	                    if folder == "01_Load_Raw_Info_5_Minute_Basis":
	                        folder_save = "5_Minute_Basis"
	                    else:
	                        folder_save = "Hourly_Basis"  
	                    
	                    dir_path = "99_Data/03_Normalized_Load_Data/" + zone + "/" + folder_save
	                    #print(dir_path)
	                    if not os.path.exists(dir_path):
	                        os.makedirs(dir_path)
	                    
	                    save_file = os.path.join(dir_path, filename) + ".pkl"
	                    #print(save_file)
	                    
	                    with open(save_file, 'wb') as f:
                        pickle.dump(df_temp, f, pickle.HIGHEST_PROTOCOL)
	toc()