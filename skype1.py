import os
import subprocess
import argparse

from datetime import datetime
from skpy import Skype
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import yagmail
from email.message import EmailMessage
from time import sleep
from dotenv import load_dotenv
import time

load_dotenv()

# Credentials and chatID for Skype
SKYPE_CHAT_ID = os.getenv("SKYPE_CHAT_ID")
SKYPE_USERNAME = os.getenv("SKYPE_USERNAME")
SKYPE_PASSWORD = os.getenv("SKYPE_PASSWORD")
SKYPE_SEND_EVERY = int(os.getenv("SKYPE_SEND_EVERY"))

# Email credentials
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

#Jumia URL
JUMIA_URL=os.getenv("AMAZON_URL")


# Capture screenshots
def capture():
    # Instance headless chrome driver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    # Get Jumia screenshot
    driver.set_window_size(1800, 3400)
    driver.get(JUMIA_URL)
    sleep(2)
    driver.save_screenshot("jumia-screenshot.png")

# Send to skype function
def send2skype(nowdt, sk):
    # Login to skype
    

    # Upload screenshot to group chat
    ch = sk.chats[SKYPE_CHAT_ID]
    msg = ch.sendFile(open("jumia-screenshot.png", "rb"), "jumia-screenshot.png", image=True)  
    print(f"Screenshot sent at {nowdt}")


def send2email(nowdt, yag):
    
    subject="Jumia Screenshot"
    body =nowdt
    attachments = ["jumia-screenshot.png"]
    yag.send(EMAIL_RECIPIENT, subject, body, attachments=attachments)

nowdt=datetime.now()


if __name__ == "__main__":
    sk = Skype(SKYPE_USERNAME, SKYPE_PASSWORD, "token_info.txt") # Authenticate once
    # yag=yagmail.SMTP(EMAIL_SENDER,EMAIL_PASSWORD)
    
    while True:
        # Have try catch to handle authentication
        print(f"Capturing Jumia screenshot at {nowdt.ctime()}")
        capture()
        send2skype(nowdt.ctime(), sk)
        # send2email(nowdt.ctime(), yag)
        time.sleep(3)
    



