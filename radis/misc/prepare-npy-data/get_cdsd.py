import urllib.request
import re
from zipfile import ZipFile
import os
from io import BytesIO

lower_bound = 1750
upper_bound = 2400

# Set the URL you want to webscrape from
url = "ftp://ftp.iao.ru/pub/CDSD-4000/"
output = "./par/"

if not os.path.exists(output):
    os.mkdir(output)

# Connect to the URL
print("Fetching filelist...")
response = urllib.request.urlopen(url)
fnames = re.findall("\S+.zip", response.read().decode())
for fname in fnames:
    low, high = map(float, re.findall("\d+", fname))
    if high > lower_bound and low < upper_bound:
        if not os.path.exists(output + fname[:-4]):
            print("Downloading " + fname[:-4] + "...", end="")
            fzip = BytesIO(urllib.request.urlopen(url + fname).read())
            ZipFile(fzip).extractall(output)
            print(" Done!"),
        else:
            print(fname[:-4] + " already exists, skipping!")
print("Done!")
