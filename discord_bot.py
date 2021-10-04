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
from selenium.webdriver.common.action_chains import ActionChains
from random_user_agent.user_agent import UserAgent as UA
from random_user_agent.params import SoftwareName, OperatingSystem


#ENTER key config
if platform.system() == 'Darwin':
	enter_key = Keys.RETURN
else:
	enter_key = Keys.ENTER

#Run single instance of a web driver dming everyone in a given channel
def run_single_instance(username, password, channel_url='https://discord.com/channels/888593181132865576/888593181132865579', message='testing'):
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
	driver_path = os.getcwd() + '/chromedriver'
	driver = webdriver.Chrome(options=options, executable_path=driver_path)
	try:
		driver.get(channel_url)
	except Exception as e:
		print(e)
		driver.close()
		sys.exit("Unable to connect to URL - Check internet and proxy")

	#login
	ac = ActionChains(driver)
	ac.send_keys(username)
	ac.send_keys(Keys.TAB)
	time.sleep(1)
	ac.send_keys(password)
	ac.send_keys(Keys.TAB)
	time.sleep(1)
	ac.send_keys(Keys.TAB)
	ac.send_keys(enter_key)
	ac.perform()
	input('\n\nPress any button after captcha (after you are logged in)')
	
	kill_popups(driver)

	#start DMing members
	members = None
	try:
		members = WebDriverWait(driver, 7).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[starts-with(@class, 'member-')]")))
	except:
		print("\n\nUnable to find members.. trying again")
		sys.exit(0)
	
	scroll_val = 2
	member_index = 1
	for i in range(1, 1000):
		try:
			for k in range(scroll_val):
				time.sleep(.5)
				members = WebDriverWait(driver, 7).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[starts-with(@class, 'member-')]")))
				try:
					elem = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f"//div[starts-with(@class, 'member-')][{len(members)}]")))
					ac = ActionChains(driver)
					ac.move_to_element(elem).click()
					ac.perform()
				except:
					continue
			members = WebDriverWait(driver, 7).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[starts-with(@class, 'member-')]")))

			rand = np.random.randint(low=1000, high=2500)/1000
			time.sleep(rand)
			success = False
			for j in range(3):
				try:
					rand2 = np.random.randint(low=0, high=len(members)) + 1
					elem = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f"//div[starts-with(@class, 'member-')][{min(rand2, len(members))}]")))
					ac = ActionChains(driver)
					ac.move_to_element(elem).click()
					ac.perform()
					success = True
					break
				except:
					continue

			if success:
				rand = np.random.randint(low=700, high=1500)/1500
				time.sleep(rand)
				type_message(message, driver)
				rand = np.random.randint(low=700, high=1500)/1500
				time.sleep(rand)
				driver.back()
			else:
				scroll_val += 1
				continue
			
			member_index += 1
		except:
			driver.refresh()
			kill_popups(driver)
			member_index = 1
			continue
		if i % 8 == 0:
			member_index = 1
			scroll_val += 1


#kill any popups
def kill_popups(driver):
	time.sleep(1)
	ac = ActionChains(driver)
	ac.send_keys(Keys.ESCAPE)
	ac.perform()
	time.sleep(1)
	ac = ActionChains(driver)
	ac.send_keys(Keys.ESCAPE)
	ac.perform()
	time.sleep(1)
	ac = ActionChains(driver)
	ac.send_keys(Keys.ESCAPE)
	ac.perform()
	time.sleep(5)


def type_message(msg, driver):
	paras = msg.split('\n\n')
	for i in range(len(paras)):
		words = paras[i].split(' ')
		for word in words:
			for letter in word:
				ac = ActionChains(driver)
				ac.send_keys(letter)
				ac.perform()
				rand = np.random.randint(low=4, high=10)/5000
				time.sleep(rand)
			ac = ActionChains(driver)
			ac.send_keys(Keys.SPACE)
			ac.perform()
			rand = np.random.randint(low=60, high=140)/4000
			time.sleep(rand)
		ac = ActionChains(driver)
		ac.send_keys(enter_key)
		ac.perform()
		rand = np.random.randint(low=1000, high=2500)/1000
		time.sleep(rand)



if __name__ == '__main__':

	start_time = time.localtime()
	start_time = time.strftime("%H:%M:%S", start_time)
	print("\n\nDiscobot Initializing...")
	print(f"Bot Start Time: {start_time}")

	with open('./message.txt') as f:
		message = f.read()

	if (os.path.isfile('./config.json')):
		use_config = input("\n\nSaved configurations detected. Do you wish to use your saved account info? (y/n) ")
		if use_config.lower().strip() == 'y':
			f = open('./config.json',)
			config = json.load(f)
			username = config['username']
			password = config['password']
			channel_url = input("\n\nEnter the channel url of the discord server you wish to Mass DM\n(e.g. https://discord.com/channels/888593181132865576/888593181132865579)\n\n")
			run_single_instance(channel_url=channel_url, username=username, password=password, message=message)
		else:
			channel_url = input("\n\nEnter the channel url of the discord server you wish to Mass DM\n(e.g. https://discord.com/channels/888593181132865576/888593181132865579)\n\n")
			username = input("\n\nEnter your username (e.g. calm_dentist@gmail.com): ")
			password = input("\n\nEnter your password: ")
			save_config = input("\n\nDo you want to save your username and passord? (y/n): ")
			if save_config.lower().strip() == 'y':
				config = {
					'username': username,
					'password': password
				}
				with open('./config.json', 'w', encoding='utf-8') as f:
					json.dump(config, f, ensure_ascii=False, indent=4)
			run_single_instance(channel_url=channel_url, username=username, password=password, message=message)
	else:
		channel_url = input("\n\nEnter the channel url of the discord server you wish to Mass DM\n(e.g. https://discord.com/channels/888593181132865576/888593181132865579)\n\n")
		username = input("\n\nEnter your username (e.g. calm_dentist@gmail.com): ")
		password = input("\n\nEnter your password: ")
		save_config = input("\n\nDo you want to save your username and passord? (y/n): ")
		if save_config.lower().strip() == 'y':
			config = {
				'username': username,
				'password': password
			}
			with open('./config.json', 'w', encoding='utf-8') as f:
				json.dump(config, f, ensure_ascii=False, indent=4)
		run_single_instance(channel_url=channel_url, username=username, password=password, message=message)

	end_time = time.localtime()
	end_time = time.strftime("%H:%M:%S", end_time)
	print("\n\nTask(s) Complete.")
	print(f"Bot End Time: {end_time}\n\n")





