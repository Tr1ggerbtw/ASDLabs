import tkinter as tk
import random
import math

n1, n2, n3, n4 = 4, 1, 1, 2
seed = int(f"{n1}{n2}{n3}{n4}")
n = 10 + n3

width = 800
height = 600
margin = 50

random.seed(seed)
T = [[random.uniform(0, 2.0) for _ in range(n)] for _ in range(n)]
k = 1.0 - n3 * 0.02 - n4 * 0.005 - 0.25
directed_adj_matrix = [[1 if T[i][j] * k >= 1.0 else 0 for j in range(n)] for i in range(n)]


undirected_adj_matrix = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if directed_adj_matrix[i][j] == 1 or directed_adj_matrix[j][i] == 1:
            undirected_adj_matrix[i][j] = 1
            undirected_adj_matrix[j][i] = 1


def get_vertex_positions(n, width, height, margin):
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    positions = []
    cell_w = (width - 2 * margin) / cols
    cell_h = (height - 2 * margin) / rows
    for i in range(n):
        col = i % cols
        row = i // cols
        x = margin + col * cell_w + cell_w / 2
        y = margin + row * cell_h + cell_h / 2
        positions.append((x, y))
    return positions


def draw_graph(canvas, A, directed=False):
    canvas.delete("all")
    radius = 20
    positions = get_vertex_positions(n, width, height, margin)


    for i in range(n):
        for j in range(n):
            if A[i][j]:
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                dx, dy = x2 - x1, y2 - y1
                dist = math.hypot(dx, dy)
                if dist == 0:
                    continue
                offset_x = radius * dx / dist
                offset_y = radius * dy / dist
                start = (x1 + offset_x, y1 + offset_y)
                end = (x2 - offset_x, y2 - offset_y)
                canvas.create_line(*start, *end, arrow=tk.LAST if directed else tk.NONE, width=2)


    for i, (x, y) in enumerate(positions):
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue")
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12, "bold"))


def print_matrix(matrix, matrix_name):
    print(f"\n{matrix_name}:")
    n = len(matrix)
    
    header = "    " + " ".join(f"{i:2}" for i in range(n))
    print(header)
    print("   " + "-" * (3 * n))

    for i, row in enumerate(matrix):
        row_str = " ".join(f"{val:2}" for val in row)
        print(f"{i:2} | {row_str}")

def show_directed():
    draw_graph(canvas, directed_adj_matrix, directed=True)


def show_undirected():
    draw_graph(canvas, undirected_adj_matrix, directed=False)


root = tk.Tk()
root.title("Graph")
canvas = tk.Canvas(root, width=width, height=height, bg="white")
canvas.pack()


button_frame = tk.Frame(root)
button_frame.pack()
tk.Button(button_frame, text="Directed", command=show_directed).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Undirected", command=show_undirected).pack(side=tk.LEFT, padx=10)


print_matrix(directed_adj_matrix, "Directed Adjacency Matrix")
print_matrix(undirected_adj_matrix, "Undirected Adjacency Matrix")


show_directed()  


root.mainloop()