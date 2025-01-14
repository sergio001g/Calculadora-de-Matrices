import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import numpy as np
from fractions import Fraction
from PIL import Image, ImageDraw, ImageTk
import io

class AdvancedMatrixCalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculadora de Matrices")
        self.master.geometry("800x700")
        
        self.show_fractions = tk.BooleanVar(value=False)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.create_matrix_input_tab()
        self.create_operations_tab()
        self.create_visualization_tab()
        
    def create_matrix_input_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Entrada de Matriz")
        
        self.size_var = tk.StringVar(value="3x3")
        ttk.Label(tab, text="Tamaño de la matriz:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Combobox(tab, textvariable=self.size_var, values=["2x2", "3x3", "4x4"]).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(tab, text="Crear matriz", command=self.create_matrix_entries).grid(row=0, column=2, padx=5, pady=5)
        
        self.matrix_frame = ttk.Frame(tab)
        self.matrix_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        self.entries = []
        
    def create_matrix_entries(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        
        size = int(self.size_var.get()[0])
        self.entries = []
        for i in range(size):
            row = []
            for j in range(size):
                entry = ttk.Entry(self.matrix_frame, width=8)
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.bind("<KeyRelease>", self.on_entry_key)
                row.append(entry)
            self.entries.append(row)
        
        self.entries[0][0].focus_set()
    
    def on_entry_key(self, event):
        widget = event.widget
        row = widget.grid_info()["row"]
        col = widget.grid_info()["column"]
        size = len(self.entries)
        
        if event.keysym == "Right" and col < size - 1:
            self.entries[row][col + 1].focus_set()
        elif event.keysym == "Left" and col > 0:
            self.entries[row][col - 1].focus_set()
        elif event.keysym == "Down" and row < size - 1:
            self.entries[row + 1][col].focus_set()
        elif event.keysym == "Up" and row > 0:
            self.entries[row - 1][col].focus_set()
    
    def create_operations_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Operaciones")
        
        operations = [
            ("Suma", self.matrix_sum),
            ("Resta", self.matrix_subtraction),
            ("Multiplicación", self.matrix_multiplication),
            ("Inversión", self.calculate_inverse),
            ("Rango", self.calculate_rank)
        ]
        
        for i, (text, command) in enumerate(operations):
            ttk.Button(tab, text=text, command=command).grid(row=i//3, column=i%3, padx=5, pady=5, sticky='ew')
            
    def matrix_sum(self):
        matrix1 = self.get_matrix()
        if matrix1 is not None:
            matrix2 = self.get_second_matrix()
            if matrix2 is not None:
                result = matrix1 + matrix2
                steps = [
                    "Suma de matrices:",
                    f"Matriz 1:\n{matrix1}",
                    f"Matriz 2:\n{matrix2}",
                    "Proceso de suma:",
                ]
                for i in range(len(matrix1)):
                    for j in range(len(matrix1[0])):
                        steps.append(f"Posición [{i},{j}]: {matrix1[i][j]} + {matrix2[i][j]} = {result[i][j]}")
                steps.append(f"Resultado final:\n{result}")
                self.display_result("Suma de Matrices", result, steps)

    def matrix_subtraction(self):
        matrix1 = self.get_matrix()
        if matrix1 is not None:
            matrix2 = self.get_second_matrix()
            if matrix2 is not None:
                result = matrix1 - matrix2
                steps = [
                    "Resta de matrices:",
                    f"Matriz 1:\n{matrix1}",
                    f"Matriz 2:\n{matrix2}",
                    "Proceso de resta:",
                ]
                for i in range(len(matrix1)):
                    for j in range(len(matrix1[0])):
                        steps.append(f"Posición [{i},{j}]: {matrix1[i][j]} - {matrix2[i][j]} = {result[i][j]}")
                steps.append(f"Resultado final:\n{result}")
                self.display_result("Resta de Matrices", result, steps)

    def matrix_multiplication(self):
        matrix1 = self.get_matrix()
        if matrix1 is not None:
            matrix2 = self.get_second_matrix()
            if matrix2 is not None:
                result = np.matmul(matrix1, matrix2)
                steps = [
                    "Multiplicación de matrices:",
                    f"Matriz 1:\n{matrix1}",
                    f"Matriz 2:\n{matrix2}",
                    "Proceso de multiplicación:",
                ]
                for i in range(len(matrix1)):
                    for j in range(len(matrix2[0])):
                        element = 0
                        for k in range(len(matrix1[0])):
                            element += matrix1[i][k] * matrix2[k][j]
                        steps.append(f"Posición [{i},{j}]: {element}")
                steps.append(f"Resultado final:\n{result}")
                self.display_result("Multiplicación de Matrices", result, steps)

    def get_second_matrix(self):
        second_matrix = simpledialog.askstring("Segunda Matriz", "Ingrese la segunda matriz (separar filas con ';' y elementos con ',')")
        if second_matrix:
            try:
                return np.array([list(map(float, row.split(','))) for row in second_matrix.split(';')])
            except ValueError:
                messagebox.showerror("Error", "Formato de matriz inválido")
        return None
    
    def create_visualization_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Visualización")
        
        ttk.Checkbutton(tab, text="Mostrar como fracciones", variable=self.show_fractions, 
                    command=self.update_result_display).pack(pady=5)
        
        self.result_text = tk.Text(tab, height=30, width=100)
        self.result_text.pack(padx=10, pady=10)
    
    def get_matrix(self):
        try:
            return np.array([[self.parse_fraction(entry.get()) for entry in row] for row in self.entries])
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese solo números válidos o fracciones.")
            return None
    
    def parse_fraction(self, s):
        try:
            return float(s)
        except ValueError:
            return float(Fraction(s))
    
    def format_number(self, num):
        if self.show_fractions.get():
            return str(Fraction(num).limit_denominator())
        else:
            return f"{num:.6f}"
    
    def display_result(self, title, result, steps=None):
        self.result = result  # Guardar el resultado para actualizaciones posteriores
        self.result_steps = steps
        self.result_title = title
        self.update_result_display()
    
    def update_result_display(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"{self.result_title}:\n\n")
        
        if self.result_steps:
            self.result_text.insert(tk.END, "Pasos:\n")
            for i, step in enumerate(self.result_steps, 1):
                self.result_text.insert(tk.END, f"{i}. {step}\n")
            self.result_text.insert(tk.END, "\nResultado final:\n")
        
        if isinstance(self.result, np.ndarray):
            for row in self.result:
                self.result_text.insert(tk.END, " ".join(self.format_number(x) for x in row) + "\n")
        else:
            self.result_text.insert(tk.END, self.format_number(self.result) + "\n")
    
    def calculate_inverse(self):
        matrix = self.get_matrix()
        if matrix is not None:
            try:
                steps = [
                    "Método de Gauss-Jordan para calcular la inversa:",
                    f"Matriz original:\n{matrix}",
                ]
                n = len(matrix)
                augmented = np.hstack((matrix, np.eye(n)))
                steps.append(f"Matriz aumentada:\n{augmented}")
                
                for i in range(n):
                    pivot = augmented[i][i]
                    if pivot == 0:
                        raise np.linalg.LinAlgError("La matriz no es invertible")
                    augmented[i] = augmented[i] / pivot
                    steps.append(f"Normalizar fila {i+1}:\n{augmented}")
                    for j in range(n):
                        if i != j:
                            factor = augmented[j][i]
                            augmented[j] -= factor * augmented[i]
                            steps.append(f"Eliminar elemento en fila {j+1}, columna {i+1}:\n{augmented}")
                
                inv = augmented[:, n:]
                steps.append(f"Matriz inversa resultante:\n{inv}")
                self.display_result("Matriz Inversa", inv, steps)
            except np.linalg.LinAlgError as e:
                messagebox.showerror("Error", str(e))
    
    def calculate_rank(self):
        matrix = self.get_matrix()
        if matrix is not None:
            steps = [
                "Cálculo del rango:",
                f"Matriz original:\n{matrix}",
                "1. Aplicar eliminación Gaussiana para obtener la forma escalonada reducida"
            ]
            rank = np.linalg.matrix_rank(matrix)
            steps.append(f"2. Contar el número de filas no nulas: {rank}")
            self.display_result("Rango", rank, steps)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedMatrixCalculator(root)
    root.mainloop()

