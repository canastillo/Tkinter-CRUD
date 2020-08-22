from tkinter import ttk
from tkinter import *
import sqlite3

class Product:
    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Products Application')

        self.create_interface()

    def create_interface(self):
        self.label_messages()
        self.table_products()
        self.actions_buttons()


    #Tabla de productos
    def table_products(self): #Crea la tabla de productos
        # Tabla
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER)

        self.get_products()

    def get_products(self): #Consulta los productos a la bd
            self.clean_table()

            query = 'SELECT * FROM PRODUCT'
            db_rows = self.run_query(query)

            for row in db_rows:
                self.tree.insert('', 0, text = row[1], values = row[2])

    def clean_table(self): #Vacía la tabla de productos
        records = self.tree.get_children()
        for record in records:
            self.tree.delete(record)

    def actions_buttons(self): #Creación botones eliminar y editar
        ttk.Button(text = 'Eliminar', command = self.delete_product).grid(row = 6, column = 0, sticky = W + E)
        ttk.Button(text = 'Editar', command = self.edit_product).grid(row = 6, column = 1, sticky = W + E)
        ttk.Button(text = 'Nuevo producto', command = self.form_new_product).grid(row = 5, column = 0, sticky = W + E)

    def delete_product(self):
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.messages['text'] = 'Seleccione un producto'
            return
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM PRODUCT WHERE name = ?'
        self.run_query(query, (name, ))
        self.messages['text'] = 'Producto eliminado'
        self.get_products()

    def edit_product(self):
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.messages['text'] = 'Seleccione un producto'
            return
        
        self.form_edit()
    

    # Ventana Editar producto
    def form_edit(self):
        name = self.tree.item(self.tree.selection())['text']
        price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar producto'

        Label(self.edit_wind, text = 'Nombre: ').grid(row = 0, column = 1)
        self.edit_wind.name = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value= name))
        self.edit_wind.name.grid(row = 0, column = 2)
        
        Label(self.edit_wind, text = 'Precio: ').grid(row = 1, column = 1)
        self.edit_wind.price = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value= price))
        self.edit_wind.price.grid(row = 1, column = 2)

        ttk.Button(self.edit_wind, text = 'Guardar', command = lambda: self.change_product(name, price)).grid(row = 4, column = 2, sticky = W)

    def change_product(self, name, price):
        if self.validate_product(self.edit_wind.name.get(), self.edit_wind.price.get()):
            self.update_product(name, price, self.edit_wind.name.get(), self.edit_wind.price.get())

    def update_product(self, name, price, nname, nprice):
        query = 'UPDATE PRODUCT SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (nname, nprice, name, price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.messages['text'] ='Producto actualizado exitosamente'
        self.get_products()


    #Formulario nuevo producto
    def form_new_product(self): #Crea el formulario para un nuevo producto
        self.add_wind = Toplevel()
        self.add_wind.title = 'Agregar producto'

        frame = LabelFrame(self.add_wind, text = 'Registre un nuevo producto')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Input nombre
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # Input precio
        Label(frame, text = 'Precio: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)
        
        # Botón Agregar producto
        ttk.Button(frame, text = 'Agregar producto', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

    def add_product(self): #Inserta un producto a la bd
        if self.validate_product(self.name.get(), self.price.get()):
            try:
                self.insert_product()
                self.messages['text'] = '{} registrado exitosamente'.format(self.name.get())
                self.get_products()
                self.add_wind.destroy()
            except:
                self.messages['text'] = 'El producto no pudo ser registrado'.format(self.name.get())
        else:
            self.messages['text'] = 'Rellene todos los campos'

    def validate_product(self, name, price): #Valida que los campos estén llenos
        return len(name) > 0 and len(price) > 0

    def insert_product(self):
        query = 'INSERT INTO PRODUCT VALUES(NULL, ?, ?)'
        parameters = (self.name.get(), self.price.get())
        self.run_query(query, parameters)

    def label_messages(self): #Crea el label de notificaciones
        self.messages = Label(text = '', fg = 'gray')
        self.messages.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

    def clean_form(self): #Vacía los campos del formulario
        self.name.delete(0, END)
        self.price.delete(0, END)


    # Base de datos
    def run_query(self, query, parameters = ()): #Ejecuta consultas
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result    
    
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()