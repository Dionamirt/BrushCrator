import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import random

class SimpleApp:
    def __init__(self, master):
        self.master = master
        self.master.title("IMGgen")

        self.images = [None, None, None]
        self.current_zoom = 1.0  # Fator de zoom inicial
        self.button_states = [False] * 5  # Estados dos botões numerados
        self.buttons = []  # Lista de referência aos botões

        # Configuração das colunas
        for i in range(3):
            self.master.grid_columnconfigure(i, weight=1)

        # Grade principal com os canvases
        self.canvas1 = Canvas(master, width=200, height=200, bg='white')
        self.canvas1.grid(row=1, column=0, padx=10, pady=5)

        self.canvas2 = Canvas(master, width=200, height=200, bg='white')
        self.canvas2.grid(row=1, column=1, padx=10, pady=5)

        self.canvas3 = Canvas(master, width=200, height=200, bg='white')
        self.canvas3.grid(row=1, column=2, padx=10, pady=5)

        # Botões de geração de imagem
        self.gen_button1 = tk.Button(master, text="Gen1", command=self.generate_image_gen1, width=3)
        self.gen_button1.grid(row=2, column=0, pady=5, sticky='ew')

        self.gen_button2 = tk.Button(master, text="Gen2", command=self.generate_image_gen2, width=3)
        self.gen_button2.grid(row=2, column=1, pady=5, sticky='ew')

        self.gen_button3 = tk.Button(master, text="Gen3", command=self.generate_image_gen3, width=3)
        self.gen_button3.grid(row=2, column=2, pady=5, sticky='ew')

        # Grid para os botões numerados
        self.button_frame = tk.Frame(master)
        self.button_frame.grid(row=0, column=0, columnspan=3, pady=5, sticky='ew')

        # Criação dos botões numerados 1 a 5
        for i in range(5):
            button = tk.Button(self.button_frame, text=str(i + 1), width=2,
                               command=lambda i=i: self.toggle_button(i))
            button.grid(row=0, column=i, padx=2)
            self.buttons.append(button)  # Armazena o botão

        # Scroll para zoom
        self.scrollbar = tk.Scale(master, from_=1, to=5, orient=tk.HORIZONTAL, resolution=0.1, command=self.update_zoom_from_scroll)
        self.scrollbar.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

    def toggle_button(self, index):
        """Alterna o estado do botão especificado e altera sua aparência."""
        self.button_states[index] = not self.button_states[index]
        button = self.buttons[index]
        if self.button_states[index]:
            button.config(bg='lightgreen')  # Cor para ativo
        else:
            button.config(bg='lightgray')  # Cor para desativo

        # Atualiza o zoom de acordo com o botão ativo
        self.current_zoom = (index + 1) * 0.5  # Exemplo de zoom simples
        self.update_zoom()

    def update_zoom_from_scroll(self, value):
        """Atualiza o fator de zoom a partir do scroll."""
        self.current_zoom = float(value)
        self.update_zoom()

    def update_zoom(self):
        """Aplica o zoom às imagens de acordo com o fator de zoom atual."""
        for i in range(3):
            if self.images[i]:
                self.display_image(self.images[i], self.get_canvas(i))

    def generate_image_gen1(self):
        """Gera uma imagem com linhas aleatórias no canvas 1."""
        self.images[0] = self.generate_lines(self.canvas1)

    def generate_image_gen2(self):
        """Gera uma imagem com círculos aleatórios no canvas 2."""
        self.images[1] = self.generate_circles(self.canvas2)

    def generate_image_gen3(self):
        """Gera uma imagem com quadrados aleatórios no canvas 3."""
        self.images[2] = self.generate_squares(self.canvas3)

    def generate_lines(self, canvas):
        """Gera linhas aleatórias no canvas."""
        img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
        for _ in range(10):
            x1 = random.randint(0, 200)
            y1 = random.randint(0, 200)
            x2 = random.randint(0, 200)
            y2 = random.randint(0, 200)
            for i in range(min(x1, x2), max(x1, x2) + 1):
                y = int(y1 + (y2 - y1) * (i - x1) / (x2 - x1)) if x2 != x1 else y1
                if 0 <= i < 200 and 0 <= y < 200:
                    img.putpixel((i, y), (0, 0, 0, 255))
        self.display_image(img, canvas)
        return img

    def generate_circles(self, canvas):
        """Gera círculos aleatórios no canvas."""
        img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
        for _ in range(10):
            x = random.randint(0, 200)
            y = random.randint(0, 200)
            r = random.randint(5, 20)
            for i in range(-r, r):
                for j in range(-r, r):
                    if i**2 + j**2 <= r**2:
                        if 0 <= x + i < 200 and 0 <= y + j < 200:
                            img.putpixel((x + i, y + j), (0, 0, 0, 255))
        self.display_image(img, canvas)
        return img

    def generate_squares(self, canvas):
        """Gera quadrados aleatórios no canvas."""
        img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
        for _ in range(10):
            x = random.randint(0, 170)
            y = random.randint(0, 170)
            size = random.randint(10, 30)
            for i in range(size):
                for j in range(size):
                    if 0 <= x + i < 200 and 0 <= y + j < 200:
                        img.putpixel((x + i, y + j), (0, 0, 0, 255))
        self.display_image(img, canvas)
        return img

    def display_image(self, img, canvas):
        """Exibe a imagem no canvas com o fator de zoom aplicado."""
        if img:
            zoomed_size = int(200 * self.current_zoom)
            img_resized = img.resize((zoomed_size, zoomed_size), Image.LANCZOS)
            brush_image = ImageTk.PhotoImage(img_resized)
            canvas.delete("all")
            canvas.create_image(0, 0, anchor='nw', image=brush_image)
            canvas.image = brush_image  # Referência para evitar coleta de lixo

    def get_canvas(self, index):
        """Retorna o canvas correspondente ao índice."""
        return [self.canvas1, self.canvas2, self.canvas3][index]

if __name__ == "__main__":
    root = tk.Tk()  # Cria a janela principal
    app = SimpleApp(root)  # Instancia o aplicativo
    root.mainloop()  # Inicia o loop principal da interface gráfica
