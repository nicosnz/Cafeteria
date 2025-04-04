import pyodbc
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


        
def conectar_db(usuario,contraseña):
        try:
            conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=localhost;"
                "DATABASE=cafeteria_new;"
                f"UID={usuario};"
                f"PWD={contraseña};"
            )
            conn.cursor()
            return conn
        except Exception as e:
            messagebox.showerror("Error de conexión", "Nombre de Usuario o Contraseña Invalidos")

def cerrar_sesion(master, conn):
    if conn:  # Verifica si la conexión está activa
        conn.close()  # Cierra la conexión a la BD
    master.quit()  # Cierra la ventana actual