import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from conexion_sqlDBA import *

path_icono = os.path.join(os.path.dirname(__file__), "coffee-cup.ico")

class Vendedor(Frame):
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
    def ver_tabla(self,tabla):
        columnas=self.funciones.describe(tabla)
        
        
        
        datos_tabla_seleccionada=self.funciones.select(tabla)
        
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
            
        
    def metodo_agregar(self, tabla):
        self.ver_tabla(tabla)
        self.ocultar_mostrarForm(self.interfaz_agregar,self.Formulario)
        self.tabla_agregar=tabla
        self.limpiar_formulario()
        self.columnas_agregar = self.funciones.describe(tabla)
        self.columnas_agregar.pop(0)
        
        

        
        total_columnas=len(self.columnas_agregar)
        
        self.labels=[]
        self.entrys=[]
        for i in range(total_columnas):  
                label = Label(self.Formulario, text="")
                label.place(x=50, y=10+i*70)  
                self.labels.append(label)
                 #Crear el Entry
                entry1 = Entry(self.Formulario,bg="white")
                entry1.place(x=5, y=37 +i*70, height=20, width=170)
                self.entrys.append(entry1)
 
        
        # Actualizar el texto de los Labels
        for i, label in enumerate(self.labels):
            label.config(text=self.columnas_agregar[i] if i < len(self.columnas_agregar) else "")
            
        self.guardar = Button(self.Formulario, text="GUARDAR", bg="green",command=self.guardar_agregar)
        self.guardar.place(x=5, y=277, height=35, width=80)
        
        self.cancelar_agregar = Button(self.Formulario, text="CANCELAR", bg="#Ff0000", command=lambda:self.limpiar_entrys(self.entrys))
        self.cancelar_agregar.place(x=95, y=277, height=35, width=80)
        
        self.regresar3 = Button(self.Formulario, text="REGRESAR", bg="#Ff0000", command=lambda:self.ocultar_mostrar(self.Formulario,self.interfaz_agregar))
        self.regresar3.place(x=3, y=315, height=35, width=173)
    
    def guardar_agregar(self):
        lista_sin_procesar=[]
        lista_procesada=[]
        columnas=self.columnas_agregar
        
        for i in range(len(self.entrys)):
            lista_sin_procesar.append(self.entrys[i].get())
      
        comprobar_elemento_vacio=self.elemento_vacio(lista_sin_procesar) 
            
        if comprobar_elemento_vacio==True:
            messagebox.showwarning("Agregar",'No introdujo ningún valor.')
            return    
        
        for valor in lista_sin_procesar:
            if valor.lstrip('-').isdigit() :
                if int(valor) < 0:
                    messagebox.showwarning("Agregar",'No se permiten numeros negativos.')
                    return
            

        for valor in lista_sin_procesar:
            if valor.isdigit() :
                lista_procesada.append(int(valor))
            else:
                lista_procesada.append(valor)
        
        if len(columnas)<4:
            resultado=self.funciones.insert_to(self.tabla_agregar,columnas[0],columnas[1],columnas[2],lista_procesada[0],lista_procesada[1],lista_procesada[2])
           
        else:
            resultado=self.funciones.insert_to2(self.tabla_agregar,columnas[0],columnas[1],columnas[2],columnas[3],lista_procesada[0],lista_procesada[1],lista_procesada[2],lista_procesada[3])
           
            
        

        messagebox.showinfo("Agregar", f"{resultado}")
        self.limpiar_entrys(self.entrys)
            
        
    def metodo_modificar(self,table):
        self.ver_tabla(table)   
        self.ocultar_mostrarForm(self.interfaz_modificar,self.Formulario)
        self.limpiar_formulario()
        self.tabla_modificar=table
        
        columnas_modificar = self.funciones.describe(table)
        self.id=columnas_modificar[0]
        self.labels=[]
        self.entrys=[]
        label = Label(self.Formulario, text="Columnas :")
        label.place(x=55, y=20)  
        self.labels.append(label)
        
        self.columna_valor=None
        columnas_modificar.pop(0)
        
        self.cur=StringVar()
        self.cur.set(columnas_modificar[0])
        self.cur.trace_add("write",self.obtener_valor)
       
        menu=OptionMenu(self.Formulario,self.cur,*columnas_modificar)
        menu.place(x=42,y=50)

        label2 = Label(self.Formulario, text="Nuevo Valor")
        label2.place(x=50, y=140)  
        self.labels.append(label2)
        entry2 = Entry(self.Formulario,bg="white")
        entry2.place(x=5, y=170, height=20, width=170)
        self.entrys.append(entry2)
        
        label3 = Label(self.Formulario, text="ID")
        label3.place(x=74, y=200)  
        self.labels.append(label3)
        entry3 = Entry(self.Formulario,bg="white")
        entry3.place(x=5, y=225, height=20, width=170)
        self.entrys.append(entry3)

        self.guardar = Button(self.Formulario, text="GUARDAR", bg="green",command=self.guardar_modificar)
        self.guardar.place(x=5, y=277, height=35, width=80)
        
        self.cancelar_modificar = Button(self.Formulario, text="CANCELAR", bg="#Ff0000", command=lambda:self.limpiar_entrys(self.entrys))
        self.cancelar_modificar.place(x=95, y=277, height=35, width=80)
        
        self.regresar3 = Button(self.Formulario, text="REGRESAR", bg="#Ff0000", command=lambda:self.ocultar_mostrar(self.Formulario,self.interfaz_modificar))
        self.regresar3.place(x=3, y=315, height=35, width=173)
        
    def obtener_valor(self,*args):
        self.columna_valor=self.cur.get()
        
    def guardar_modificar(self):
        valor1=self.columna_valor
        valor2=self.entrys[0].get()
        valor4=self.entrys[1].get()
        
        campo_id=self.id
        if valor2=='' or valor4=='':
            messagebox.showwarning("Modificar",'No introdujo valores.')
            return
        try:
            valor3=int(self.entrys[1].get())
        except ValueError:
            messagebox.showerror("Modificar", "El campo de ID debe ser un número entero.")
            return
        
        respuesta=messagebox.askquestion("Modificar","¿Deseas modificar el registro seleccionado?")
        if respuesta==messagebox.YES:
            resultado=self.funciones.modificar(self.tabla_modificar,valor1,valor2,campo_id,valor3)
        else:
            self.limpiar_entrys(self.entrys)
            
        if resultado!=True:
            messagebox.showerror("Error en la Base de Datos", f"Error: {resultado}")
            return
        
        messagebox.showinfo("Modificar",'Elemento modificado correctamente.')
        self.limpiar_entrys(self.entrys)
                
            

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
            ("CLIENTES", lambda: self.ver_tabla('clientes')),
            ("PRODUCTOS", lambda: self.ver_tabla('producto')),
            ("DETALLES PEDIDOS", lambda: self.ver_tabla('detallespedido')),
            ("PEDIDOS", lambda: self.ver_tabla('pedidos')),
            ("PAGOS", lambda: self.ver_tabla('pagos')),
        ]

        self.comandos_agregar = [
            ("CLIENTES", lambda: self.metodo_agregar('clientes')),
            ("PRODUCTOS", lambda: self.metodo_agregar('producto')),
            ("DETALLES PEDIDOS", lambda: self.metodo_agregar('detallespedido')),
            ("PEDIDOS", lambda: self.metodo_agregar('pedidos')),
            ##("PAGOS", lambda: self.metodo_agregar('pagos')),
        ]

        self.comandos_modificar = [
            ("CLIENTES", lambda: self.metodo_modificar('clientes')),
            ("PRODUCTOS", lambda: self.metodo_modificar('producto')),
            ("DETALLES PEDIDOS", lambda: self.metodo_modificar('detallespedido')),
            ("PEDIDOS", lambda: self.metodo_modificar('pedidos')),
            ("PAGOS", lambda: self.metodo_modificar('pagos')),
        ]

        #creacion de la interfaz principal
        self.bloque_principal=Frame(self,bg="#F5EDE1")
        self.bloque_principal.place(x=20,y=20,height=270,width=150)
        self.ver=Button(self.bloque_principal,text="VER",bg="#C19A6B",command=lambda:self.ocultar_mostrar(self.bloque_principal,self.interfaz_vista))
        self.ver.place(x=7,y=10,height=80,width=135) 
        self.agregar=Button(self.bloque_principal,text="AGREGAR",bg="#C19A6B",command=lambda:self.ocultar_mostrar(self.bloque_principal,self.interfaz_agregar))
        self.agregar.place(x=7,y=95,height=80,width=135)
        self.modificar=Button(self.bloque_principal,text="MODIFICAR",bg="#C19A6B",command=lambda:self.ocultar_mostrar(self.bloque_principal,self.interfaz_modificar))
        self.modificar.place(x=7,y=180,height=80,width=135)

        #creacion de las diferentes vistas de las interfaces
        self.interfaz_vista=self.crear_interfaz(self.comandos_ver)        
        self.interfaz_agregar=self.crear_interfaz(self.comandos_agregar)
        self.interfaz_modificar=self.crear_interfaz(self.comandos_modificar)
        
        #creacion del formulario
        self.Formulario=Frame(self,bg="#E3E1DC")
        
        #creacion del treeview (hace que se vea la base de datos)
        self.vista_database=ttk.Treeview(self)
        self.vista_database.place(x=220,y=18,width=600,height=355)


def main():
    raiz=Tk()
    raiz.wm_title("Cafeteria")

    app=Vendedor(raiz)

    app.mainloop()

