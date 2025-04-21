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
    positions = []
    plot_width = width - 2 * margin
    plot_height = height - 2 * margin
    perimeter = 2 * (plot_width + plot_height)
    step = perimeter / n

    current_dist = 0
    for i in range(n):
        x, y = 0, 0 # 

        if current_dist < plot_width: 
            x = current_dist
            y = 0
        elif current_dist < plot_width + plot_height:
            dist_on_edge = current_dist - plot_width
            x = plot_width
            y = dist_on_edge
        elif current_dist < 2 * plot_width + plot_height: 
            dist_on_edge = current_dist - (plot_width + plot_height)
            x = plot_width - dist_on_edge
            y = plot_height
        else: 
            dist_on_edge = current_dist - (2 * plot_width + plot_height)
            x = 0
            y = plot_height - dist_on_edge

        positions.append((x + margin, y + margin))

        current_dist += step

    return positions

def draw_graph(canvas, A, directed=False):
    canvas.delete("all")
    radius = 20
    edge_offset = 15
    loop_radius = 15  

    positions = get_vertex_positions(n, width, height, margin)

    for i in range(n):
        for j in range(n):
            if A[i][j]:
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                if i == j:

                    canvas.create_oval(
                        x1 - radius, y1 - radius - loop_radius,
                        x1 + radius, y1 + radius - loop_radius,
                        outline="gray", width=2
                    )
                    if directed:
                        canvas.create_line(
                            x1, y1 - radius - loop_radius,
                            x1, y1 - radius - loop_radius - 10,
                            arrow=tk.LAST, fill="gray", width=2
                        )
                    continue

                dx, dy = x2 - x1, y2 - y1
                dist = math.hypot(dx, dy)

                if dist == 0:
                    continue

                offset_x = radius * dx / dist
                offset_y = radius * dy / dist
                start = (x1 + offset_x, y1 + offset_y)
                end = (x2 - offset_x, y2 - offset_y)

                if directed:
                    pdx, pdy = -dy, dx
                    p_dist = math.hypot(pdx, pdy)
                    if p_dist > 0:
                        n_pdx, n_pdy = pdx / p_dist, pdy / p_dist
                    else:
                        n_pdx, n_pdy = 0, 0

                    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                    cp_x = mid_x + edge_offset * n_pdx
                    cp_y = mid_y + edge_offset * n_pdy

                    canvas.create_line(start[0], start[1], cp_x, cp_y, end[0], end[1],
                                       smooth=tk.TRUE, arrow=tk.LAST, width=2, fill="gray")
                else:
                    canvas.create_line(*start, *end, width=2, fill="gray")

    for i, (x, y) in enumerate(positions):
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue", outline="blue")
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
root.title("Візуалізація графа")

canvas = tk.Canvas(root, width=width, height=height, bg="white")
canvas.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=10) 


tk.Button(button_frame, text="Directed", command=show_directed).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Undirected", command=show_undirected).pack(side=tk.LEFT, padx=10)


print_matrix(directed_adj_matrix, "Directed matrix")
print_matrix(undirected_adj_matrix, "Undirected matrix")


show_directed()


root.mainloop()