import tkinter as tk
from tkinter import messagebox, filedialog
import os
import requests
import csv
from datetime import datetime

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
        # Consulta a la API de Mintscan para ATOM
        url = f"https://api.mintscan.io/v1/cosmos/account/{wallet}/txs"
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTA1NSwiaWF0IjoxNzQ2NjE3ODQxfQ.sWnquLQMNJtFpN-nD-LQS22V6GTp87fCirnvOMlAUmx3HFeobGePmfCj8X_Ze0ENje8OJb7Ya0WYMOO42ktBKQ"
        }
        try:
            response = requests.get(url, headers=headers)
            print(f"Status Code: {response.status_code}")  # Debug info
            print(f"Response: {response.text[:200]}")  # Debug info
            
            if response.status_code == 200:
                data = response.json()
                return data
            elif response.status_code == 404:
                return {"error": "Wallet no encontrada"}
            elif response.status_code == 401:
                return {"error": "Error de autenticación con la API"}
            else:
                return {"error": f"Error en la API: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            print(f"Error en la petición: {str(e)}")  # Debug info
            return {"error": f"Error de conexión: {str(e)}"}
        except Exception as e:
            print(f"Error inesperado: {str(e)}")  # Debug info
            return {"error": f"Error inesperado: {str(e)}"}

    return None

def exportar_a_csv(transactions, wallet):
    # Crear nombre de archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reporte_cosmos_{wallet}_{timestamp}.csv"
    
    # Pedir al usuario dónde guardar el archivo
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        initialfile=filename,
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if file_path:
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                # Escribir encabezados
                writer.writerow(['Fecha', 'Tipo', 'Cantidad', 'Hash', 'Estado'])
                
                # Escribir datos
                for tx in transactions:
                    writer.writerow([
                        tx.get('timestamp', 'N/A'),
                        tx.get('type', 'N/A'),
                        tx.get('amount', 'N/A'),
                        tx.get('txHash', 'N/A'),
                        tx.get('status', 'N/A')
                    ])
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo: {str(e)}")
            return False
    return False

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
    print(f"Info recibida: {info}")  # Debug info

    if info:
        # Mostrar los resultados de la consulta
        if blockchain == "ATOM":
            if isinstance(info, dict):
                if "error" in info:
                    messagebox.showerror("Error", info["error"])
                    return
                    
                if "data" in info:
                    transactions = info["data"]
                    if not transactions:
                        messagebox.showinfo("Consulta exitosa", f"No se encontraron transacciones para la wallet {wallet}")
                        return
                        
                    result_text = f"Blockchain: {blockchain}\nWallet: {wallet}\n\nTransacciones encontradas: {len(transactions)}\n\n"
                    
                    for tx in transactions[:10]:  # Mostrar las 10 primeras transacciones
                        timestamp = tx.get("timestamp", "N/A")
                        tx_type = tx.get("type", "N/A")
                        amount = tx.get("amount", "N/A")
                        result_text += f"Fecha: {timestamp}\nTipo: {tx_type}\nCantidad: {amount}\n\n"
                    
                    if len(transactions) > 10:
                        result_text += f"... y {len(transactions) - 10} transacciones más"
                    
                    # Preguntar si quiere exportar a CSV
                    if messagebox.askyesno("Exportar", "¿Deseas exportar todas las transacciones a un archivo CSV?"):
                        if exportar_a_csv(transactions, wallet):
                            messagebox.showinfo("Éxito", "Reporte exportado correctamente")
                    
                    messagebox.showinfo("Consulta exitosa", result_text)
                else:
                    messagebox.showinfo("Consulta exitosa", f"No se encontraron transacciones para la wallet {wallet}")
            else:
                messagebox.showinfo("Consulta exitosa", f"No se encontraron transacciones para la wallet {wallet}")
        else:
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

