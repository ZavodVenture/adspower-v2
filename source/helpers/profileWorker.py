from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from time import sleep
from random import choices
from string import ascii_letters
from sys import exc_info


class WorkerException(Exception):
    ...


class Worker:
    metamask_id = None

    def __init__(self, ws, driver_path, seed, password=None):
        self.seed = seed
        self.password = password if password else ''.join(choices(ascii_letters, k=15))

        options = Options()
        options.add_experimental_option('debuggerAddress', ws)
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        try:
            self.driver.maximize_window()
        except:
            pass

    def close_all_tabs(self):
        self.driver.switch_to.new_window()
        windows = self.driver.window_handles
        current = self.driver.current_window_handle
        windows.remove(current)
        for window in windows:
            self.driver.switch_to.window(window)
            self.driver.close()
        self.driver.switch_to.window(current)

    def get_extensions(self):
        self.driver.get('chrome://extensions/')

        script = '''ext_manager = document.getElementsByTagName('extensions-manager')[0].shadowRoot;
        item_list = ext_manager.getElementById('items-list').shadowRoot;
        container = item_list.getElementById('container');
        extension_list = container.getElementsByClassName('items-container')[1].getElementsByTagName('extensions-item');

        var extensions = {};

        for (i = 0; i < extension_list.length; i++) {
            console.log(extension_list[i]);
            name = extension_list[i].shadowRoot.getElementById('name').textContent;
            id = extension_list[i].id;
            extensions[name] = id;
        }

        return extensions;'''

        return self.driver.execute_script(script)

    def get_metamask_status(self):
        extensions = self.get_extensions()
        metamask_id = extensions.get('MetaMask')
        if not metamask_id:
            raise Exception('MetaMask Extension not found')

        self.metamask_id = metamask_id

        self.driver.get(f'chrome-extension://{metamask_id}/home.html')
        try:
            WebDriverWait(self.driver, 10).until(ec.url_changes(f'chrome-extension://{metamask_id}/home.html'))
        except TimeoutException:
            self.driver.get('about:blank')
            return 'unlocked'

        current_url = self.driver.current_url

        if 'unlock' in current_url:
            return 'locked'
        elif 'onboarding' in current_url:
            return 'new'
        else:
            raise Exception('Couldn\'t receive MetaMask state')

    def import_keplr(self):
        try:
            extensions = self.get_extensions()
            keplr_id = extensions.get('Keplr')
            if not keplr_id:
                raise WorkerException('Keplr Extension not found')

            self.driver.get(f'chrome-extension://{keplr_id}/register.html')

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[3]/div[3]/button'))).click()
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div/div[5]/button'))).click()

            sleep(2)

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//div[@class="sc-jQHtVU iEYmkL"]/div[1]//input')))

            seed = self.seed.split(' ')

            if len(seed) != 12:
                raise WorkerException('Couldn\'t import seed into keplr: seed must be 12 words length')

            for i in range(len(seed)):
                self.driver.find_element(By.XPATH, f'//div[@class="sc-jQHtVU iEYmkL"]/div[{i + 1}]//input').send_keys(seed[i])

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div/div/form/div[6]/div/button'))).click()

            sleep(2)

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[1]/div[2]/div/div/input'))).send_keys('Wallet')
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[3]/div[2]/div/div/input'))).send_keys(self.password)
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[5]/div[2]/div/div/input'))).send_keys(self.password)
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[4]/div/div/form/div/div[7]/button'))).click()

            WebDriverWait(self.driver, 60).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div/div/div[9]/div/button'))).click()

            old_tab = self.driver.current_window_handle
            self.driver.switch_to.new_window()
            self.driver.get('about:blank')
            new_tab = self.driver.current_window_handle
            self.driver.switch_to.window(old_tab)

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div[5]/div[1]/button'))).click()
            self.driver.switch_to.window(new_tab)
        except Exception:
            exc_type, exc_value, exc_tb = exc_info()
            raise WorkerException(f'exception at line {exc_tb.tb_lineno}')

    def import_metamask(self):
        try:
            if not self.metamask_id:
                extensions = self.get_extensions()
                self.metamask_id = extensions.get('MetaMask')
                if not self.metamask_id:
                    raise WorkerException('MetaMask Extension not found')

            self.driver.get(f'chrome-extension://{self.metamask_id}/home.html')

            try:
                WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/button'))).click()
            except:
                pass

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="onboarding-terms-checkbox"]'))).click()
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="onboarding-import-wallet"]'))).click()
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="metametrics-no-thanks"]'))).click()

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="import-srp__srp-word-0"]')))

            seed = self.seed.split(' ')

            if len(seed) != 12:
                if len(seed) not in [12, 15, 18, 21, 24]:
                    raise WorkerException(f'Seed has wrong length - {len(seed)}')

                WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//div[@class="dropdown import-srp__number-of-words-dropdown"]'))).click()
                WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, f'//option[@value="{len(seed)}"]'))).click()

            for i in range(len(seed)):
                self.driver.find_element(By.XPATH, f'//input[@data-testid="import-srp__srp-word-{i}"]').send_keys(seed[i])

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="import-srp-confirm"]'))).click()

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="create-password-new"]'))).send_keys(self.password)
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="create-password-confirm"]'))).send_keys(self.password)
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="create-password-terms"]'))).click()
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="create-password-import"]'))).click()

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="onboarding-complete-done"]'))).click()
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-next"]'))).click()
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="pin-extension-done"]'))).click()
            sleep(1)

            self.driver.get('about:blank')
        except Exception:
            exc_type, exc_value, exc_tb = exc_info()
            raise WorkerException(f'exception at line {exc_tb.tb_lineno}')

    def restore_metamask(self):
        try:
            if not self.metamask_id:
                extensions = self.get_extensions()
                self.metamask_id = extensions.get('MetaMask')
                if not self.metamask_id:
                    raise WorkerException('MetaMask Extension not found')

            self.driver.get(f'chrome-extension://{self.metamask_id}/home.html')

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//a[@class="button btn-link unlock-page__link"]'))).click()

            WebDriverWait(self.driver, 15).until(
                ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="import-srp__srp-word-0"]')))

            seed = self.seed.split(' ')

            if len(seed) != 12:
                if len(seed) not in [12, 15, 18, 21, 24]:
                    raise WorkerException(f'Seed has wrong length - {len(seed)}')

                WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//div[@class="dropdown import-srp__number-of-words-dropdown"]'))).click()
                WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, f'//option[@value="{len(seed)}"]'))).click()

            for i in range(len(seed)):
                self.driver.find_element(By.XPATH, f'//input[@data-testid="import-srp__srp-word-{i}"]').send_keys(seed[i])

            url_before = self.driver.current_url

            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="create-vault-password"]'))).send_keys(self.password)
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//input[@data-testid="create-vault-confirm-password"]'))).send_keys(self.password)
            WebDriverWait(self.driver, 15).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-testid="create-new-vault-submit-button"]'))).click()

            WebDriverWait(self.driver, 60).until(ec.url_changes(url_before))

            self.driver.get('about:blank')
        except Exception:
            exc_type, exc_value, exc_tb = exc_info()
            raise WorkerException(f'exception at line {exc_tb.tb_lineno}')