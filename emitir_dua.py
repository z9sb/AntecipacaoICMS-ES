from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import time, sleep

class Dua:
    def send_delayed_keys(self, element, text, delay=0.3):
            for c in text:
                endtime = time() + delay
                element.send_keys(c)
                sleep(endtime - time())

    def emitir_dua_sefaz(self, imposto, cnpj, n_nf, n_for):
            data = datetime.now()
            month = data.month
            year = data.year

            if month == 0:
                month = 12
                year = year -1

            nav = webdriver.Chrome(service= Service(
                ChromeDriverManager().install()), options= webdriver.ChromeOptions())
            nav.get("https://internet.sefaz.es.gov.br/agenciavirtual/area_publica/e-dua/icms.php")
            nav.find_element(
                                By.XPATH ,"/html/body/div[3]/div[2]/div[2]/fieldset/form/table/tbody/tr[2]/td[2]/select").click()
            nav.find_element(
                                By.XPATH ,"/html/body/div[3]/div[2]/div[2]/fieldset/form/table/tbody/tr[2]/td[2]/select/option[13]").click()
            nav.find_element(
                                By.XPATH ,"/html/body/div[3]/div[2]/div[2]/fieldset/form/table/tbody/tr[3]/td[2]/input").click()
            nav.find_element(
                                By.XPATH ,"/html/body/div[3]/div[2]/div[2]/fieldset/form/table/tbody/tr[3]/td[2]/input").send_keys(
                                    f"{month:02}/{year}"
                                )
            nav.find_element(
                                By.XPATH ,"/html/body/div[3]/div[2]/div[2]/fieldset/form/table/tbody/tr[5]/td[2]/input").click()
            nav.find_element(
                                By.XPATH ,"/html/body/div[3]/div[2]/div[2]/fieldset/form/table/tbody/tr[5]/td[2]/input").send_keys(
                                    f"{imposto}"
                                )
            g = nav.find_element(
                                By.XPATH ,"/html/body/div[3]/div[2]/div[2]/fieldset/form/table/tbody/tr[1]/td[2]/input")
            
            self.send_delayed_keys(g,cnpj, 0.3)
            
            nav.find_element(
                                By.XPATH ,"/html/body/div[3]/div[2]/div[2]/fieldset/form/table/tbody/tr[7]/td[2]/input").send_keys(
                                    f"REF. NF N°{n_nf} {str(n_for)}"
                                )
            nav.find_element(
                                By.XPATH ,"/html/body/div[3]/div[2]/div[2]/fieldset/form/table/tbody/tr[4]/td[2]/input").click()
            nav.find_element(
                                By.XPATH ,"/html/body/div[3]/div[2]/div[2]/fieldset/form/table/tbody/tr[4]/td[2]/input").send_keys(
                                    f"10/{month + 1:02}/{year}")
            
            sleep(300)
            return None