# ============================================================
# STEP 3: MEANINGFUL LOGGING ADDED
# InstaStore_with_logging.py
# ============================================================
# LOGGING ADDED:
# - Logs to both console AND a file: instastore.log
# - Uses correct log levels: info, warning, error, exception
# - Includes context (URL, filename, username) in log messages
# - logger.exception() captures full stack traces on errors
# ============================================================

from datetime import datetime
from tqdm import tqdm
import requests
import re
import sys
import instaloader
import logging

# ---- Logging Setup ----
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("instastore.log"),   # saves all logs to file
        logging.StreamHandler()                  # also prints to console
    ]
)
logger = logging.getLogger(__name__)


def internet(url='https://www.google.com/', timeout=5):
    try:
        req = requests.get(url, timeout=timeout)
        req.raise_for_status()
        logger.info("Internet connection verified successfully.")
        return True
    except requests.HTTPError as e:
        logger.error("Internet check failed with HTTP status %s.", e.response.status_code)
    except requests.ConnectionError:
        logger.error("No internet connection available. Cannot proceed.")
    return False


def download_photo():
    url = input("\nPlease enter your desired Image URL: \n")
    logger.info("User requested photo download from URL: %s", url)

    x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)
    if not x:
        logger.warning("URL rejected — not an Instagram URL: %s", url)
        print("Entered URL is not an instagram.com URL.")
        return

    try:
        logger.info("Fetching page content from URL.")
        request_image = requests.get(url, timeout=10)
        request_image.raise_for_status()
        src = request_image.content.decode('utf-8')

        check_type = re.search(r'<meta name="medium" content=[\'"]?([^\'" >]+)', src)
        if not check_type:
            logger.warning("Could not determine content type from page at URL: %s", url)
            print("Could not determine content type. The page structure may have changed.")
            return

        final = re.sub('<meta name="medium" content="', '', check_type.group())

        if final == "image":
            logger.info("Content type confirmed as image. Starting download.")
            extract_image_link = re.search(r'meta property="og:image" content=[\'"]?([^\'" >]+)', src)
            if not extract_image_link:
                logger.warning("Could not extract image link from page.")
                print("Could not extract image link from page.")
                return

            image_url = re.sub('meta property="og:image" content="', '', extract_image_link.group())
            file_size_request = requests.get(image_url, stream=True, timeout=10)
            file_size_request.raise_for_status()

            file_size = int(file_size_request.headers.get('Content-Length', 0))
            logger.info("Image file size: %d bytes.", file_size)

            block_size = 1024
            filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
            t = tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
            with open(filename + '.jpg', 'wb') as f:
                for data in file_size_request.iter_content(block_size):
                    t.update(len(data))
                    f.write(data)
            t.close()
            logger.info("Image downloaded successfully. Saved as %s.jpg", filename)
            print("\nImage downloaded successfully!!")
        else:
            logger.warning("URL content type is '%s', not 'image'. Download skipped.", final)
            print("URL does not point to an image.")

    except requests.ConnectionError:
        logger.error("Network error while downloading photo from URL: %s", url)
        print("Network error: Could not connect. Check your internet connection.")
    except requests.Timeout:
        logger.error("Request timed out while accessing URL: %s", url)
        print("Request timed out. Instagram may be slow or unreachable.")
    except requests.HTTPError as e:
        logger.error("HTTP error %s when accessing URL: %s", e.response.status_code, url)
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.reason}")
    except KeyError as e:
        logger.error("Missing expected response header: %s", e)
        print(f"Missing expected data in response headers: {e}")
    except Exception as e:
        logger.exception("Unexpected error in download_photo()")  # logs full traceback
        print(f"An unexpected error occurred: {e}")


def download_video():
    url = input("\nPlease enter your desired Video URL: \n")
    logger.info("User requested video download from URL: %s", url)

    x = re.match(r'^(https:)[/][/]www.([^/]+[.])*instagram.com', url)
    if not x:
        logger.warning("URL rejected — not an Instagram URL: %s", url)
        print("Entered URL is not an instagram.com URL.")
        return

    try:
        logger.info("Fetching page content from URL.")
        request_image = requests.get(url, timeout=10)
        request_image.raise_for_status()
        src = request_image.content.decode('utf-8')

        check_type = re.search(r'<meta name="medium" content=[\'"]?([^\'" >]+)', src)
        if not check_type:
            logger.warning("Could not determine content type from page at URL: %s", url)
            print("Could not determine content type. The page structure may have changed.")
            return

        final = re.sub('<meta name="medium" content="', '', check_type.group())

        if final == "video":
            logger.info("Content type confirmed as video. Starting download.")
            extract_video_link = re.search(r'meta property="og:video" content=[\'"]?([^\'" >]+)', src)
            if not extract_video_link:
                logger.warning("Could not extract video link from page.")
                print("Could not extract video link from page.")
                return

            video_url = re.sub('meta property="og:video" content="', '', extract_video_link.group())
            file_size_request = requests.get(video_url, stream=True, timeout=10)
            file_size_request.raise_for_status()

            file_size = int(file_size_request.headers.get('Content-Length', 0))
            logger.info("Video file size: %d bytes.", file_size)

            block_size = 1024
            filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
            t = tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
            with open(filename + '.mp4', 'wb') as f:
                for data in file_size_request.iter_content(block_size):
                    t.update(len(data))
                    f.write(data)
            t.close()
            logger.info("Video downloaded successfully. Saved as %s.mp4", filename)
            print("\nVideo downloaded successfully!!")
        else:
            logger.warning("URL content type is '%s', not 'video'. Download skipped.", final)
            print("URL does not point to a video.")

    except requests.ConnectionError:
        logger.error("Network error while downloading video from URL: %s", url)
        print("Network error: Could not connect. Check your internet connection.")
    except requests.Timeout:
        logger.error("Request timed out while accessing URL: %s", url)
        print("Request timed out. Instagram may be slow or unreachable.")
    except requests.HTTPError as e:
        logger.error("HTTP error %s when accessing URL: %s", e.response.status_code, url)
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.reason}")
    except KeyError as e:
        logger.error("Missing expected response header: %s", e)
        print(f"Missing expected data in response headers: {e}")
    except Exception as e:
        logger.exception("Unexpected error in download_video()")
        print(f"An unexpected error occurred: {e}")


def download_dp():
    try:
        ig = instaloader.Instaloader()
        user = input("Please enter your Instagram Username: ").strip()
        if not user:
            logger.warning("Empty username entered for profile download.")
            print("Username cannot be empty.")
            return

        logger.info("Attempting to download profile picture for user: %s", user)
        ig.download_profile(user, profile_pic_only=True)
        logger.info("Profile picture downloaded successfully for user: %s", user)
        print("\nProfile Photo downloaded successfully!!")

    except instaloader.exceptions.ProfileNotExistsException:
        logger.error("Profile does not exist: %s", user)
        print(f"Error: The profile '{user}' does not exist.")
    except instaloader.exceptions.PrivateProfileNotFollowedException:
        logger.warning("Attempted to download private profile: %s", user)
        print(f"Error: '{user}' is a private account. You must follow them first.")
    except Exception as e:
        logger.exception("Unexpected error in download_dp() for user: %s", user)
        print(f"Failed to download profile picture: {e}")


if internet():
    logger.info("Application started.")
    try:
        while True:
            print("Press 'A' to download Photo, 'B' for Video, 'C' for Profile Picture, 'E' to Exit.")
            select = input("\nINSTA DOWNLOADER --> ").strip().upper()
            logger.info("User selected option: %s", select)

            if select == 'A':
                download_photo()
            elif select == 'B':
                download_video()
            elif select == 'C':
                download_dp()
            elif select == 'E':
                logger.info("User exited the application.")
                print("\nThanks for visiting! Goodbye.")
                sys.exit()
            else:
                logger.warning("Invalid menu option entered: %s", select)
                print("Invalid option. Please press A, B, C, or E.")
    except KeyboardInterrupt:
        logger.warning("Application interrupted by user (KeyboardInterrupt).")
        print("\nProgramme Interrupted")
else:
    logger.critical("No internet connection. Application cannot start.")
    sys.exit()
