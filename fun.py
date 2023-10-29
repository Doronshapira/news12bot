import time

# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
def chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1200x600')
    return chrome_options


def get_media_type(media_item):
    # Check if the media item is a video
    if media_item and 'mc-content-media-item_video' in media_item['class']:
        return 'Video'

    # Check if the media item is an image
    elif media_item and 'mc-content-media-item_picture' in media_item['class']:
        return 'Photo'

    # Return null if no media item or unknown type
    return None


# Create a dictionary to store the results

def extract_info(soup):
    # Extracting msg_id
    msg_id = soup['data-msg-id']

    # Extracting reporter name
    reporter_name = soup.find('p', class_='mc-message-header__name').text.strip()

    # Extracting message
    message = soup.find('div', class_='mc-extendable-text__content')
    if message:
        message = message.text.strip()
    else:
        message = None
    media_item = soup.find('div', class_='mc-content-media-item')
    media=get_media_type(media_item)
    if media =='Photo':
        media_url = media_item['style'].split('("')[1].split('")')[0]
    elif media == 'Video':
        url=media_item['style'].split('("')[1].split('")')[0]
        to_add=url.split('telegram')[-1].replace('thumb','video').replace('jpg','mp4')
        media_url='https://makostorepdl-a.akamaihd.net/telegram'+to_add
    else:
        media_url = None
    # Extracting message time
    message_time = soup.find('p', class_='mc-message-footer__time').text.strip()

    return {msg_id: {'Reporter Name': reporter_name, 'Message': message, 'Media Type':media,'Media URL': media_url, 'Time': message_time}}



def initilize_bot():
    output_dict = {}
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get('https://www.n12.co.il/')
    x = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'mc-drawer__btn')))
    x.click()
    html_code = driver.page_source
    # Parse the HTML code
    soup = BeautifulSoup(html_code, 'html.parser')
    # Find all the message wraps
    message_wraps = soup.find_all('div', class_='mc-message-wrap')
    # Process each message wrap and store the results in the array
    for message_wrap in message_wraps:
        result = extract_info(message_wrap)
        output_dict.update(result)
    return output_dict
