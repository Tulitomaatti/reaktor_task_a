import urllib2 as url
import StringIO
import zipfile as zip
import pandas as pd

# Does worldbank offer more interesting datasets? if so, write function to generate urls.
# Possibly just make this a module to fetch datasets by keys such as "SP.POP.TOTL"
# Even better, see if a list of datasets can be fetched nicely. Scope creep?

data_urls = {
    "pop": "http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv",
    "co2": "http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.KT?downloadformat=csv"
}

def fetch_data(url_timeout = 10):

    data_res = {}
    for t in data_urls:
        try:
            res = url.urlopen(data_urls[t], timeout=url_timeout)
            data_res[t] = StringIO.StringIO() # Zipfile lib wants to seek around, urllib response is unseekable.
            data_res[t].write(res.read())
            res.close()
        except url.URLError, err:
            print "Error in opening data source", t, "at", data_urls[t], ".", err.reason

    # Data source seems to actually be a zip file - not CVS
    # Security: Zip bombs? Assume worldbank is a nice source and zipfile a good library.

    data_archives = {}
    data = {}
    metadata = {}

    for t in data_res:
        data_archives[t] = zip.ZipFile(data_res[t], 'r')
        flist = data_archives[t].filelist

        for f in flist:
            # Check: Are these filename assumptions ok?

            if f.filename.find("API_") == 0 and ".csv" in f.filename:
                fp = data_archives[t].open(f.filename, 'r')
                data[t] = pd.read_csv(fp, header=2) # Would 1 be ok for other datasets?
                fp.close()

            elif "Metadata_Country_" in f.filename and ".csv" in f.filename:
                fp = data_archives[t].open(f.filename, 'r')
                metadata[t] = pd.read_csv(fp, header=0)
                fp.close()

    return (data, metadata)


# TODO: Offer data cleaning functions here?