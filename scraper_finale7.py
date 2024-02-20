from bz2 import decompress
from concurrent.futures import thread
import datetime
import json
from re import S
import re
from subprocess import TimeoutExpired
from threading import Thread
from typing import final
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time

#inserisco window size

PATH = "C:\Program Files (x86)\chromedriver.exe"
s = Service(PATH)


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# To avoid notification popup
options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=s, options=options)


driver.get("https://www.farfetch.com/it/shopping/women/items.aspx")

cookies = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/section/div[2]/button[1]'))
            )
cookies.click()
searchbar = driver.find_element(By.XPATH,'//*[@id="search"]')

type_list = [8] #idice tipologie di borsa, per velocizzare ne ho fatti partire diversi contemporaneamente

for type in type_list:
    action = webdriver.ActionChains(driver)
    borse = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="slice-header"]/div[2]/div/div[2]/div[1]/div/div[1]/div/nav/ul/li[7]/a'))
        ) 
    action.move_to_element(borse).perform()
    type = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="slice-header"]/div[2]/div/div[2]/div[1]/div/div[1]/div/nav/ul/li[7]/div/ul/li[1]/ul/li['+str(type)+']/a'))
    )
    action.move_to_element(type).perform()
    type.click()
    #searchbar.send_keys(elem)
    time.sleep(1)
    #searchbar.send_keys(Keys.RETURN)
    try:
        closeAd = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="newsletter-modal"]/div/button'))
            )
        closeAd.click()
    except:
        pass

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight-1800)")
    action.move_by_offset(0, 100).perform()
    time.sleep(2)
    pages = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="slice-container"]/div[3]/div[2]/div[2]/div/div[2]/div/div[2]'))
    )
    npage = pages.text.split(' ')[2]
    driver.execute_script("window.scrollTo(0,100)")
    time.sleep(1)
    #sposta il mouse di 100px verso il basso
    action.move_by_offset(0, 200).perform()
    for currentpage in range (1,32):
        for i in range(1,94):
            try:
                bag = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,'//*[@id="slice-container"]/div[3]/div[2]/div[2]/div/div[1]/ul/div['+str(i)+']/a'))
                )            
                bag.click()
        
                brand = WebDriverWait(driver, 10).until(            #//*[@id="content"]/div/div[1]/div[2]/div/div/div[2]/div[1]/div/h1/a
                        EC.presence_of_element_located((By.XPATH, '//a[@class = "ltr-jtdb6u-Body-Heading-HeadingBold escdwlz1"]'))
                    )                                            #//*[@id="bannerComponents-Container"]/h1/span[1]/a/span'
                print(brand.text)
                print(str(currentpage)+" - "+str(i))
                bag_type = WebDriverWait(driver, 10).until(        #//*[@id="content"]/div/div[1]/div[2]/div/div/div[1]/div[1]/div/h1/p
                        EC.presence_of_element_located((By.XPATH, '//p[@class = "ltr-13ze6d5-Body e1hhaa0c0"]'))
                    )
                print(bag_type.text)
                
                try:
                    price = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH,'//p[@data-component = "PriceLarge"]'))
                    )
                    priceINT = int((price.text.split(' ',1)[0]).replace(".",""))
                    print(price.text)
                except:
                    price = WebDriverWait(driver, 10).until(      
                        EC.presence_of_element_located((By.XPATH,'//p[@data-component = "PriceFinalLarge"]'))
                    )
                    priceINT = int((price.text.split(' ',1)[0]).replace(".",""))
                    print(price.text + "prezzo scontato")
            
                png = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH,'//*[@id="content"]/div/div[1]/div[1]/div/button[1]/div/img'))
                )
                bag_image = (png.get_attribute('src'))
                #print(png.get_attribute('src'))
                    
                driver.execute_script("window.scrollTo(0,800)")
                try:
                    try:
                        description = WebDriverWait(driver, 10).until( #aggiungi un try execpt ho trovato borse senza descrizione
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="tabpanel-0"]/div/div[1]/div/p'))
                        )                                                  
                        descrizione = description.text
                        print(description.text)
                    except: 
                        description = WebDriverWait(driver, 10).until( #aggiungi un try execpt ho trovato borse senza descrizione
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="tabpanel-0"]/div/div[1]/div/div[2]/p'))
                        )                                                  
                        descrizione = description.text
                        print(description.text)
                except:
                    pass
                   
                #materiali
                materiali = []
                for A in range(1,5): #A counter span in tabpanel
                    try:
                        mat_A = driver.find_element(By.XPATH,'//*[@id="tabpanel-0"]/div/div[2]/div/div[1]/p/span['+str(A)+']')
                        materiali.append(mat_A.text)
                    except:
                        try:
                            for Q in range(1,4): #Q counter p[] in tabpanel
                                mat_A = driver.find_element(By.XPATH,'//*[@id="tabpanel-0"]/div/div[2]/div/div[1]/p['+str(Q)+']/span['+str(A)+']')
                                materiali.append(mat_A.text)
                        except:
                            pass
                try:
                    IDbrand = WebDriverWait(driver, 10).until(      
                        EC.visibility_of_element_located((By.XPATH,'//*[@id="tabpanel-0"]/div/div[2]/div/p/span[2]'))
                    )
                    print("IDbrand: "+IDbrand.text)
                    IDbrandtext = IDbrand.text
                except:
                    print("no id located")
                    IDbrand = "no id located"
                try:    
                    taglie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-1"]/h2')))                
                    taglie_button.click()
                    dimensioni = [ ]
                    try:
                        for s in range(1,6):                                                                        
                            dimensione = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tabpanel-1"]/div/div[2]/div/div/div[2]/table/tbody/tr['+str(s)+']/td[1]')))
                            misura = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tabpanel-1"]/div/div[2]/div/div/div[2]/table/tbody/tr['+str(s)+']/td[2]')))
                            dimensioni.append(dimensione.text +': '+ misura.text) 
                                                         

                    except TimeoutException: 
                        try:
                            for s in range(1,6):                                                                        #//*[@id="tabpanel-1"]/div/div[1]/div/div/table/tbody/tr[1]/td[1]
                                dimensione = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tabpanel-1"]/div/div[1]/div/div/div[2]/table/tbody/tr['+str(s)+']/td[1]')))
                                misura = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tabpanel-1"]/div/div[1]/div/div/div[2]/table/tbody/tr['+str(s)+']/td[2]')))
                                dimensioni.append(dimensione.text +': '+ misura.text)  
                                                            
                        except: 
                            print("no dimensions found")
                            pass
                except:
                    pass                

                now = datetime.datetime.now()
                time_date = now.strftime("%Y-%m-%d %H:%M:%S")
                bag_url = driver.current_url
                print(bag_url)
                
                
                entry = {
                    "brand": brand.text,
                    "bag type": bag_type.text,
                    "price": priceINT,
                    "BrandID": IDbrandtext,
                    "bag_url":bag_url,
                    "description": descrizione,
                    "material": materiali,
                    "dimensions": dimensioni,
                    "bag_image": bag_image,
                    "date and time": time_date,
                }
                with open ("farfetch7_1.json", "a", encoding="UTF-8") as f:
                    json_object = json.dumps(entry,default=lambda o: '<not serializable>', ensure_ascii=False)
                    f.write(str(json_object + "\n"))
                    
                driver.back()         
            except:
                if(currentpage!=int(npage)+1):
                    if(i<89):
                        print('error - skip')   
                        continue
                    else:
                        print("borse finite nella pagina")
                        currentpage = currentpage+1
                        if (currentpage>2):
                            url = re.sub(r".$", str(currentpage), driver.current_url)
                            driver.get(url)
                            print(i)
                            break
                        else:
                            driver.get(driver.current_url +'?page='+str(currentpage)+'')
                            break

driver.quit()
