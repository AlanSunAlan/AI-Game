#! /usr/bin/env python3

from selenium import webdriver
import time

browser = webdriver.Firefox() # Get local session of firefox
browser.get("file:///home/alan/developing/AI_Game/dist/index.html") # Load page

browser.maximize_window()