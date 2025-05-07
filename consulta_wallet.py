import tkinter as tk
from tkinter import messagebox

# Lista de blockchains que se extraen del archivo settings.py
blockchains = [
    "AKT", "ALGO", "ARCH", "ATOM", "DYDX", "EVMOS", "INJ", "JUNO", "OSMO", "STRD", "TIA", "KUJI", "KYVE", "LUNA1", "LUNA2", "MNTL", "NLS", "NTRN", "SEI", "SOL", "SCRT", "STARS", "STRD", "TIA", "TORI"
]

# Función que se ejecuta cuando el usuario presiona "Consultar"
def consultar():
    # Obtener la blockchain seleccionada y la wallet ingresada
    blockchain = blockchain_var.get()
    wallet = wallet_entry.get()

    if not wallet:
        messagebox.showerror("Error", "Por favor, ingresa una wallet válida.")
        return

    # Aquí puedes agregar tu lógica de conexión con las APIs
    # Ejemplo: conectar con la API de la blockchain seleccionada y mostrar la wallet
    messagebox.showinfo("Consulta exitosa", f"Blockchain seleccionada: {blockchain}\nWallet ingresada: {wallet}")

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
