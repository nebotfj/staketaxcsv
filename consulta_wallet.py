import tkinter as tk
from tkinter import messagebox
import os
import requests

# Aquí importa los módulos que necesitas de StakeTax
# Ejemplo: si tienes una función en staketax que consulta la blockchain
# from staketax_module import consulta_wallet

# Lista de blockchains que se extraen del archivo settings.py
blockchains = [
    "AKT", "ALGO", "ARCH", "ATOM", "DYDX", "EVMOS", "INJ", "JUNO", "OSMO", "STRD", "TIA", "KUJI", "KYVE", "LUNA1", "LUNA2", "MNTL", "NLS", "NTRN", "SEI", "SOL", "SCRT", "STARS", "STRD", "TIA", "TORI"
]

# Función para obtener la información de la wallet
def obtener_info_wallet(blockchain, wallet):
    # Aquí es donde iría la lógica de StakeTax para hacer la consulta a las APIs
    # Ejemplo para una blockchain "KUJI"
    
    if blockchain == "KUJI":
        kuji_node = os.environ.get("STAKETAX_KUJI_NODE", "https://kujira-api.polkachu.com")
        # Realiza una consulta a la API usando requests (o la que uses en StakeTax)
        url = f"{kuji_node}/wallet/{wallet}/transactions"  # Ejemplo de URL
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Procesar los datos aquí
                data = response.json()
                return data
            else:
                return None
        except Exception as e:
            return f"Error al obtener datos: {e}"

    # Añadir más condiciones para otras blockchains
    elif blockchain == "ATOM":
        # Implementar consulta para ATOM
        pass
    # Puedes continuar para otras blockchains

    return None

# Función que se ejecuta cuando el usuario presiona "Consultar"
def consultar():
    # Obtener la blockchain seleccionada y la wallet ingresada
    blockchain = blockchain_var.get()
    wallet = wallet_entry.get()

    if not wallet:
        messagebox.showerror("Error", "Por favor, ingresa una wallet válida.")
        return

    # Llamar a la función de consulta de StakeTax
    info = obtener_info_wallet(blockchain, wallet)

    if info:
        # Mostrar los resultados de la consulta
        messagebox.showinfo("Consulta exitosa", f"Blockchain seleccionada: {blockchain}\nWallet ingresada: {wallet}\nDatos: {info}")
    else:
        messagebox.showerror("Error", "No se pudo obtener información para esa wallet en la blockchain seleccionada.")

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Consulta de Wallet y Blockchain")

# Configurar la ventana
root.geometry("400x200")

# Título
title_label = tk.Label(root, text="Selecciona una Blockchain y pega la Wallet", font=("Arial", 14))
title_label.pack(pady=10)

# Crear el menú desplegable para seleccionar la blockchain
blockchain_var = tk.StringVar(root)
blockchain_var.set(blockchains[0])  # Establecer valor por defecto

blockchain_menu = tk.OptionMenu(root, blockchain_var, *blockchains)
blockchain_menu.pack(pady=10)

# Crear el cuadro de texto para ingresar la wallet
wallet_label = tk.Label(root, text="Introduce la Wallet:")
wallet_label.pack(pady=5)

wallet_entry = tk.Entry(root, width=40)
wallet_entry.pack(pady=5)

# Botón para consultar
consultar_button = tk.Button(root, text="Consultar", command=consultar)
consultar_button.pack(pady=10)

# Iniciar la interfaz
root.mainloop()

