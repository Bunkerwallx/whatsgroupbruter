import itertools
import string
import requests
import random
import time
from colorama import Fore, Style

# Configuración
BASE_URL = "https://chat.whatsapp.com/"
CHARSET = string.ascii_letters + string.digits
LENGTH = 22
TIMEOUT = 5
PROXIES = [
    # Añade proxies aquí en el formato "http://ip:puerto"
]

def obtener_proxy():
    """
    Devuelve un proxy al azar de la lista de proxies.
    """
    return {"http": random.choice(PROXIES)} if PROXIES else None

def probar_url(codigo, numero):
    """
    Prueba una URL generada y verifica si es válida.
    """
    url = f"{BASE_URL}{codigo}"
    try:
        proxy = obtener_proxy()
        response = requests.get(url, timeout=TIMEOUT, proxies=proxy)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[{numero}] [VALIDO] {url}{Style.RESET_ALL}")
            with open("grupos_validos.txt", "a") as f:
                f.write(f"{numero}. {url}\n")
        else:
            print(f"{Fore.RED}[{numero}] [INVALIDO] {url}{Style.RESET_ALL}")
    except requests.RequestException:
        print(f"{Fore.YELLOW}[{numero}] [ERROR] {url}{Style.RESET_ALL}")

def generar_combinaciones(parcial=False):
    """
    Genera todas las combinaciones posibles o un subconjunto.
    """
    print(f"{Fore.CYAN}Generando combinaciones...{Style.RESET_ALL}")
    if parcial:
        # Genera un subconjunto aleatorio de combinaciones
        for _ in range(10000):  # Cambia el número según la necesidad
            yield ''.join(random.choices(CHARSET, k=LENGTH))
    else:
        # Genera todas las combinaciones
        for combinacion in itertools.product(CHARSET, repeat=LENGTH):
            yield ''.join(combinacion)

def main():
    print(f"{Fore.CYAN}Fuerza Bruta para URLs de Grupos de WhatsApp{Style.RESET_ALL}")
    try:
        contador = 0  # Inicializar contador
        for codigo in generar_combinaciones(parcial=True):  # Cambiar a False para modo completo
            contador += 1
            probar_url(codigo, contador)
            time.sleep(0.1)  # Pausa entre solicitudes para evitar detección
    except KeyboardInterrupt:
        print(f"{Fore.RED}\nProceso interrumpido por el usuario.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
