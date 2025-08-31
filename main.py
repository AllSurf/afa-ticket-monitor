from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import hashlib
import winsound
from datetime import datetime

# --- Configuración ---
URL = "https://shop.afatickets.com.ar/content"
CHECK_INTERVAL = 15  # cada 15 segundos
SIRENA_FILE = "sirena-tornado.wav"  # poné tu archivo de sirena en la misma carpeta
HEADLESS = False  # True para monitoreo en background

no_change_counter = 0  # cuenta los chequeos sin cambios

# --- Setup Selenium ---
options = webdriver.ChromeOptions()
if HEADLESS:
    options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--log-level=3")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
)
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- Funciones ---
def get_ticket_html(driver):
    driver.get(URL)
    time.sleep(5)

    # obtener el nodo catalog y su padre
    catalog = driver.find_element(By.ID, "catalog")
    parent = catalog.find_element(By.XPATH, "..")

    # obtener HTML de catalog
    catalog_html = catalog.get_attribute("outerHTML")

    # obtener nombres de los hermanos
    siblings = parent.find_elements(By.XPATH, "./*")
    sibling_summary = "\n".join([
        f"{el.tag_name} {el.get_attribute('class') or ''}".strip()
        for el in siblings
    ])

    # combinar ambos para el hash
    return catalog_html + "\n<!-- Siblings -->\n" + sibling_summary

def hash_html(html):
    return hashlib.md5(html.encode("utf-8")).hexdigest()

def alerta_sonora():
    try:
        winsound.PlaySound(SIRENA_FILE, winsound.SND_FILENAME)
    except:
        winsound.Beep(2500, 1000)

def beep_suave():
    winsound.Beep(1000, 50)  # beep corto para indicar revisión sin cambios

# --- Loop principal ---
last_hash = None

while True:
    try:
        current_html = get_ticket_html(driver)
        current_hash = hash_html(current_html)
        now = datetime.now().strftime("%H:%M:%S")

        if last_hash is None:
            with open("initial_page.html", "w", encoding="utf-8") as f:
                f.write(current_html)
            last_hash = current_hash  # primer chequeo
            #last_hash = last_hash +"n" # forzar cambio
            print(f"{now} -- Estado inicial guardado.")
        elif current_hash != last_hash:
            print(f"{now} - ¡Cambio detectado! Reproduciendo alerta sonora...")
            alerta_sonora()
            last_hash = current_hash
        else:
            no_change_counter += 1
            if no_change_counter >= 3:
                print(f"{now} - Sin cambios. (beep)")
                beep_suave()
                no_change_counter = 0  # reiniciar luego del beep
            else:
                print(f"{now} - Sin cambios. ({no_change_counter})")

    except Exception as e:
        print(f"❌{now}: ", e)

    time.sleep(CHECK_INTERVAL)
