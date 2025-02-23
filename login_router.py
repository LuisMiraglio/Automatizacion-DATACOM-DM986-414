#pyinstaller --onefile --add-binary "msedgedriver.exe;." login_router.py
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime

def verificar_fecha():
    try:
        # Obtener la fecha y hora actual del sistema
        fecha_actual = datetime.now()

        # Definir la fecha límite (1 de abril de 2025)
        fecha_limite = datetime(2025, 4, 1)

        # Comparar las fechas
        if fecha_actual < fecha_limite:
            print("La fecha del sistema es válida. Continuando con la ejecución del script.")
            return True
        else:
            print("La fecha del sistema supera la fecha límite. El script no se ejecutará.")
            return False
    except Exception as e:
        print(f"No se pudo obtener la fecha del sistema: {e}")
        return False

# Uso de la función en tu script de Selenium
if verificar_fecha():
    # Coloca aquí el código de tu script de Selenium
    pass
else:
    print("Finalizando la ejecución del script debido a la verificación de fecha fallida.")


# Solicitar al usuario el SSID y la contraseña
ssid = input("Ingrese el SSID: ")
password = input("Ingrese la contraseña: ")
print(f"SSID ingresado: {ssid}")
print(f"Contraseña ingresada: {password}")

# Determinar la ruta base
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

# Obtiene la ruta del driver en base a la ruta determinada
driver_path = os.path.join(base_path, "msedgedriver.exe")
service = Service(driver_path)
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=options)

try:
    print("Abriendo la página del módem...")
    driver.get("http://192.168.0.1")
    print("Ingresando al módem...")

    # Esperar a que los campos de usuario y contraseña estén presentes
    wait = WebDriverWait(driver, 20)
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    # Ingresar las credenciales
    username_field.send_keys("user")
    password_field.send_keys("user")

    # Enviar el formulario
    password_field.send_keys(Keys.RETURN)

    # Hacer clic en el botón WAN
    print("Haciendo clic en el botón WAN...")
    wan_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@rel='4' and text()='WAN']")))
    wan_button.click()

    # Cambiar al contenido especificado
    print("Cambiando al contenido especificado...")
    content_iframe = wait.until(EC.presence_of_element_located((By.NAME, "contentIframe")))
    driver.switch_to.frame(content_iframe)

    # Hacer clic en la caja de verificación "Enable VLAN"
    print("Haciendo clic en la caja de verificación 'Enable VLAN'...")
    vlan_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='vlan' and @type='checkbox']")))
    vlan_checkbox.click()

    # Ingresar el número 500 en el campo "VLAN ID"
    print("Ingresando el número 500 en el campo 'VLAN ID'...")
    vlan_id_field = wait.until(EC.presence_of_element_located((By.NAME, "vid")))
    vlan_id_field.clear()
    vlan_id_field.send_keys("500")

    # Seleccionar "IPoE" en el menú desplegable "Channel Mode"
    print("Seleccionando 'IPoE' en el menú desplegable 'Channel Mode'...")
    channel_mode_dropdown = wait.until(EC.presence_of_element_located((By.NAME, "adslConnectionMode")))
    channel_mode_dropdown.click()
    ipoe_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='adslConnectionMode']/option[@value='1']")))
    ipoe_option.click()

    # Seleccionar "INTERNET" en el menú desplegable "Connection Type"
    print("Seleccionando 'INTERNET' en el menú desplegable 'Connection Type'...")
    connection_type_dropdown = wait.until(EC.presence_of_element_located((By.NAME, "ctype")))
    connection_type_dropdown.click()
    internet_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='ctype']/option[@value='2']")))
    internet_option.click()

    # Seleccionar "DHCP" en la sección "WAN IP Settings"
    print("Seleccionando 'DHCP' en la sección 'WAN IP Settings'...")
    dhcp_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and @value='1' and @name='ipMode']")))
    dhcp_option.click()

    # Hacer clic en la casilla "ALL" en la sección "Port Mapping"
    print("Haciendo clic en la casilla 'ALL' en la sección 'Port Mapping'...")
    all_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='chkpt_all' and @type='checkbox']")))
    all_checkbox.click()

    # Hacer clic en el botón "Apply Changes"
    print("Haciendo clic en el botón 'Apply Changes'...")
    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Apply Changes' and @name='apply']")))
    apply_button.click()
    print("✅ Se hizo clic en el botón 'Apply Changes'.")

    # Cambiar al contenido especificado
    print("Cambiando al contenido especificado...")
    driver.switch_to.default_content()
    wrapper = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='wrapper']")))

    # Hacer clic en el botón "WLAN"
    print("Haciendo clic en el botón 'WLAN'...")
    wlan_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nav']/li[3]/a")))
    wlan_button.click()

    # Cambiar al contenido especificado
    content_iframe = wait.until(EC.presence_of_element_located((By.NAME, "contentIframe")))
    driver.switch_to.frame(content_iframe)

    # Ingresar el SSID en el campo correspondiente
    print(f"Ingresando el SSID '{ssid}'...")
    ssid_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @name='ssid']")))
    ssid_field.clear()
    ssid_field.send_keys(ssid)

    # Seleccionar "Auto" en el menú desplegable "Channel Number"
    print("Seleccionando 'Auto' en el menú desplegable 'Channel Number'...")
    channel_number_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@name='chan']")))
    channel_number_dropdown.click()
    auto_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='chan']/option[@value='0']")))
    auto_option.click()

    # Hacer clic en el botón "Apply Changes"
    print("Haciendo clic en el botón 'Apply Changes'...")
    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Apply Changes' and @name='save']")))
    apply_button.click()
    print("✅ Se hizo clic en el botón 'Apply Changes'.")

    # Cambiar al contenido especificado
    print("Cambiando al contenido especificado...")
    driver.switch_to.default_content()
    wrapper = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='wrapper']")))

    # Hacer clic en "Security"
    print("Haciendo clic en 'Security'...")
    security_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@target='contentIframe' and @href='boaform/formWlanRedirect?redirect-url=/wlwpa.asp&wlan_idx=0']")))
    security_link.click()

    # Cambiar al contenido especificado
    content_iframe = wait.until(EC.presence_of_element_located((By.NAME, "contentIframe")))
    driver.switch_to.frame(content_iframe)

    # Seleccionar la opción "WPA2 Mixed" en el menú desplegable de "Encryption"
    print("Seleccionando la opción 'WPA2 Mixed' en el menú desplegable de 'Encryption'...")
    encryption_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='security_method' and @name='security_method']")))
    encryption_dropdown.click()
    wpa2_mixed_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='security_method']/option[@value='6']")))
    wpa2_mixed_option.click()

    # Ingresar la contraseña en el campo "Pre-Shared Key"
    print(f"Ingresando la contraseña en el campo 'Pre-Shared Key'...")
    psk_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password' and @name='pskValue' and @id='wpapsk']")))
    psk_field.clear()
    psk_field.send_keys(password)

    # Hacer clic en el botón "Apply Changes"
    print("Haciendo clic en el botón 'Apply Changes'...")
    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Apply Changes' and @name='save']")))
    apply_button.click()
    print("✅ Se hizo clic en el botón 'Apply Changes'.")

    # Cambiar al contenido especificado
    print("Cambiando al contenido especificado...")
    driver.switch_to.default_content()
    wrapper = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='wrapper']")))

    # Hacer clic en "wlan1 (2.4GHz)"
    print("Haciendo clic en 'wlan1 (2.4GHz)'...")
    wlan1_link = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[1]/div/ul/li[2]/h3/a")))
    wlan1_link.click()

    # Cambiar al contenido especificado
    content_iframe = wait.until(EC.presence_of_element_located((By.NAME, "contentIframe")))
    driver.switch_to.frame(content_iframe)

    # Ingresar el SSID en el campo correspondiente
    print(f"Ingresando el SSID '{ssid}' en el campo 'SSID'...")
    ssid_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @name='ssid']")))
    ssid_field.clear()
    ssid_field.send_keys(ssid)

    # Seleccionar "Auto" en el menú desplegable "Channel Number"
    print("Seleccionando 'Auto' en el menú desplegable 'Channel Number'...")
    channel_number_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@name='chan']")))
    channel_number_dropdown.click()
    auto_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='chan']/option[@value='0']")))
    auto_option.click()

    # Hacer clic en el botón "Apply Changes"
    print("Haciendo clic en el botón 'Apply Changes'...")
    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Apply Changes' and @name='save']")))
    apply_button.click()
    print("✅ Se hizo clic en el botón 'Apply Changes'.")

     # === Nuevo bloque: Hacer clic en "Security" para la red de 2.4GHz ===
    # Salir del iframe para interactuar con el menú lateral
    print("Cambiando al contenido principal para acceder al menú lateral...")
    driver.switch_to.default_content()
    wrapper = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='wrapper']")))

     # === Nuevo bloque: Hacer clic en "Security" para la red de 2.4GHz ===
    # Salir del iframe para interactuar con el menú lateral
    print("Cambiando al contenido principal para acceder al menú lateral...")
    driver.switch_to.default_content()
    wrapper = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='wrapper']")))

    #Hacer clic en "Security" para la red de 2.4GHz ===
    # Salir del iframe para interactuar con el menú lateral
    print("Cambiando al contenido principal para acceder al menú lateral...")
    driver.switch_to.default_content()
    wrapper = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='wrapper']")))

    # Hacer clic en "Security" para la red de 2.4GHz
    print("Haciendo clic en 'Security' para wlan1 (2.4GHz)...")
    security_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@target='contentIframe' and contains(@href, 'wlwpa.asp') and contains(@href, 'wlan_idx=1')]")))
    security_link.click()

    # Cambiar al contenido especificado
    content_iframe = wait.until(EC.presence_of_element_located((By.NAME, "contentIframe")))
    driver.switch_to.frame(content_iframe)

    # Seleccionar la opción "WPA2 Mixed" en el menú desplegable de "Encryption"
    print("Seleccionando la opción 'WPA2 Mixed' en el menú desplegable de 'Encryption'...")
    encryption_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@id='security_method' and @name='security_method']")))
    encryption_dropdown.click()
    wpa2_mixed_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@id='security_method']/option[@value='6']")))
    wpa2_mixed_option.click()

    # Ingresar la contraseña en el campo "Pre-Shared Key"
    print(f"Ingresando la contraseña en el campo 'Pre-Shared Key'...")
    psk_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password' and @name='pskValue' and @id='wpapsk']")))
    psk_field.clear()
    psk_field.send_keys(password)

    # Hacer clic en el botón "Apply Changes"
    print("Haciendo clic en el botón 'Apply Changes'...")
    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Apply Changes' and @name='save']")))
    apply_button.click()
    print("✅ Se hizo clic en el botón 'Apply Changes'.")

    # Cambiar al contenido especificado
    print("Cambiando al contenido especificado...")
    driver.switch_to.default_content()
    wrapper = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='wrapper']")))

    # Hacer clic en "Admin"
    print("Haciendo clic en 'Admin'...")
    admin_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='javascript:void(0)' and @rel='9']")))
    admin_link.click()

    # Hacer clic en el botón "Password"
    print("Haciendo clic en el botón 'Password'...")
    password_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@target='contentIframe' and @href='password.asp']")))
    password_link.click()

    # Cambiar al contenido especificado
    content_iframe = wait.until(EC.presence_of_element_located((By.NAME, "contentIframe")))
    driver.switch_to.frame(content_iframe)

    # Ingresar la palabra "user" en el campo "Old Password"
    print("Ingresando la palabra 'user' en el campo 'Old Password'...")
    old_password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password' and @name='oldpass']")))
    old_password_field.clear()
    old_password_field.send_keys("user")

    # Ingresar la nueva contraseña en el campo "New Password"
    print("Ingresando la nueva contraseña en el campo 'New Password'...")
    new_password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password' and @name='newpass']")))
    new_password_field.clear()
    new_password_field.send_keys("conectar")

    # Ingresar la confirmación de la nueva contraseña en el campo "Confirmed Password"
    print("Ingresando la confirmación de la nueva contraseña en el campo 'Confirmed Password'...")
    confirm_password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password' and @name='confpass']")))
    confirm_password_field.clear()
    confirm_password_field.send_keys("conectar")

    # Hacer clic en el botón "Apply Changes"
    print("Haciendo clic en el botón 'Apply Changes'...")
    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@class='link_bg' and @type='submit' and @value='Apply Changes' and @name='save']")))
    apply_button.click()
    print("✅ Se hizo clic en el botón 'Apply Changes'.")

    #Cambiar al contenido especificado y hacer clic en "Advance" ===
    print("Cambiando al contenido especificado...")
    driver.switch_to.default_content()
    wrapper = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='wrapper']")))

    # Hacer clic en "Advance"
    print("Haciendo clic en 'Advance'...")
    advance_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='javascript:void(0)' and @rel='7']")))
    advance_link.click()

    # Hacer clic en el botón "Remote Access"
    print("Haciendo clic en el botón 'Remote Access'...")
    remote_access_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@target='contentIframe' and @href='rmtacc.asp']")))
    remote_access_link.click()

    # Cambiar al contenido especificado
    content_iframe = wait.until(EC.presence_of_element_located((By.NAME, "contentIframe")))
    driver.switch_to.frame(content_iframe)

    # Hacer clic en la casilla de verificación "HTTPS"
    print("Haciendo clic en la casilla de verificación 'HTTPS'...")
    https_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and @name='w_https' and @value='1']")))
    https_checkbox.click()

    # Hacer clic en el botón "Apply Changes"
    print("Haciendo clic en el botón 'Apply Changes'...")
    apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@class='link_bg' and @type='submit' and @value='Apply Changes' and @name='set']")))
    apply_button.click()
    print("✅ Se hizo clic en el botón 'Apply Changes'.")

finally:
    # Cerrar el navegador
    driver.quit()