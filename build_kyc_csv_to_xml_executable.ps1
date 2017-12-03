#compiles our python script to an exectuable
#then builds a zip file with readme, the exectuable, and the python source.
pyinstaller --noconfirm --onefile kyc_csv_to_adobe_xml.py
Compress-Archive -Force -Path .\dist\kyc_csv_to_adobe_xml.exe, .\readme.txt, .\kyc_csv_to_adobe_xml.py -DestinationPath dist\kyc_csv_to_xml.zip
