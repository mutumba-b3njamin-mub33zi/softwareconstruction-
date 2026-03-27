# ============================================================
# STEP 1: ORIGINAL CODE — POORLY WRITTEN ERROR HANDLING
# InstaStore.py (Original)
# ============================================================
# ISSUES IDENTIFIED:
# [1] Bare except AttributeError — too vague, only catches one type of failure
# [2] No error handling on requests.get() calls — network failures crash the app
# [3] Content-Length header assumed to always exist — KeyError if missing
# [4] download_dp() has zero error handling — any failure crashes the program
# [5] Logic error in main menu — else: sys.exit() exits on ANY valid input
# ============================================================

from datetime import datetime
from tqdm import tqdm
import requests
import re
import sys
import instaloader

def download_photo():
    url = input("\nPlease enter your desired Image URL from your Instagram profile: \n")
    x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)

    try:
        if x:
            request_image = requests.get(url)   # [ISSUE 2] No timeout, no error handling
            src = request_image.content.decode('utf-8')
            check_type = re.search(r'<meta name="medium" content=[\'"]?([^\'" >]+)', src)
            check_type_f = check_type.group()
            final = re.sub('<meta name="medium" content="', '', check_type_f)

            if final == "image":
                print("\nDownloading the image...")
                extract_image_link = re.search(r'meta property="og:image" content=[\'"]?([^\'" >]+)', src)
                image_link = extract_image_link.group()
                final = re.sub('meta property="og:image" content="', '', image_link)
                _response = requests.get(final).content
                file_size_request = requests.get(final, stream=True)
                file_size = int(file_size_request.headers['Content-Length'])  # [ISSUE 3] KeyError if header missing
                block_size = 1024
                filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
                t = tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
                with open(filename + '.jpg', 'wb') as f:
                    for data in file_size_request.iter_content(block_size):
                        t.update(len(data))
                        f.write(data)
                t.close()
                print("\nImage downloaded successfully!!")
        else:
            print("Entered URL is not an instagram.com URL.")
    except AttributeError:  # [ISSUE 1] Too vague — only catches AttributeError
        print("Unknown URL!!")


def download_video():
    url = input("\nPlease enter your desired Video URL from your Instagram profile: \n")
    x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)

    try:
        if x:
            request_image = requests.get(url)   # [ISSUE 2] No timeout, no error handling
            src = request_image.content.decode('utf-8')
            check_type = re.search(r'<meta name="medium" content=[\'"]?([^\'" >]+)', src)
            check_type_f = check_type.group()
            final = re.sub('<meta name="medium" content="', '', check_type_f)

            if final == "video":
                print("\nDownloading the video...")
                extract_video_link = re.search(r'meta property="og:video" content=[\'"]?([^\'" >]+)', src)
                video_link = extract_video_link.group()
                final = re.sub('meta property="og:video" content="', '', video_link)
                _response = requests.get(final).content
                file_size_request = requests.get(final, stream=True)
                file_size = int(file_size_request.headers['Content-Length'])  # [ISSUE 3] KeyError if header missing
                block_size = 1024
                filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
                t = tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
                with open(filename + '.mp4', 'wb') as f:
                    for data in file_size_request.iter_content(block_size):
                        t.update(len(data))
                        f.write(data)
                t.close()
                print("\nVideo downloaded successfully!!")
        else:
            print("Entered URL is not an instagram.com URL.")
    except AttributeError:  # [ISSUE 1] Too vague
        print("Unknown URL!!")


def download_dp():
    # [ISSUE 4] No try/except at all — wrong username or network error crashes everything
    ig = instaloader.Instaloader()
    user = input("Please enter your Instagram Username: ")
    ig.download_profile(user, profile_pic_only=True)
    print("\nProfile Photo downloaded successfully!!")


# [ISSUE 5] Logic error — else: sys.exit() is attached to the last if (select == 'E')
# meaning the program exits even if the user pressed A, B, or C
while True:
    print("Press 'A' to download Photo, 'B' for Video, 'C' for Profile Picture, 'E' to Exit.")
    select = str(input("\nINSTA DOWNLOADER --> "))
    if select == 'A' or select == 'a':
        download_photo()
    if select == 'B' or select == 'b':
        download_video()
    if select == 'C' or select == 'c':
        download_dp()
    if select == 'E' or select == 'e':
        sys.exit()
    else:
        sys.exit()  # [ISSUE 5] BUG: This exits on any input that is not exactly 'E'
