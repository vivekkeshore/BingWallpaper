import re
import os
import json
import requests
from urllib import request
from urllib import error as urllib_error


URL = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"


def check_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def set_wallpaper(file_path, image_desc):
    command = 'gsettings set org.gnome.desktop.background picture-uri file://'+file_path
    os.system(command)
    notify = 'notify-send -u critical "Wallpaper for the Day updated!" "' + image_desc + '"'
    os.system(notify)


def download_bing_wallpaper():
    try:
        image_data = json.loads(requests.get(URL).text)
        image_url = 'http://www.bing.com' + image_data['images'][0]['url']

        # url for better quality image
        image_download_url = 'http://www.bing.com/hpwp/' + image_data['images'][0]['hsh']
        image_name = image_url[re.search("rb/", image_url).end():re.search('_EN', image_url).start()] + '.jpg'

        dir_path = os.environ['HOME'] + '/Pictures/Bing_Pic_of_the_Day/'
        file_path = dir_path + image_name
        check_dir(dir_path)

        if not os.path.isfile(file_path):
            try:
                # try downloading by first url(better quality)
                request.urlretrieve(image_download_url, filename=file_path)
            except urllib_error.HTTPError:
                # if first url fails
                request.urlretrieve(image_url, filename=file_path)
            image_desc = image_data['images'][0]['copyright']
            set_wallpaper(file_path, image_desc)

        else:
            # wallpaper alredy updated!!
            notify = 'notify-send -u critical "Bing Wallpaper" ' \
                     '"Wallpaper for the day has been updated already!"'
            os.system(notify)

    except:
        # If no network connection or sometinh wrong occurs....Who cares ??
        notify = 'notify-send -u critical "Bing Wallpaper" ' \
                 '"Wallpaper can\'t be updated!"'
        os.system(notify)


if __name__ == '__main__':
    download_bing_wallpaper()
