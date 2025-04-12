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

    def limpiarIds(self, valorID):
        if valorID.strip():  
            id_g = int(valorID.split()[0])
            return id_g
    #metodos de las interfaces
    def ver_tabla(self,tabla):
        columnas=self.funciones.describe(tabla)
        datos_tabla_seleccionada=self.funciones.select(tabla)

        
        
        # ##NUEVO

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
        ##NUEVO
        datos_tabla_empleados = self.funciones.select("empleados")
        datos_tabla_clientes = self.funciones.select("clientes")
        datos_tabla_pedidos = self.funciones.selectPedido("pedidos")
        datos_tabla_productos = self.funciones.selectProducto("producto")
        ##NUEVO

        self.labels=[]
        self.entrys=[]
        total_columnas=len(self.columnas_agregar)


        for i in range(total_columnas):  
                label = Label(self.Formulario, text="")
                label.place(x=50, y=10+i*70)  
                self.labels.append(label)
                
                 #Crear el Entry
                entry1 = Entry(self.Formulario,bg="white")
                entry1.place(x=5, y=37 +i*70, height=24, width=160)
                self.entrys.append(entry1)

        ##NUEVO
        empleados_lista = []
        for empleado in datos_tabla_empleados:
            nombre_completo = f"{empleado[0]} {empleado[1]} {empleado[2]}"  
            empleados_lista.append(nombre_completo)

        clientes_lista = []
        for cliente in datos_tabla_clientes:
            nombre_completo = f"{cliente[0]} {cliente[1]} {cliente[2]}"  
            clientes_lista.append(nombre_completo)

        pedidos_lista = []
        for pedido in datos_tabla_pedidos:
            nombre_completo = f"{pedido[0]}"  
            pedidos_lista.append(nombre_completo)

        productos_lista = []
        for producto in datos_tabla_productos:
            nombre_completo = f"{producto[0]} {producto[1]}"  
            productos_lista.append(nombre_completo)
 
        if tabla == "pedidos":
            
            self.entrada_agregar1 = StringVar()
            desplegableEntrada = ttk.Combobox(self.Formulario,
                                              font="Arial 13 ",
                                              width=16,
                                              values=clientes_lista,
                                              state="readonly",
                                              textvariable=self.entrada_agregar1)
            desplegableEntrada.place(x=5, y=37)
            
            
            self.entrada_agregar2 = StringVar()
            desplegableEntrada2 = ttk.Combobox(self.Formulario,
                                              font="Arial 13 ",
                                              width=16,
                                              values=empleados_lista,
                                              state="readonly",
                                              textvariable=self.entrada_agregar2)
            desplegableEntrada2.place(x=5, y=107)
        

        elif tabla == "detallespedido":
            self.entrada_agregar3 = StringVar()
            desplegableEntrada3 = ttk.Combobox(self.Formulario,
                                              font="Arial 13 ",
                                              width=16,
                                              values=pedidos_lista,
                                              state="readonly",
                                              textvariable=self.entrada_agregar3)
            desplegableEntrada3.place(x=5, y=37)
            
            self.entrada_agregar4 = StringVar()
            desplegableEntrada4 = ttk.Combobox(self.Formulario,
                                              font="Arial 13 ",
                                              width=16,
                                              values=productos_lista,
                                              state="readonly",
                                              textvariable=self.entrada_agregar4)
            desplegableEntrada4.place(x=5, y=107)
            
        elif tabla == "pagos":
            self.entrada_agregar5 = StringVar()
            desplegableEntrada5 = ttk.Combobox(self.Formulario,
                                              font="Arial 13 ",
                                              width=16,
                                              values=pedidos_lista,
                                              state="readonly",
                                              textvariable=self.entrada_agregar5)
            desplegableEntrada5.place(x=5, y=37)
            
        ##NUEVO
       
        
        
        
        # Actualizar el texto de los Labels
        for i, label in enumerate(self.labels):
            label.config(text=self.columnas_agregar[i] if i < len(self.columnas_agregar) else "")
            
        self.guardar = Button(self.Formulario, text="GUARDAR", bg="green",command=lambda:self.guardar_agregar(tabla))
        self.guardar.place(x=5, y=277, height=35, width=80)
        
        self.cancelar_agregar = Button(self.Formulario, text="CANCELAR", bg="#Ff0000", command=lambda:self.limpiar_entrys(self.entrys))
        self.cancelar_agregar.place(x=95, y=277, height=35, width=80)
        
        self.regresar3 = Button(self.Formulario, text="REGRESAR", bg="#Ff0000", command=lambda:self.ocultar_mostrar(self.Formulario,self.interfaz_agregar))
        self.regresar3.place(x=3, y=315, height=35, width=173)
    
    def guardar_agregar(self,tabla):
        lista_sin_procesar=[]
        lista_procesada=[]
        columnas=self.columnas_agregar

        if tabla == "pedidos":

            valor_id_cliente = self.entrada_agregar1.get()
            id_cliente = self.limpiarIds(valor_id_cliente)
            lista_procesada.append(id_cliente)
            valor_id_empleado = self.entrada_agregar2.get()
            id_empleado = self.limpiarIds(valor_id_empleado)
            lista_procesada.append(id_empleado)
            for i in range(2,len(self.entrys)):
                lista_sin_procesar.append(self.entrys[i].get())
        

        
        elif tabla == "detallespedido":
            valor_id_pedidos = self.entrada_agregar3.get()
            id_pedidos = self.limpiarIds(valor_id_pedidos)
            lista_procesada.append(id_pedidos)

            valor_id_producto = self.entrada_agregar4.get()
            id_producto = self.limpiarIds(valor_id_producto)
            lista_procesada.append(id_producto)
            for i in range(2,len(self.entrys)):
                lista_sin_procesar.append(self.entrys[i].get())
        elif tabla == "pagos":
            valor_id_pedido_pago = self.entrada_agregar5.get()
            id_pedido_pago = self.limpiarIds(valor_id_pedido_pago)
            lista_procesada.append(id_pedido_pago)
            for i in range(1,len(self.entrys)):
                lista_sin_procesar.append(self.entrys[i].get())

        else: 
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
           
            
        if resultado != True:
            messagebox.showerror("Error en la Base de Datos", f"Error: {resultado}")
            return  

        messagebox.showinfo("Agregar", "Elemento agregado correctamente.")
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

        
              
    def metodo_eliminar(self,tabla):
        self.ver_tabla(tabla)
        self.ocultar_mostrarForm(self.interfaz_eliminar,self.Formulario)
        
        self.limpiar_formulario()
        self.tabla_eliminar=tabla
        
        self.columnas_eliminar = self.funciones.describe(tabla)
        self.campo_id=self.columnas_eliminar[0]
        
        self.labels=[]
        self.entrys=[]
        
        label = Label(self.Formulario, text="ID")
        label.place(x=83, y=65)  
        self.labels.append(label)
        #Crear el Entry
        entry1 = Entry(self.Formulario,bg="white")
        entry1.place(x=5, y=100, height=20, width=170)
        self.entrys.append(entry1)
        self.guardar = Button(self.Formulario, text="GUARDAR", bg="green",command=self.guardar_eliminar)
        self.guardar.place(x=5, y=277, height=35, width=80)
        
        self.cancelar_eliminar = Button(self.Formulario, text="CANCELAR", bg="#Ff0000", command=lambda:self.limpiar_entrys(self.entrys))
        self.cancelar_eliminar.place(x=95, y=277, height=35, width=80)
        
        self.regresar3 = Button(self.Formulario, text="REGRESAR", bg="#Ff0000", command=lambda:self.ocultar_mostrar(self.Formulario,self.interfaz_eliminar))
        self.regresar3.place(x=3, y=315, height=35, width=173)
    
        
    
    def guardar_eliminar(self):
        id_eliminar_sin_procesar=self.entrys[0].get()
        
        if id_eliminar_sin_procesar =='':
            messagebox.showwarning("Eliminar", "No introdujo ningún valor.")
        else:
            try:
                id_eliminar_procesado=int(self.entrys[0].get())
                respuesta=messagebox.askquestion("Eliminar","¿Deseas eliminar el registro seleccionado?")
                if respuesta==messagebox.YES:
                    self.funciones.delete(self.tabla_eliminar,self.campo_id,id_eliminar_procesado)
                    messagebox.showinfo("Eliminar",'Elemento eliminado correctamente.')
                else:
                    self.limpiar_entrys(self.entrys)
            except:
                    messagebox.showerror("Eliminar",'El campo de ID debe ser un número entero.')

                
            
                
       
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
            ("EMPLEADOS", lambda: self.ver_tabla('empleados')),
            ("PRODUCTOS", lambda: self.ver_tabla('producto')),
            ("DETALLES PEDIDOS", lambda: self.ver_tabla('detallespedido')),
            ("PEDIDOS", lambda: self.ver_tabla('pedidos')),
            ("PAGOS", lambda: self.ver_tabla('pagos')),
        ]

        self.comandos_agregar = [
            ("CLIENTES", lambda: self.metodo_agregar('clientes')),
            ("EMPLEADOS", lambda: self.metodo_agregar('empleados')),
            ("PRODUCTOS", lambda: self.metodo_agregar('producto')),
            ("DETALLES PEDIDOS", lambda: self.metodo_agregar('detallespedido')),
            ("PEDIDOS", lambda: self.metodo_agregar('pedidos')),
            ("PAGOS", lambda: self.metodo_agregar('pagos')),
        ]

        self.comandos_modificar = [
            ("CLIENTES", lambda: self.metodo_modificar('clientes')),
            ("EMPLEADOS", lambda: self.metodo_modificar('empleados')),
            ("PRODUCTOS", lambda: self.metodo_modificar('producto')),
            ("DETALLES PEDIDOS", lambda: self.metodo_modificar('detallespedido')),
            ("PEDIDOS", lambda: self.metodo_modificar('pedidos')),
            ("PAGOS", lambda: self.metodo_modificar('pagos')),
        ]

        self.comandos_eliminar = [
            ("CLIENTES", lambda: self.metodo_eliminar('clientes')),
            ("EMPLEADOS", lambda: self.metodo_eliminar('empleados')),
            ("PRODUCTOS", lambda: self.metodo_eliminar('producto')),
            ("DETALLES PEDIDOS", lambda: self.metodo_eliminar('detallespedido')),
            ("PEDIDOS", lambda: self.metodo_eliminar('pedidos')),
            ("PAGOS", lambda: self.metodo_eliminar('pagos')),
        ]
        
        #creacion de la interfaz principal
        self.bloque_principal=Frame(self,bg="#F5EDE1")
        self.bloque_principal.place(x=20,y=20,height=355,width=150)
        self.ver=Button(self.bloque_principal,text="VER",bg="#C19A6B",command=lambda:self.ocultar_mostrar(self.bloque_principal,self.interfaz_vista))
        self.ver.place(x=7,y=10,height=80,width=135) 
        self.agregar=Button(self.bloque_principal,text="AGREGAR",bg="#C19A6B",command=lambda:self.ocultar_mostrar(self.bloque_principal,self.interfaz_agregar))
        self.agregar.place(x=7,y=95,height=80,width=135)
        self.modificar=Button(self.bloque_principal,text="MODIFICAR",bg="#C19A6B",command=lambda:self.ocultar_mostrar(self.bloque_principal,self.interfaz_modificar))
        self.modificar.place(x=7,y=180,height=80,width=135)
        self.eliminar=Button(self.bloque_principal,text="ELIMINAR",bg="#C19A6B",command=lambda:self.ocultar_mostrar(self.bloque_principal,self.interfaz_eliminar))
        self.eliminar.place(x=7,y=265,height=80,width=135)
        
        #creacion de las diferentes vistas de las interfaces
        self.interfaz_vista=self.crear_interfaz(self.comandos_ver)        
        self.interfaz_agregar=self.crear_interfaz(self.comandos_agregar)
        self.interfaz_modificar=self.crear_interfaz(self.comandos_modificar)
        self.interfaz_eliminar=self.crear_interfaz(self.comandos_eliminar)
        
        #creacion del formulario
        self.Formulario=Frame(self,bg="#E3E1DC")
        
        #creacion del treeview (hace que se vea la base de datos)
        self.vista_database=ttk.Treeview(self)
        self.vista_database.place(x=220,y=18,width=600,height=355)
   
        
def mainDBA():
    # Crear la ventana principal
    raiz=Tk()
    raiz.wm_title("Cafetería")

    app=Interfaz(raiz)

    app.mainloop()