#importo las herramientas que necesito
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {    #para evitar los pop up que interfieren en el proceso
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "password_manager_enabled": False,
    "profile.password_manager_leak_detection": False,  
    "password_leak_detection_enabled": False           
})

#etiqueto el test de LOGIN
@pytest.mark.login
def test_login_exitoso():

    #Abro el navegador y agrando
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    # Navego en la página
    driver.get("https://www.saucedemo.com/")

    # Ubico elementos usuario-password-botón login
    usuario = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    boton_login = driver.find_element(By.ID, "login-button")

    # completo datos para el login
    usuario.send_keys("standard_user")
    password.send_keys("secret_sauce")
    boton_login.click()
  
    # Creo una espera explicita
    wait = WebDriverWait(driver, 10)

    #Ubico elemento Title
    titulo_inventario = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )

    # Verifico que el titulo sea productos
    assert titulo_inventario.text == "Products"

    # Valido la URL
    assert "/inventory.html" in driver.current_url
    #Cierro navegador
    driver.quit()


#etiqueto el test de CATALOGO
@pytest.mark.catalogo
def test_catalogo_productos():

    # Abro navegador y agrando ventana
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    # Navego la página y me logueo 
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    wait = WebDriverWait(driver, 10)

    # Valido que el título es "Products"
    titulo = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )
    assert titulo.text == "Products"

    #Valido que existen productos visibles:
    #Primero busco el elemento
    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    #Posibles resultados:
    assert len(productos) > 0, "No se encontraron productos en la página"

    # Valido elementos menú y filtro
    #Primero busca los elementos
    menu = driver.find_element(By.ID, "react-burger-menu-btn")
    filtro = driver.find_element(By.CLASS_NAME, "product_sort_container")

    assert menu.is_displayed()
    assert filtro.is_displayed()

    # Obtener nombre y precio del primer producto
    primer_producto_nombre = productos[0].find_element(By.CLASS_NAME, "inventory_item_name").text
    primer_producto_precio = productos[0].find_element(By.CLASS_NAME, "inventory_item_price").text

    print("\nPrimer producto:")
    print("Nombre:", primer_producto_nombre)
    print("Precio:", primer_producto_precio)

    driver.quit()
    
#marco TEST CARRITO
@pytest.mark.carrito
def test_agregar_producto_al_carrito():

    # Abro el navegador
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    # Entro al sitio
    driver.get("https://www.saucedemo.com/")

    # Espero carga y completo el login
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Espero que cargue el catálogo
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list"))
    )

    # Ubico los productos del catálogo
    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(productos) > 0, "No se encontraron productos para agregar al carrito"

    # Tomo el primer producto
    primer_producto = productos[0]

    # Pausa visual
    time.sleep(1)

    # Ubico nombre del primer producto
    nombre_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text

    # Selecciono el botón correcto dentro del producto
    boton_agregar = WebDriverWait(primer_producto, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory"))
    )

    # Pausa visual antes del click
    time.sleep(1)
    boton_agregar.click()

    # Pequeña pausa para permitir que se actualice el ícono
    time.sleep(1)

    # Espero a que aparezca el badge del carrito
    carrito_badge = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert carrito_badge.text == "1", "El carrito no muestra la cantidad correcta"

    # Ingreso al carrito
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # Espero que cargue el carrito
    item_carrito = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "cart_item"))
    )

    # Verifico que el producto sea el correcto
    nombre_carrito = item_carrito.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert nombre_carrito == nombre_producto, "El producto del carrito no coincide con el que agregaste"

    # Cierro navegador
    time.sleep(1)
    driver.quit()
