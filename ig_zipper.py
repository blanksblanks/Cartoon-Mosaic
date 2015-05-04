import requests
import json
import sys
import urllib2
import os
import zipfile


'''
Makes Requests to Instagram API
Takes 2 command line arguments

argv1 = gallery_name
argv2 = access_token

stores thumbnail sized images in handle_response()
'''
gallery_name = sys.argv[1]
access_token = sys.argv[2]

def fetch_user_id():
    user_url = 'https://api.instagram.com/v1/users/search?q=%s&access_token=%s' %(gallery_name, access_token)

    make_request(user_url, None)

def start_instagram_requests(parsed_request):
    BASE_URL = 'https://api.instagram.com/v1/users/'
    user_id = parsed_request['data'][0]['id']

    initial_request = '%s%s/media/recent?access_token=%s' %(BASE_URL, user_id, access_token)
    make_request(initial_request, gallery_name)

'''
Python requests
'''
def make_request(request_url, gallery_name):
    raw_request = requests.get(request_url)
    parsed_request = json.loads(raw_request.text)

    if gallery_name == None:
        start_instagram_requests(parsed_request)
    else:
        handle_response(parsed_request, gallery_name)

def handle_response(parsed_request, gallery_name):
    for item in range(len(parsed_request['data'])):
        content = parsed_request['data'][item]
        image_key = content['created_time']

        imagePath = content['images']['thumbnail']['url']
        print image_key

        if imagePath:
            store_images_locally(gallery_name, image_key, imagePath)

    if parsed_request['pagination'] and parsed_request['pagination']['next_url']:
        request_url = parsed_request['pagination']['next_url']
        make_request(request_url, gallery_name) # get next page of content
    else:
        zip_folder(gallery_name) # generate zip folder

def store_images_locally(directory, filename, imagePath):
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = open(directory + '/' + filename + '.png', 'wb')
    f.write(urllib2.urlopen(imagePath).read())
    f.close()

'''
Functions to create zip folder locally
Folder/Zip name are created by gallery_name
'''
def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

def zip_folder(directory):
    zipf = zipfile.ZipFile(directory + '.zip', 'w')
    zipdir(directory, zipf)
    zipf.close()

if __name__ == "__main__":
    fetch_user_id()