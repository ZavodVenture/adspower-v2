import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from random import choice


def do_shit(discord_id, validator_address, capacity, activities, website, validator_endpoint, storage_ip, storage_kv_ip, contributions, applications, social_media, bugs, interested, feedback):
    driver = webdriver.Chrome()

    try:
        driver.maximize_window()
    except:
        pass

    driver.get('https://docs.google.com/forms/d/e/1FAIpQLScsa1lpn43F7XAydVlKK_ItLGOkuz2fBmQaZjecDn76kysQsw/viewform?ts=6617a343')

    discordId_input = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    validatorAddress_input = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    capacity_input = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    otherActivities_input = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div[2]/textarea')))
    website_input = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    validatorEndpoint_input = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    storageIp_input = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    storageKvIp_input = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    contibutions_input = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[11]/div/div/div[2]/div/div[1]/div[2]/textarea')))
    applications_input = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[12]/div/div/div[2]/div/div[1]/div[2]/textarea')))
    socialMedia_input = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[13]/div/div/div[2]/div/div[1]/div[2]/textarea')))
    bugs_input = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[14]/div/div/div[2]/div/div[1]/div[2]/textarea')))
    interested_yes = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[15]/div/div/div[2]/div[1]/div/span/div/div[1]/label/div/div[1]/div/div[3]/div')))
    interested_no = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[15]/div/div/div[2]/div[1]/div/span/div/div[2]/label/div/div[1]/div/div[3]/div')))
    feedback_input = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[16]/div/div/div[2]/div/div[1]/div[2]/textarea')))
    continue_button = WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')))

    if discord_id:
        discordId_input.send_keys(discord_id)
    if validator_address:
        validatorAddress_input.send_keys(validator_address)
    if capacity:
        capacity_input.send_keys(capacity)
    if activities:
        otherActivities_input.send_keys(activities)
    if website:
        website_input.send_keys(website)
    if validator_endpoint:
        validatorEndpoint_input.send_keys(validator_endpoint)
    if storage_ip:
        storageIp_input.send_keys(storage_ip)
    if storage_kv_ip:
        storageKvIp_input.send_keys(storage_kv_ip)
    if contributions:
        contibutions_input.send_keys(contributions)
    if applications:
        applications_input.send_keys(applications)
    if social_media:
        socialMedia_input.send_keys(social_media)
    if bugs:
        bugs_input.send_keys(bugs)

    if interested:
        interested_yes.click()
    else:
        interested_no.click()

    if feedback:
        feedback_input.send_keys(feedback)

    continue_button.click()

    WebDriverWait(driver, 15).until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')))
    time.sleep(1.5)


def main():
    data = open('data.txt').read().split('\n')
    if not data[-1]:
        data = data[:-1]

    sleep_from = 1600
    sleep_to = 2200

    for s in data:
        shit_data = s.split('||')

        try:
            do_shit(*shit_data)
        except:
            print(f'Не удалось для {shit_data[0]}')
        else:
            print(f'Выполнено для {shit_data[0]}')
        finally:
            s_time = random.randint(sleep_from, sleep_to)
            print(f'Спим {s_time}')
            time.sleep(s_time)


if __name__ == '__main__':
    main()
