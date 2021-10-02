import os
import sys
import six
import platform
import argparse
import logging.config
import re
import time
import random
import json
import pandas as pd
import numpy as np
import scipy.interpolate as si
import datetime
import asyncio
import requests
import keyboard
import csv
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from selenium.webdriver.common.action_chains import ActionChains
from random_user_agent.user_agent import UserAgent as UA
from random_user_agent.params import SoftwareName, OperatingSystem
from timeit import default_timer as timer


#Run single instance of a web driver dming everyone in a given channel
def run_single_instance(channel_url='https://discord.com/channels/888593181132865576/888593181132865579', username='advaith101@gmail.com', password='Arstycoon$1998'):
    time_elapsed = timer()
    message = 'testing'

    #setup user agent
    options = webdriver.ChromeOptions()
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UA(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    # print('\n')
    # print(user_agent)
    options.add_argument(f'user-agent={user_agent}')

    #start web driver and navigate to channel page
    LOGGER = logging.getLogger()
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(channel_url)
    except Exception as e:
        print(e)
        driver.close()
        sys.exit("Unable to connect to URL - Check internet and proxy")

    ac = ActionChains(driver)
    ac.send_keys(username)
    ac.send_keys(Keys.TAB)
    time.sleep(1)
    ac.send_keys(password)
    ac.send_keys(Keys.TAB)
    time.sleep(1)
    ac.send_keys(Keys.TAB)
    ac.send_keys(Keys.RETURN)
    ac.perform()
    
    # pause = input('Press Enter once ads are gone')
    time.sleep(5)

    members = driver.find_elements_by_xpath("//div[starts-with(@class, 'member-')]")
    num_members = len(members)
    time.sleep(1)
    for i in range(1, num_members):
        time.sleep(1)
        ac = ActionChains(driver)
        ac.move_to_element(members[i]).click()
        ac.perform()
        time.sleep(1)
        for i in range(len(message)):
            ac = ActionChains(driver)
            ac.send_keys(message[i])
            ac.perform()
            time.sleep(.07)
        ac = ActionChains(driver)
        ac.send_keys(Keys.RETURN)
        ac.perform()
        time.sleep(1)
        driver.back()
        members = driver.find_elements_by_xpath("//div[starts-with(@class, 'member-')]")



if __name__ == '__main__':
    run_single_instance()




