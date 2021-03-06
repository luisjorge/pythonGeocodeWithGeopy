""" python version 2.7
# require geopy, version 1.3.0 or later. Check "geopy.__version__"
# this works with [google, arcgis, openmapquest, nominatim] services
# - these services don't require extra info, like username, APIkey, etc.
# I am adding timeout=5 seconds to avoid timeout error during geocode
# this will produce a new csv file: (original filename)_(servicename)Geocoded.csv

usage note: 1st argument: service name [google, arcgis, openmapquest, nominatim]
usage note: 2nd argument: input CSV file name
usage note: 3rd argument: geocoding address field
usage note: 4th argument: (optional) supplemental geocoding address field
usage note: 5th argument: (optional) supplemental geocoding address field
usage note: 6th argument: (optional) supplemental geocoding address field
usage note: 7th argument: (optional) supplemental geocoding address field

usage examples
python geocode.py arcgis sample_addresses_lr.csv address
python geocode.py nominatim sample_addresses_lr.csv address
python geocode.py google test20.csv StreetAddress City State ZipCode
python geocode.py openmapquest test20.csv StreetAddress City State ZipCode
"""
import sys, os, csv, geopy
# require geopy version 1.3.0. Check "geopy.__version__"

def main():
    # eg: geoloc = geopy.geocoders.ArcGIS() # see geocoders/__init__.py for service names
    geoloc = geopy.get_geocoder_for_service(sys.argv[1])()
    # print(geoloc) 
    inputfname = os.path.splitext(os.path.basename(sys.argv[2]))[0]
    with open(sys.argv[2],'r') as f:
        originalf = csv.reader(f)
        inputf = list(originalf) # convert csv input to list
        totaln = len(inputf)-1
        ffname = inputf[0] # collect names of columns/vars
	# add names for geocoding result vars
        ffname.append('service') # holder for geocoding service name
        ffname.append('geocodeinput')
        ffname.append('geocodedlocation')
        ffname.append('latitude')
        ffname.append('longitude')
	ffname.append('geocodedraw')
        # loop through the list (originally csv), collect info and send to a geocoder
	rownum = 0
	cnterror = 0	
	for row in inputf:
	    if rownum == 0:
		row = ffname # the first row is header/names of columns
	    else:
	        geocodeinput = row[ffname.index(sys.argv[3])] # address field has to be in the first column
		if len(sys.argv) > 4:    # 2nd  optional address field
		    geocodeinput = geocodeinput + ", "+ row[ffname.index(sys.argv[4])]
		if len(sys.argv) > 5:    # 3rd optional address field
		    geocodeinput = geocodeinput + ", "+ row[ffname.index(sys.argv[5])]	        
		if len(sys.argv) > 6:    # 4th optional address field
		    geocodeinput = geocodeinput + ", "+ row[ffname.index(sys.argv[6])]
		if len(sys.argv) > 7:    # 5th optional address field
		    geocodeinput = geocodeinput + ", "+ row[ffname.index(sys.argv[7])]
		row.append(sys.argv[1])  # keep the name of the geocoding service used
	        row.append(geocodeinput) # keep address/location string to be geocoded
		# result is the location object
		try:
		    location = geoloc.geocode(geocodeinput,timeout=1) # try different timeout in second..
		    row.append(location.address.encode('utf-8')) # keep geocoded location
		    row.append(location.latitude)                # keep lat/y
		    row.append(location.longitude)               # keep lon/x
		    row.append(location.raw)                     # keep all location object info (json)
		    print(sys.argv[1]+' geocoding '+str(rownum)+' of '+str(totaln)) # tell the progress..
		except:
		    row.append('')                               # place holder for geocoded location
		    row.append('')                               # place holder lat/y
		    row.append('')                               # place holder lon/x
		    row.append('')                               # place holder location object info (json)
		    print(sys.argv[1]+' geocoding '+str(rownum)+' of '+str(totaln)+' - unsuccessful - most likely time-out')
		    cnterror += 1
		    pass
	    # print('\t'.join(row))
	    rownum += 1
	ratesuccess=(rownum-cnterror-1)/float(totaln)*100
	print('Done! '+str(rownum-cnterror-1)+' cases were successfully geocoded ('+str(ratesuccess)+'% success)')
	# save the result/updated list in CSV format
    	with open(inputfname+'_'+sys.argv[1]+'Geocoded.csv', 'w') as f2:  
	    w = csv.writer(f2, delimiter=',')
	    # w.writeheader()
	    for row in inputf:
	        w.writerow(row)
	file.close

# =============================
if __name__ == '__main__':
  main()

