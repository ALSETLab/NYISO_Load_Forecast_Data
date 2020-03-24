======================================================
DOWNLOAD AND VISUALIZE NYISO DATA
======================================================

This repository contains a set of Python scripts used to massively download, organize and plot. 

Examples of the use of the scripts are found in the Jupyter Notebook '01_Examples.ipynb'.

Below is a list of the signatures of the functions in the repository:

- 'download_nyiso_data(start_year, destination_folder, print_info = False)': this function downloads all the '.csv' files of load forecast and actual load (hourly time-stamp) from the NYISO website from a given start year up to present time. It can be used to update existing files (i.e., does not overwrite pre-existing data).

