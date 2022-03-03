# yandexDiskDownloader
Script to download all files from a folder on Yandex.Disk

Usage of this is very simple. Currently it is tested only for files in one folder, not subfolders. 
Copy your yandex disk folder url in this format - https://disk.yandex.ru/d/ + 14 characters of unique ID. 

Edit configProd.yaml file

targetUrl: yandex disk folder url
destination_folder: where you want to download all files
number_of_files: number of files in yandex disk folder

I've used testConfig file to keep my secrets, so you also need to change line 12 to configProd.yaml or create your own configTest.yaml file. 

That's it. Just run the script.

Leave me a message if you have any question related to this script. 
