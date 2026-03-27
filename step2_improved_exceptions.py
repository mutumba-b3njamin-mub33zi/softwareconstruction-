# ============================================================
# STEP 2: IMPROVED EXCEPTION STRATEGIES
# InstaStore_improved.py
# ============================================================
# FIXES APPLIED:
# [1] Replaced bare AttributeError with specific, meaningful exceptions
# [2] Added timeout and raise_for_status() to all requests.get() calls
# [3] Used .get() with fallback for Content-Length header
# [4] Added full try/except to download_dp() with instaloader-specific errors
# [5] Fixed main menu logic — replaced if/else chain with proper elif
# ============================================================

from datetime import datetime
from tqdm import tqdm
import requests
import re
import sys
import instaloader


def download_photo():
    url = input("\nPlease enter your desired Image URL: \n")
    x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)

    if not x:
        print("Entered URL is not an instagram.com URL.")
        return  # FIX: return early instead of nesting everything in if x:

    try:
        request_image = requests.get(url, timeout=10)   # FIX [2]: added timeout
        request_image.raise_for_status()                # FIX [2]: catch 4xx/5xx responses
        src = request_image.content.decode('utf-8')

        check_type = re.search(r'<meta name="medium" content=[\'"]?([^\'" >]+)', src)
        if not check_type:                              # FIX [1]: explicit None check
            print("Could not determine content type. The page structure may have changed.")
            return

        final = re.sub('<meta name="medium" content="', '', check_type.group())

        if final == "image":
            print("\nDownloading the image...")
            extract_image_link = re.search(r'meta property="og:image" content=[\'"]?([^\'" >]+)', src)
            if not extract_image_link:                  # FIX [1]: explicit None check
                print("Could not extract image link from page.")
                return

            image_url = re.sub('meta property="og:image" content="', '', extract_image_link.group())
            file_size_request = requests.get(image_url, stream=True, timeout=10)  # FIX [2]
            file_size_request.raise_for_status()

            file_size = int(file_size_request.headers.get('Content-Length', 0))  # FIX [3]: safe fallback to 0
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
            print("URL does not point to an image.")

    except requests.ConnectionError:                    # FIX [1]: specific network error
        print("Network error: Could not connect. Check your internet connection.")
    except requests.Timeout:                            # FIX [1]: specific timeout error
        print("Request timed out. Instagram may be slow or unreachable.")
    except requests.HTTPError as e:                     # FIX [1]: specific HTTP error
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.reason}")
    except KeyError as e:                               # FIX [3]: catch missing headers
        print(f"Missing expected data in response headers: {e}")
    except Exception as e:                              # FIX [1]: catch-all as last resort
        print(f"An unexpected error occurred: {e}")


def download_video():
    url = input("\nPlease enter your desired Video URL: \n")
    x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)

    if not x:
        print("Entered URL is not an instagram.com URL.")
        return

    try:
        request_image = requests.get(url, timeout=10)   # FIX [2]
        request_image.raise_for_status()
        src = request_image.content.decode('utf-8')

        check_type = re.search(r'<meta name="medium" content=[\'"]?([^\'" >]+)', src)
        if not check_type:
            print("Could not determine content type. The page structure may have changed.")
            return

        final = re.sub('<meta name="medium" content="', '', check_type.group())

        if final == "video":
            print("\nDownloading the video...")
            extract_video_link = re.search(r'meta property="og:video" content=[\'"]?([^\'" >]+)', src)
            if not extract_video_link:
                print("Could not extract video link from page.")
                return

            video_url = re.sub('meta property="og:video" content="', '', extract_video_link.group())
            file_size_request = requests.get(video_url, stream=True, timeout=10)  # FIX [2]
            file_size_request.raise_for_status()

            file_size = int(file_size_request.headers.get('Content-Length', 0))  # FIX [3]
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
            print("URL does not point to a video.")

    except requests.ConnectionError:
        print("Network error: Could not connect. Check your internet connection.")
    except requests.Timeout:
        print("Request timed out. Instagram may be slow or unreachable.")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.reason}")
    except KeyError as e:
        print(f"Missing expected data in response headers: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def download_dp():
    try:                                                # FIX [4]: added full try/except
        ig = instaloader.Instaloader()
        user = input("Please enter your Instagram Username: ").strip()
        if not user:                                    # FIX [4]: validate empty input
            print("Username cannot be empty.")
            return
        ig.download_profile(user, profile_pic_only=True)
        print("\nProfile Photo downloaded successfully!!")

    except instaloader.exceptions.ProfileNotExistsException:   # FIX [4]: specific error
        print(f"Error: The profile '{user}' does not exist.")
    except instaloader.exceptions.PrivateProfileNotFollowedException:  # FIX [4]
        print(f"Error: '{user}' is a private account. You must follow them first.")
    except Exception as e:                              # FIX [4]: catch-all fallback
        print(f"Failed to download profile picture: {e}")


# FIX [5]: Replaced broken if/else chain with proper if/elif/else
while True:
    print("Press 'A' to download Photo, 'B' for Video, 'C' for Profile Picture, 'E' to Exit.")
    select = input("\nINSTA DOWNLOADER --> ").strip().upper()

    if select == 'A':
        download_photo()
    elif select == 'B':
        download_video()
    elif select == 'C':
        download_dp()
    elif select == 'E':
        print("\nThanks for visiting! Goodbye.")
        sys.exit()
    else:
        print("Invalid option. Please press A, B, C, or E.")  # FIX [5]: no longer exits
