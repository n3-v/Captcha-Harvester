import os
import time
import queue
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from .scripts import(
    Hcaptcha,
    ReCaptchaV2,
    ReCaptchaV3,
    )

from .exceptions import(
    InvalidSolverType,
    InvalidProxyFormat,
    SolveTimeout,
    )

class new:
    def __init__(self, solver_type: str, url: str, site_key: str,action: str = None):

        if "hcaptcha" in solver_type.lower():
            self.script = Hcaptcha(site_key)
        elif "recaptchav2" in solver_type.lower():
            self.script = ReCaptchaV2(site_key)
        elif "recaptchav3" in solver_type.lower():
            self.script = ReCaptchaV3(site_key, action)
        else:
            raise InvalidSolverType()

        self.queue = queue.Queue(maxsize=1)

        options = Options()
        option_args = ["--allow-insecure-localhost", "--ignore-ssl-errors", 
            "--ignore-certificate-errors-spki-list", "--window-size=500,645", 
            "--ignore-certificate-errors", "user-agent=Chrome",
            "--disable-blink-features","--disable-blink-features=AutomationControlled",
            "--disable-extensions", "disable-infobars", "--allow-profiles-outside-user-dir"]
        
        for x in option_args:
            options.add_argument(x)

        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get(url)
        self.driver.execute_script(self.script.template)

        time.sleep(3)

    def solve(self, timeout: float = 100):
        while 1:
            if not self.queue.full():
                self.queue.put('s')
                self.driver.execute_script(self.script.invoke)

                try:
                    resp = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.ID, "captchaResp")))
                except:
                    self.driver.execute_script(self.script.template)
                    raise SolveTimeout()

                time.sleep(1)

                captcha = resp.get_attribute("value")

                self.driver.execute_script(self.script.template)
                self.queue.get()
                return captcha

    def close(self):
        self.driver.close()

