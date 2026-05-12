from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

PERFIL_CHROME = "Profile 2"
PATH_PERFIL_CHROME = r'C:\Users\Mac\AppData\Local\Google\Chrome\User Data\\'
PATRH_DRIVER = r'C:\Users\Mac\chromedriver'

perfiles_tiktok = []
perfiles_tiktok_contactados = []

backstage = "https://live-backstage.tiktok.com/portal/anchor/instant-messages"

mensaje_1 = "Hola! Somos Dreaml, Agencia Oficial de TikTok Live. Hemos visto tu perfil y creemos que tienes potencial para crecer dentro de TikTok Live, por lo que nos gustaría que te unieras a nosotros."
mensaje_2 = "Holaa! Somos Dreaml, Agencia Oficial de TikTok LIVE! Hemos visto el potencial de tu perfil y, dado que no colaboras con ninguna agencia oficial del programa, nos gustaría que formaras parte de nosotros."
mensaje_3 = "Hola! Somos Dreaml, Agencia Oficial de TikTok Live. Hemos visto el potencial de tu perfil y dado que no colaboras con ninguna agencia oficial del programa, nos gustaría que te unieras a nosotros."
mensajes = [mensaje_2,mensaje_3]

max_iteraciones = 200

def send_msg_backstage(PERFIL_CHROME,PATH_PERFIL_CHROME,PATRH_DRIVER,backstage,usuarios = list):
    perfiles_contactados = []

  # Entrar en Instgram en la publicacion especifica:

    option = Options()
    # Indacar la ruta de los perfiles de chrome
    option.add_argument("--user-data-dir=" r'C:\Users\Mac\AppData\Local\Google\Chrome\User Data\\')
    option.add_argument('--profile-directory='+f'{PERFIL_CHROME}')  # Perfil escogido
    #option.add_argument("--headless")
    
    # Desactivar las notificaciones del navegador
    option.add_experimental_option("excludeSwitches",["enable-automation"])

 # Indicar la ruta del manejador del navegador
    driver = webdriver.Chrome(executable_path=r'C:\Users\Mac\chromedriver', options=option)
    driver.implicitly_wait(2)
    driver.maximize_window()

# Ingresa al text_area
    driver.get(backstage)
    contactados = 0
    for i, usuario in enumerate(usuarios):

        try:
            
            if i == max_iteraciones:
                break
            
            
            search_area = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div[4]/div/div/main/div/div/div/div/div/div/div/div/div[1]/div[1]/div/div/input')))
            search_area.send_keys(Keys.CONTROL + "a")
            search_area.send_keys(Keys.BACKSPACE)
            search_area.send_keys(usuario)
            
            search_area.send_keys(Keys.ENTER)
            sleep(3)
            
            first_match = driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div/div/main/div/div/div/div/div/div/div/div/div[1]/div[1]/div/div[2]/div/div/div/div/div/div/div')
            first_match.click()
            sleep(3)
                                                                  
            
            input_msg = search_area = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div[4]/div/div/main/div/div/div/div/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[1]/textarea')))
    
            selector_padre = '#neo-layout-fmp > div > div > div > div > div > div.rightContainer_633b1 > div.contentArea_633b1 > div.centerArea_633b1 > div.messageArea_633b1 > div > div > div:nth-child(1) > div > div.messageLayout_506c9'
            try:
               driver.find_element(By.CSS_SELECTOR, selector_padre)
            except:    
                mensaje = random.choice(mensajes)
                input_msg.send_keys(mensaje)
                first_message_send =  WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div[4]/div/div/main/div/div/div/div/div/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[2]/button')))
                first_message_send.click()
                sleep(3)
            
                
                contactados = contactados + 1
    
        
                
                perfiles_contactados.append(usuario)
        except:
             continue
        
    driver.quit()

    print(f"Perfiles conctactados:{contactados}")

    with open('perfiles_tiktok_contactados.txt', 'a', encoding='utf-8') as archivo:
                for elemento in perfiles_contactados:
                    archivo.write(f"{elemento}\n") 


if __name__ == "__main__":

    with open('perfiles_tiktok.txt', 'r', encoding='utf-8') as file:
        perfiles_tiktok = file.read().splitlines()

    with open('perfiles_tiktok_contactados.txt', 'r', encoding='utf-8') as file:
        perfiles_tiktok_contactados = file.read().splitlines()

    perfiles_tiktok = [elemento for elemento in perfiles_tiktok if elemento not in perfiles_tiktok_contactados]  
    
    send_msg_backstage(PERFIL_CHROME,PATH_PERFIL_CHROME,PATRH_DRIVER,backstage,perfiles_tiktok)
