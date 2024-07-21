from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import tkinter as tk
from tkinter import simpledialog

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver

def search_player(driver, player_name):
    url = "https://fmref.com/"
    driver.get(url)
    search_box = driver.find_element(By.CSS_SELECTOR, "input[type='search']")
    search_box.send_keys(player_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

def process_results(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    h2_tags = soup.find_all('h2')
    if len(h2_tags) == 1:
        button = soup.find('button', class_='fm-id')
        if button:
            return button.text.strip()
    else:
        driver.maximize_window()
        return None

def get_user_input():
    root = tk.Tk()
    root.withdraw()
    user_input = simpledialog.askstring(title="Multiple Results",
                                        prompt="Multiple results found. Please copy and paste the correct ID:")
    root.destroy()
    return user_input

def main():
    player_name = input("Enter the player name: ")
    driver = init_driver()
    try:
        search_player(driver, player_name)
        result = process_results(driver)
        if result:
            print(result)
        else:
            user_input = get_user_input()
            if user_input:
                print(user_input)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
