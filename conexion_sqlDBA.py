import pyodbc
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
class Funciones:
    def __init__(self):
        host = "localhost"    
        database = "cafeteria_new"  
        try:
            self.conexion = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={host};'
                f'DATABASE={database};'
                f'Trusted_Connection=yes;'
            )
            
        except pyodbc.Error as e:
            print(f"Error al conectar{e}")
    def cerrar_conexion(self):
        try:
            if self.conexion:
                self.conexion.close() 
                print("Conexión cerrada correctamente.")
        except pyodbc.Error as e:
            print(f"Error al cerrar la conexión: {e}")

    def select(self,tabla):
        try:
            cursor=self.conexion.cursor()
            
            consulta = f"SELECT * FROM {tabla} ;"  
            cursor.execute(consulta)

        
            resultados = cursor.fetchall()
            cursor.close()
            
            return resultados
        except pyodbc.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
    def select_view(self,tabla,columna):
        try:
            cursor=self.conexion.cursor()
            
            consulta = f"SELECT * FROM {tabla} ORDER BY {columna} DESC;"
  
            cursor.execute(consulta)

        
            resultados = cursor.fetchall()
            cursor.close()
            
            return resultados
        except pyodbc.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
    
    def describe(self,tabla):
        try:
            cursor = self.conexion.cursor()
            
            consulta =  f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tabla}'"
            cursor.execute(consulta)
            resultados=[fila[0]for fila in cursor.fetchall()]  
            
            return resultados 
        except pyodbc.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None



            
    def insert_to(self, NombreTabla, val1, val2, val3, valor1, valor2, valor3):
        try:
            cursor = self.conexion.cursor()
            
            if NombreTabla == "producto":
                consulta = ''' EXEC [dbo].[AgregarProductos] ?, ?, ? '''
                cursor.execute(consulta, (valor1, valor2, valor3))

            elif NombreTabla == "pedidos":
                consulta=''' EXEC [dbo].[RegistrarPedido] ?, ?, ? '''

                cursor.execute(consulta, (valor1, valor2, valor3))
                filas_afectadas = cursor.rowcount
                if filas_afectadas != 1:
                    messagebox.showerror("Error","Ha ocurrido un error")
            elif NombreTabla == "detallespedido":
                consulta=''' EXEC [dbo].[RegistrarDetallePedido] ?, ?, ? '''

                cursor.execute(consulta, (valor1, valor2, valor3))
                filas_afectadas = cursor.rowcount
                print(filas_afectadas)
                if filas_afectadas != 1:
                    messagebox.showerror("Error","Ha ocurrido un error")

                


            else:
                consulta = f'''INSERT INTO {NombreTabla} ({val1}, {val2}, {val3})
                            VALUES (?, ?, ?)'''
                cursor.execute(consulta, (valor1, valor2, valor3))

            self.conexion.commit()
            return True

        except pyodbc.Error as e:
            return str(e)

        
    def insert_to2(self,NombreTabla,val1,val2,val3,val4,valor1,valor2,valor3,valor4):
        try:
                
                cursor=self.conexion.cursor()
                consulta=f'''INSERT INTO {NombreTabla}({val1},{val2},{val3},{val4})
                            VALUES
                            (?,?,?,?)
                            '''
                cursor.execute(consulta,(valor1,valor2,valor3,valor4))
                self.conexion.commit()
                return True
        except pyodbc.Error as e:
            return str(e)

        
    def delete(self,tabla,campo,valor):
        
        try:
            cursor = self.conexion.cursor()
            if tabla == "pedidos":
                consulta=''' EXEC [dbo].[sp_eliminar_pedido] ?'''

                cursor.execute(consulta, (valor))
                filas_afectadas = cursor.rowcount
                print(filas_afectadas)
            
            else:
                consulta = f"DELETE FROM {tabla} WHERE {campo} = ?"
                cursor.execute(consulta, valor)  
            self.conexion.commit()
            print(f"Se elimino correctamente de la tabla: {tabla}, el valor: {valor}")
        except pyodbc.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        
        
    def modificar(self,tabla,columna,nuevoValor,campoID,Id):
        
        try:
            cursor = self.conexion.cursor()
            
            consulta = f"UPDATE {tabla} SET {columna}=? WHERE {campoID}=?"      
            cursor.execute(consulta,nuevoValor,Id)  
            self.conexion.commit()
            return True
        except pyodbc.Error as e:
            return str(e) 