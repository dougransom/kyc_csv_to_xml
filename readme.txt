The  executable program kyc_csv_to_adobe_xml.exe (or the python program kyc_csv_to_adobe_xml.py) converts files downloaded 
from NBIN compass into files that can populate  iA Securities New Client Account Forms from July 2017.


Here is what you need to do to get it working:
 
Step 1:  Get the program installed.
* Option 1.  Use the prebuilt 
	This is the simpler option.  You should have a program kyc_csv_to_adobe_xml.exe already in the folder.  You can run this to produce the desired
	output.  
* Option 2.  Install Python and use a the script  kyc_csv_to_adobe_xml.py
	This is the best option if you plan to make changes to the script or you need to use it on a platform
	other than windows.
	- install Python 3.6 or later on your PC.  Find the  latest release on 
	https://www.python.org/downloads/ and download the Windows x86-64 web-based installer.  Run it.


Step1: Create a folder for your work. 
	You will want a new folder specifically for all the files that will produced by this program, as you will have a unique file for each client number.
	Create thew new folder with windows explorer.

Step 2: Download files from NBIN
	Log into your National Bank Independent Network (aka National Bank Corresppendant Network)
	From the compass home page, choose data export.  
	Request data set "Account Profile - KYC Export" for all RR Codes
	Request data set "My Name and Address Extract" for all RR Codes
	Go to the Recent Files tab and hit refresh.  Those files should be available to download.  They will have names like 255968_KYC_1121_109.csv and 255968_NAA_1125_1.csv
	Download them to the new folder you created.
	
Step 3:  Option Install Python
    If you want to edit the source code befor you run it, or you are not on windows, you will need Python 3.6 or later installed on your system. 

Step 4:   Download the code.  	
     The code can be retrieved from GitHub.  
	 https://github.com/dougransom/kyc_csv_to_xml/releases
	 
	 Download the zip file kyc_csv_to_xml.zip into your new folder and 
	 extract the files into that folder.  You can use windows explorer
	 or 
	    Expand-Archive '..\account profile\dist\kyc_csv_to_xml.zip'  -DestinationPath .
	in Windows Powershell 
	 

Step5:	
	Start Windows Powershell or Windows Command Prompt
	https://winaero.com/blog/all-ways-to-open-powershell-in-windows-10/
	
	Us the "cd" command to change folder to the new folder you created, and your two CSV files are stored.
	https://technet.microsoft.com/en-us/library/ee176962.aspx

	i.e. cd "C:\Users\Doug\OneDrive\doug\work in progress\account profile\".  
	
	
Step6:
	In your Power Shell
	
	kyc_csv_to_adobe_xml.exe name-of-your-csv-file name-of-your-address-file

	or if you installed Python, 
	
	python kyc_csv_to_adobe_xml.py name-of-your-csv-file name-of-your-address-file



That will create a file for each of your cient numbers with an extension xml.  That file can be imported into many PDF programs 
including Foxit Reader (free), Nuance PDF Professional, 
and various Adobe products (but not Adobe Reader DC).  
Open the appropriate NCAF in your PDF program.  Use the forms menu to import data.

You cannot use Adobe Reader DC!!!  If you want a free program, use Foxit Reader.  

 

