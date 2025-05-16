import math
import tkinter as tk
import random
from collections import deque

n3 = 1
n4 = 2
vertexes = n3 + 10

variant = 4112
random.seed(variant)

k = 1 - n3 * 0.01 - n4 * 0.005 - 0.15

def calculate_element(coefficient_k):
    return math.floor(random.random() * 2 * coefficient_k)

matrix_dir = [[0] * vertexes for _ in range(vertexes)]
for i in range(vertexes):
    for j in range(vertexes):
        matrix_dir[i][j] = calculate_element(k)

def print_matrix(matrix):
    for row in matrix:
        for element in row:
            print(element, end=" ")
        print()

def bfs_tree(matrix, start):
    print("\nBFS traversal order:")
    n = len(matrix)
    visited = set()
    tree = [[0] * n for _ in range(n)]
    queue = deque([start])
    visited.add(start)
    parent = [-1] * n
    paths = []
    order = 1
    vertex_order = {}

    while queue:
        node = queue.popleft()
        vertex_order[node] = order
        print(f"{node + 1} -> {order}")
        order += 1

        for neighbor in range(n):
            if matrix[node][neighbor] == 1 and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                tree[node][neighbor] = 1
                parent[neighbor] = node
                paths.append([node, neighbor])
    return [tree, paths, vertex_order]

def dfs_tree(matrix, start):
    print("\nDFS traversal order:")
    n = len(matrix)
    visited = set()
    tree = [[0] * n for _ in range(n)]
    stack = [(start, -1)]
    paths = []
    order = 1
    vertex_order = {}

    while stack:
        node, p_node = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        vertex_order[node] = order
        print(f"{node + 1} -> {order}")
        order += 1

        if p_node != -1:
            tree[p_node][node] = 1
            paths.append([p_node, node])

        for neighbor in range(n - 1, -1, -1):
            if matrix[node][neighbor] == 1 and neighbor not in visited:
                stack.append((neighbor, node))
    return [tree, paths, vertex_order]

WIDTH_CANVAS = 800
HEIGHT_CANVAS = 800
MARGIN = 50
R = 20

root = tk.Tk()
root.title("Graph Traversal Visualization (Rectangular Layout)")
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

def draw_graph(matrix, bfs_paths_param, dfs_paths_param):
    canvas.delete("all")
    n = len(matrix)
    width_edge = 2
    curve_offset_val = 45
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                x1, y1 = vertex_pos[i]
                x2, y2 = vertex_pos[j]

                if i == j:
                    canvas.create_line(
                        x1, y1 - R,
                        x1 + R * 1.2, y1 - R * 2.2,
                        x1 - R * 1.2, y1 - R * 2.2,
                        x1 - R * 0.1, y1 - R,
                        smooth=tk.TRUE, arrow=tk.LAST, width=width_edge, fill="black"
                    )
                else:
                    dx, dy = x2 - x1, y2 - y1
                    dist = math.hypot(dx, dy)
                    if dist == 0: continue

                    dx_norm, dy_norm = dx / dist, dy / dist
                    sx, sy = x1 + dx_norm * R, y1 + dy_norm * R
                    ex, ey = x2 - dx_norm * R, y2 - dy_norm * R

                    mid_node_x, mid_node_y = (x1 + x2) / 2, (y1 + y2) / 2
                    cpx = mid_node_x - dy_norm * curve_offset_val
                    cpy = mid_node_y + dx_norm * curve_offset_val

                    canvas.create_line(sx, sy, cpx, cpy, ex, ey,
                                        smooth=tk.TRUE, arrow=tk.LAST, width=width_edge, fill="black")

    for i in range(n):
        x_coord, y_coord = vertex_pos[i]
        fill_color = "skyblue" if i == 0 else "white"
        outline_color = "blue"
        canvas.create_oval(x_coord - R, y_coord - R, x_coord + R, y_coord + R,
                            fill=fill_color, outline=outline_color, width=1.5)
        canvas.create_text(x_coord, y_coord, text=str(i + 1), font=("Montserrat", 12, "bold"))

    def highlight_path(paths, color="skyblue", k=0):
        if k == 0:
            canvas.delete("highlight")
            for idx in range(n):
                x_node, y_node = vertex_pos[idx]
                canvas.create_oval(x_node - R, y_node - R, x_node + R, y_node + R,
                                   fill="white", outline="blue", width=1.5, tags="highlight_node_base")
                canvas.create_text(x_node, y_node, text=str(idx + 1), font=("Montserrat", 12, "bold"), tags="highlight_node_base_text")
            start_node_x, start_node_y = vertex_pos[0]
            canvas.create_oval(start_node_x - R, start_node_y - R, start_node_x + R, start_node_y + R,
                               fill=color, outline="red", width=2, tags="highlight")
            canvas.create_text(start_node_x, start_node_y, text=str(1), font=("Montserrat", 12, "bold"), fill="black", tags="highlight")

        if k < len(paths):
            i_node, j_node = paths[k]
            x1_h, y1_h = vertex_pos[i_node]
            x2_h, y2_h = vertex_pos[j_node]

            if i_node == j_node:
                canvas.create_line(
                    x1_h, y1_h - R,
                    x1_h + R * 1.2, y1_h - R * 2.2,
                    x1_h - R * 1.2, y1_h - R * 2.2,
                    x1_h - R * 0.1, y1_h - R,
                    smooth=tk.TRUE, arrow=tk.LAST, width=3, fill=color, tags="highlight"
                )
            else:
                dx_h, dy_h = x2_h - x1_h, y2_h - y1_h
                dist_h = math.hypot(dx_h, dy_h)
                if dist_h == 0:
                    canvas.after(700, lambda: highlight_path(paths, color, k + 1))
                    return

                dx_norm_h, dy_norm_h = dx_h / dist_h, dy_h / dist_h
                sx_h, sy_h = x1_h + dx_norm_h * R, y1_h + dy_norm_h * R
                ex_h, ey_h = x2_h - dx_norm_h * R, y2_h - dy_norm_h * R

                mid_node_x_h, mid_node_y_h = (x1_h + x2_h) / 2, (y1_h + y2_h) / 2
                cpx_h = mid_node_x_h - dy_norm_h * curve_offset_val
                cpy_h = mid_node_y_h + dx_norm_h * curve_offset_val

                canvas.create_line(sx_h, sy_h, cpx_h, cpy_h, ex_h, ey_h,
                                   smooth=tk.TRUE, arrow=tk.LAST, width=3, fill=color, tags="highlight")

            xj_h, yj_h = vertex_pos[j_node]
            canvas.create_oval(xj_h - R, yj_h - R, xj_h + R, yj_h + R,
                               fill=color, outline="red", width=2, tags="highlight")
            canvas.create_text(xj_h, yj_h, text=str(j_node + 1), font=("Montserrat", 12, "bold"), fill="black", tags="highlight")
            canvas.after(700, lambda: highlight_path(paths, color, k + 1))

    tk.Button(root, text="Show BFS", command=lambda: highlight_path(bfs_paths_param, "skyblue")).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(root, text="Show DFS", command=lambda: highlight_path(dfs_paths_param, "skyblue")).pack(side=tk.LEFT, padx=5, pady=5)

print("Directed matrix (matrix_dir):\n")
print_matrix(matrix_dir)

bfs_tree_result = bfs_tree(matrix_dir, 0)
dfs_tree_result = dfs_tree(matrix_dir, 0)

print("\nBFS tree (adjacency matrix representation):\n")
print_matrix(bfs_tree_result[0])

print("\nDFS tree (adjacency matrix representation):\n")
print_matrix(dfs_tree_result[0])

print("\nBFS vertex processing order (vertex: order):")
print(bfs_tree_result[2])

print("\nDFS vertex processing order (vertex: order):")
print(dfs_tree_result[2])

draw_graph(matrix_dir, bfs_tree_result[1], dfs_tree_result[1])

root.mainloop()
