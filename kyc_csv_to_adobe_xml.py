import argparse
import sys
import xml.etree.ElementTree as ET
import re

version = 0.3

program_description =   f"""Creates XML files that can be used to populate iA Securities New Client Account Forms (July 2017 Version). \r\n
Supply the KYC and Name and Address File Export form NBCN Compass https://www.nbin.ca/lrportal/group/nbcn-compass/dataexport    
Many of the fields will be populated.  The Client Name will need require tweaking.  The address fields will not 
import correctly for addresses longer than two lines.

Marital Status and Citenzhip are not imported.

The data you can expect to imported are:  client number, tombstone information of primary account owner, address info, and 
types of accounts that are opened (i.e. a/e/r/s etc).  

A separate file will be created for each client number, in the form clientnumber.xml.  You will need a program
that can import the file into a form.  Acrobat Reader DC cannot do this.  Foxit Reader can import data into a form and it is free.
Nuance Power PDF Professional can do it, and so can some editions of Adobe Acrobat.

Version: {version}  """

                                                  

parser=argparse.ArgumentParser(description=program_description,formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('infile_kyc', help=" specify the file name of the KYC export file.  ")
parser.add_argument('infile_name_and_address', help=" specify the name of the file of the Name and Address export")

parsed=parser.parse_args()
infile_kyc=parsed.infile_kyc
infile_address  = parsed.infile_name_and_address
print("processing {0} {0}".format(infile_kyc,infile_address))


# we only need the first account for the client, since we are  only pulling boilerplate for the client,
# not objectives and risk tolerance per account
def select_unique_clients(reader):
    client_numbers=set()
    for row in reader:
        client_number = row["Client Number"]
        if client_number not in client_numbers:
            client_numbers.add(client_number)
            yield row



xfdf_attrib_ns = "http://ns.adobe.com/xfdf-transition/"  #namespace for field attributes required by adobe
xfdf_attrib_ns_et = "{0}{1}{2}".format("{",xfdf_attrib_ns,"}")
xfdf_original = "{0}{1}".format(xfdf_attrib_ns_et, "original")


def row_to_xml(row,letters_dict):
    fieldnumber=0
    fields = ET.Element("fields")

    #write an xml field in a format that will be picked up by acrobat and matched to a field name of "text_name"
    #i is important elementName be unique in the  document.

    def write_xml_field(elementName, text_name, value):
        subelement = ET.SubElement(fields, elementName, {xfdf_original: text_name})
        subelement.text = value

    ET.register_namespace("xfdf",xfdf_attrib_ns )
    repcode=row["Client RR Code"]



    def iso_to_american_date(isodate):
        day = isodate[-2:]
        year = isodate[0:4]
        month = isodate[4:6]
        return "{0}/{1}/{2}".format(month,day,year)


	#field names are different in CSV and the PDF, so transform them
    mapCSVtoXML = {
     'Account Name' : 'L name',
     'Client RR Code': 'IA Code',
     'Client Number': 'Client ID',
     'Client SIN': 'SIN',
     'Client Email Address': 'E-mail',
      'Province/Res': 'Prov',
      'Client Income': 'AAIS',
       'Client Occupation': 'Occupation',
        'Employer description': 'Employer Name and Address',
    }

	#any fields not in mapCSVtoXML require special handling
    write_xml_field('ClientEmailAddressElectronic', '409 2 e mail',row["Client Email Address"])

    birthday=iso_to_american_date(row['Client Date of birth'])
    write_xml_field("ClientBirthday1","Date year",birthday)




    for k,v in mapCSVtoXML.items():
        subelement=ET.SubElement(fields,"ImportNumber{0}".format(fieldnumber), {xfdf_original : v})
        value = row[k]
        subelement.text = value
        fieldnumber=1+fieldnumber

    client_phone_number = row["Client Phone Number"]
    client_area_code = client_phone_number[1:4]
    client_local = client_phone_number[5:13]

    write_xml_field("ClientPhoneNumber",'Phone',client_local)
    write_xml_field("ClientAreaCode",'AC',client_area_code)

    client_alt_phone_number=row['Client Alternate Telephone Number']
    client_alt_area_code = client_alt_phone_number[1:4]
    client_alt_local = client_alt_phone_number[5:13]

    write_xml_field("ClientAltPhoneNumber",'Phone 2',client_alt_local)
    write_xml_field("ClientAltAreaCode",'AC 2',client_alt_area_code)


    client_number = row["Client Number"]

    account_letters=letters_dict[client_number]

	#if the client has an account open, have it checked in in the NCAF.
	#some of the form fields don't match their names.
    #for example, if a client as a -X account, the "Y"	 field must be checked in the NCAF, which will
	#display as "X".
	
    def write_on(letterfield):

        translate_letters = {'Z':'O', 'Y':'Z', 'W':'6','T':'W','S':'7','R':'8',
                         'P':'R','N':'9','J':'N','X':'Y'}
        if letterfield in translate_letters.keys():
            letterfield=translate_letters[letterfield]

        write_xml_field("AccountType{0}".format(letterfield),letterfield,"Yes")

    for letter in account_letters:
        write_on(letter)

    subelement=ET.SubElement(fields,"Adresse", {xfdf_original :   "Adresse"})
    address_1=address_lookup[client_number]["Account Address Line 1"]
    subelement.text=address_1



    address_2 = address_lookup[client_number]["Account Address Line 2"]

    try:
        postal = address_2[-7:]
        write_xml_field("PostalCode1","Code postal",postal)

        #strip of postal code of 7 digits
        rest = address_2[0:-7]
        rest=rest.strip()  #whitespace

        mm=re.match("(.*) (.*)",rest)
        (city,province)=mm.group(1,2)

        write_xml_field("Province1","Prov",province)

        write_xml_field("City1","Ville",city)

    except:
        #ignore errors on address line 2, skip address line 3
        pass



    output_filename = "{0}.xml".format(row['Client Number'])
    tree = ET.ElementTree(fields)
    tree.write(output_filename)

import csv

from string import ascii_uppercase
from itertools import groupby

#from the name and address file, we figure out the letters of accounts that need to be updated
#along with the address info.
with open(infile_address,"r" ) as csvaddress:
    address_reader= csv.DictReader(csvaddress, delimiter=',', quotechar='"')
    address_reader.fieldnames[0]="Account Number" #fix first field name
    pairs=[]
    account_letters=[]
    for address_row in address_reader:
        account_number = address_row["Account Number"]  #the first column name is munged by python
        client_number = account_number[0:6]
        account_letter = account_number[6:7]
        pairs.append( (client_number,address_row))
        account_letters.append( (client_number,account_letter))
    address_lookup = dict(pairs)#gets rid of duplicates

    grouped_letters=[]
    for (key,group) in groupby(account_letters, lambda x : x[0]):
        vals = set([v for (k,v) in group])
        grouped_letters.append((key,vals))

    grouped_letters_dict=dict(grouped_letters)

with open(infile_kyc, newline='') as csvfile:
    file_reader =  csv.DictReader(csvfile, delimiter=',', quotechar='"')
    account_number = address_row["Account Number"]  # the first column name is munged by python
    client_reader = select_unique_clients(file_reader)
    for c in client_reader:
            row_to_xml(c,grouped_letters_dict)