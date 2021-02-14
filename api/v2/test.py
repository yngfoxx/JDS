import sys
import argparse
import requests as req

# test URL: https://www.bing.com/th?id=OIP.1L3zMoMScZvtQ9VLhf4MRgHaLH&w=200&h=300&c=8&o=5&pid=1.7

parser = argparse.ArgumentParser(prog='grab', description='download contents from internet using Python')
parser.add_argument('-u', '--url', type=str, required=True, help='The URL of the target file')
args = parser.parse_args()

res = req.get(args.url, stream=True)

data = ''

for chunk in res.iter_content(chunk_size=1024):
    if (chunk):
        data += chunk

open('file.jpg','wb').write(data)
