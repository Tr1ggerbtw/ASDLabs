import math
import tkinter as tk
import random

n3 = 1
n4 = 2
vertexes = n3 + 10
variant = 4112
random.seed(variant)
k = 1 - n3 * 0.01 - n4 * 0.005 - 0.05

def calculate_element(k):
    return math.floor(random.random() * 2 * k)

matrix_dir = [[0] * vertexes for _ in range(vertexes)]
matrix_undir = [[0] * vertexes for _ in range(vertexes)]

for i in range(vertexes):
    for j in range(vertexes):
        matrix_dir[i][j] = calculate_element(k)

for i in range(vertexes):
    for j in range(vertexes):
        matrix_undir[i][j] = matrix_dir[i][j] or matrix_dir[j][i]

def print_array(arr, text, separator):
    print(text, end=" ")
    if len(arr) == 0:
        print("no such vertexes")
    else:
        for i in range(len(arr)):
            print(arr[i], end=separator)
        print()

def print_matrix(matrix):
    for row in matrix:
        for element in row:
            print(element, end=" ")
        print()

def matrix_multiply(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] + B[i][j]
    return result

def get_weights(matrix_undir):
    vertexes = len(matrix_undir)
    B = [[random.random() * 2 for _ in range(vertexes)] for _ in range(vertexes)]
    C = [[math.ceil(100 * B[i][j] * matrix_undir[i][j]) for j in range(vertexes)] for i in range(vertexes)]
    D = [[1 if C[i][j] > 0 else 0 for j in range(vertexes)] for i in range(vertexes)]
    H = [[1 if D[i][j] != D[j][i] else 0 for j in range(vertexes)] for i in range(vertexes)]
   
    W = [[0]*vertexes for _ in range(vertexes)]
    for i in range(vertexes):
        for j in range(vertexes):
            val = C[i][j] * (D[i][j] + H[i][j] * (i < j))
            if i == j:
                W[i][j] = W[j][i] = 0
            elif val == 0:
                W[i][j] = W[j][i] = math.inf
            else:
                W[i][j] = W[j][i] = val
    return W

def get_edges(matrix, weights):
    edges = []
    size = len(matrix)
    for i in range(size):
        for j in range(i + 1, size):
            if matrix[i][j] == 1:
                edges.append((i, j, weights[i][j]))
    return edges

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            self.parent[root_v] = root_u
            return True
        return False

def kruskal(matrix, weights):
    edges = get_edges(matrix, weights)
    edges.sort(key=lambda x: x[2])
    uf = UnionFind(len(matrix))
    mst_edges = []

    for u, v, weight in edges:
        if uf.union(u, v):
            mst_edges.append((u, v))
    return mst_edges

print("\nUndirected matrix:\n")
print_matrix(matrix_undir)

W = get_weights(matrix_undir)

print("\nW:\n")
for row in W:
    print(" ".join(f"{num:4}" if num != math.inf else " inf" for num in row))

edges = get_edges(matrix_undir, W)
mst = kruskal(matrix_undir, W)

print_array(edges, "Edges: ", ", ")
print_array(mst, "MST: ", ", ")

WIDTH_CANVAS = 800
HEIGHT_CANVAS = 800
MARGIN = 50
R = 20

root = tk.Tk()
root.title("Graph - Kruskal's Algorithm (Step-by-step)")

canvas = tk.Canvas(root, width=WIDTH_CANVAS, height=HEIGHT_CANVAS, bg="white")
canvas.pack()

def get_vertex_positions(n_verts, width_canvas, height_canvas, margin_canvas):
    pw, ph = width_canvas - 2 * margin_canvas, height_canvas - 2 * margin_canvas
    if n_verts == 0: return []
    if n_verts == 1: return [(margin_canvas + pw / 2, margin_canvas + ph / 2)]

    perim = 2 * (pw + ph)
    step = perim / n_verts if perim > 0 else 0
    
    dist = 0
    pos = []
    for _ in range(n_verts):
        current_x, current_y = 0, 0
        if dist < pw:
            current_x, current_y = dist, 0
        elif dist < pw + ph:
            current_x, current_y = pw, dist - pw
        elif dist < 2 * pw + ph:
            current_x, current_y = pw - (dist - pw - ph), ph
        else:
            current_x, current_y = 0, ph - (dist - 2 * pw - ph)
        pos.append((current_x + margin_canvas, current_y + margin_canvas))
        dist += step
    return pos

vertex_pos = get_vertex_positions(vertexes, WIDTH_CANVAS, HEIGHT_CANVAS, MARGIN)

def draw_graph(matrix, paths, weights):
    for i in range(vertexes):
        for j in range(vertexes):
            if matrix[i][j] == 1 and i <= j: 
                x1, y1 = vertex_pos[i]
                x2, y2 = vertex_pos[j]

                if i == j:  
                    canvas.create_line(
                        x1, y1 - R,
                        x1 + R * 1.2, y1 - R * 2.2,
                        x1 - R * 1.2, y1 - R * 2.2,
                        x1 - R * 0.1, y1 - R,
                        smooth=tk.TRUE, width=2, fill="black"
                    )
                else:
                    dx, dy = x2 - x1, y2 - y1
                    length = math.hypot(dx, dy)
                    if length == 0:
                        ctrl_x, ctrl_y = (x1 + x2) / 2, (y1 + y2) / 2
                    else:
                        norm_dx, norm_dy = -dy / length, dx / length
                        bulge = 30  
                        ctrl_x = (x1 + x2) / 2 + norm_dx * bulge
                        ctrl_y = (y1 + y2) / 2 + norm_dy * bulge

                    canvas.create_line(x1, y1, ctrl_x, ctrl_y, x2, y2, smooth=True, width=2, fill="black", tags="edges")

                    if weights[i][j] != 0 and weights[i][j] != math.inf:
                        mx, my = ctrl_x, ctrl_y
                        size = 9
                        canvas.create_rectangle(mx - size - 1, my - size - 1, mx + size + 5, 
                                                my + size + 1, fill="#DDDDDD", outline="black", tags="bg")
                        canvas.create_text(mx, my, text=str(weights[i][j]), 
                                           font=("Montserrat", size), fill="black", tags="weight_text")

    for i in range(vertexes):
        x, y = vertex_pos[i]
        canvas.create_oval(x - R, y - R, x + R, y + R, fill="white", outline="black")
        canvas.create_text(x, y, text=str(i + 1), font=("Montserrat", 12))

    visited_vertices = [False] * vertexes
    total_weight = [0]
    step_index = [0]

    total_text_id = canvas.create_text(WIDTH_CANVAS - 100, 30, 
                                       text=f"Total weight: 0", font=("Montserrat", 12), fill="black")

    def highlight_next_step(event=None):
        k = step_index[0]
        if k >= len(paths):
            return

        i, j = paths[k]
        total_weight[0] += weights[i][j]
        canvas.itemconfig(total_text_id, text=f"Total weight: {total_weight[0]}")

        x1, y1 = vertex_pos[i]
        x2, y2 = vertex_pos[j]

        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy)
        if length == 0:
            ctrl_x, ctrl_y = (x1 + x2) / 2, (y1 + y2) / 2
        else:
            norm_dx, norm_dy = -dy / length, dx / length
            bulge = 30
            ctrl_x = (x1 + x2) / 2 + norm_dx * bulge
            ctrl_y = (y1 + y2) / 2 + norm_dy * bulge

        canvas.create_line(x1, y1, ctrl_x, ctrl_y, x2, y2, smooth=True, width=3, fill="orange", tags="mst_edge")

        for v in [i, j]:
            if not visited_vertices[v]:
                visited_vertices[v] = True
                x, y = vertex_pos[v]
                canvas.create_oval(x - R, y - R, x + R, y + R, fill="orange", outline="black")
                canvas.create_text(x, y, text=str(v + 1), font=("Montserrat", 12))

        mx, my = ctrl_x, ctrl_y
        size = 9
        canvas.create_rectangle(mx - size - 1, my - size - 1, mx + size + 5, 
                                my + size + 1, fill="orange", outline="black")
        canvas.create_text(mx, my, text=str(weights[i][j]), 
                           font=("Montserrat", size), fill="black")

        step_index[0] += 1

    button = tk.Button(root, text="Наступний крок", command=highlight_next_step)
    button.pack(pady=10)

    root.bind("<Return>", highlight_next_step)
    root.bind("n", highlight_next_step)

draw_graph(matrix_undir, mst, W)
root.mainloop()
