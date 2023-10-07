from tkinter import *
from PIL import Image, ImageTk
import os
from tkinter.filedialog import askopenfilename

class RecortadorDeImagen:
    def _init_(self, root):
        self.root = root
        self.root.title("Recortador de Imágenes")
        
        self.imagenes = []
        self.imagen_actual = 0
        
        self.canvas = Canvas(root)
        self.canvas.pack()
        
        self.left = IntVar()
        self.top = IntVar()
        self.right = IntVar()
        self.bottom = IntVar()
        
        self.left_label = Label(root, text="Izquierda:")
        self.left_label.pack()
        self.left_entry = Entry(root, textvariable=self.left)
        self.left_entry.pack()
        
        self.top_label = Label(root, text="Arriba:")
        self.top_label.pack()
        self.top_entry = Entry(root, textvariable=self.top)
        self.top_entry.pack()
        
        self.right_label = Label(root, text="Derecha:")
        self.right_label.pack()
        self.right_entry = Entry(root, textvariable=self.right)
        self.right_entry.pack()
        
        self.bottom_label = Label(root, text="Abajo:")
        self.bottom_label.pack()
        self.bottom_entry = Entry(root, textvariable=self.bottom)
        self.bottom_entry.pack()
        
        self.cargar_boton = Button(root, text="Cargar Imagen", command=self.cargar_imagen)
        self.cargar_boton.pack()
        
        self.recortar_boton = Button(root, text="Recortar", command=self.recortar_imagen)
        self.recortar_boton.pack()
        
    def cargar_imagen(self):
        imagen_path = askopenfilename(filetypes=[("Imágenes", "*.jpg *.png")])
        if imagen_path:
            imagen = Image.open(imagen_path)
            self.imagenes.append(imagen)
            self.imagen_actual = len(self.imagenes) - 1
            self.actualizar_canvas()
    
    def recortar_imagen(self):
        left = self.left.get()
        top = self.top.get()
        right = self.right.get()
        bottom = self.bottom.get()
        
        if self.imagen_actual < len(self.imagenes):
            imagen_actual = self.imagenes[self.imagen_actual]
            imagen_recortada = imagen_actual.crop((left, top, right, bottom))
            imagen_recortada.show()
        
    def actualizar_canvas(self):
        if self.imagen_actual < len(self.imagenes):
            imagen_actual = self.imagenes[self.imagen_actual]
            imagen_actual.thumbnail((600, 400))  # Ajusta el tamaño para que quepa en el canvas
            self.imagen_original = ImageTk.PhotoImage(imagen_actual)
            self.canvas.config(width=imagen_actual.width, height=imagen_actual.height)
            self.canvas.create_image(0, 0, anchor=NW, image=self.imagen_original)

if __name__ == "_main_":
    root = Tk()
    app = RecortadorDeImagen(root)
    root.mainloop()