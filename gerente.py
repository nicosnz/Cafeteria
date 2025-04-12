import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from conexion_sqlDBA import *

path_icono = os.path.join(os.path.dirname(__file__), "coffee-cup.ico")

class Interfaz(Frame):
    funciones=Funciones()
    def __init__(self, master = None):
        super().__init__(master, bg = "#6F4E37", height = 400, width = 840)
        self.master=master
        self.master.resizable(False,False)
        self.master.iconbitmap(path_icono)
        self.pack()
        self.objetos()
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
    
    def cerrar_ventana(self):
        self.funciones.cerrar_conexion()
        self.master.destroy()

    def elemento_vacio(self,cadena):
        for x in cadena:
            if not x:
                return True
        return False
    
    #ocultar interfaces
    def ocultar_mostrar(self,bloque_a_ocultar,bloque_a_mostrar):
        if bloque_a_ocultar:
            bloque_a_ocultar.place_forget()
        if bloque_a_mostrar:
            bloque_a_mostrar.place(x=20,y=20,height=355,width=150)
    def ocultar_mostrarForm(self,bloque_a_ocultar,bloque_a_mostrar):
        if bloque_a_ocultar:
            bloque_a_ocultar.place_forget()
        if bloque_a_mostrar:
            bloque_a_mostrar.place(x=20,y=20,height=355,width=180)
  
    #limpiar datos
    def limpiar_database(self):
        for datos in self.vista_database.get_children():
            self.vista_database.delete(datos)
    def limpiar_formulario(self):
        for widget in self.Formulario.winfo_children():
            widget.destroy()
    def limpiar_entrys(self,entrys):
        for i in entrys:
            i.delete(0,END)
        entrys[0].focus()

    #metodos de las interfaces
    def ver_tabla(self,tabla,columna):
        columnas=self.funciones.describe(tabla)
        
        datos_tabla_seleccionada=self.funciones.select_view(tabla,columna)
        
        self.vista_database['columns']=columnas
        for x in columnas:
            self.vista_database.column(x,width=120,anchor=CENTER)
            self.vista_database.heading(x,text=x,anchor=CENTER)
        self.vista_database['show']='headings'
        #limpiar tabla cada vez que se active el metodo ver_tabla
        if self.ver_tabla:
            self.limpiar_database()

        for dato in (datos_tabla_seleccionada):
            if (len(columnas)<=4):
                self.vista_database.insert("", END, values=(dato[0],dato[1],dato[2],dato[3]))
            else:
                self.vista_database.insert("", END, values=(dato[0],dato[1],dato[2],dato[3],dato[4]))

    #metodo creador de interfaces
    def crear_interfaz(self,comandos):
        bloque=Frame(self,bg="#E3E1DC")
        for i,(nombre_boton,comando) in enumerate(comandos):
            boton=Button(bloque,text=nombre_boton,bg="#C19A6B",command=comando)
            boton.place(x=7,y=5+i*50,height=45,width=135)
        boton_regresar = Button(bloque, text="REGRESAR", bg="#Ff0000", command=lambda: self.ocultar_mostrar(bloque,self.bloque_principal))
        boton_regresar.place(x=7, y=5 + len(comandos) * 50, height=45, width=135)
        return bloque
    
        
    def objetos(self):
        #listas de comandos
        self.comandos_ver = [
            ("VENTAS HOY", lambda: self.ver_tabla('VentasHoy',"Monto")),
            ("CLIENTES COMPRADORES", lambda: self.ver_tabla('vista_mejoresclientes',"CantidadCompras")),
            ("MEJORES PRODUCTOS", lambda: self.ver_tabla('vista_mejoresproductos',"CantidadCompras")),
            ("MEJORES CLIENTES", lambda: self.ver_tabla('vista_clientes_mayor_gasto',"TotalGastado")),
            ("PRODUCTOS BAJO STOCK", lambda: self.ver_tabla('vista_productos_bajo_stock',"Stock")),
            ("MEJORES VENDEDORES", lambda: self.ver_tabla('vista_mejores_vendedores',"TotalVentas")),
        ]

        #creacion de la interfaz principal
        self.bloque_principal=Frame(self,bg="#F5EDE1")
        self.bloque_principal.place(x=20,y=20,height=100,width=150)
        self.ver=Button(self.bloque_principal,text="REPORTES",bg="#C19A6B",command=lambda:self.ocultar_mostrar(self.bloque_principal,self.interfaz_vista))
        self.ver.place(x=7,y=10,height=80,width=135)

        #creacion de las diferentes vistas de las interfaces
        self.interfaz_vista=self.crear_interfaz(self.comandos_ver)        
        
        #creacion del treeview (hace que se vea la base de datos)
        self.vista_database=ttk.Treeview(self)
        self.vista_database.place(x=220,y=18,width=600,height=355)


def mainGerente():
    raiz=Tk()
    raiz.wm_title("Cafeteria")

    app=Interfaz(raiz)

    app.mainloop()

