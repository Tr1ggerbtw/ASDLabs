import math
import tkinter as tk
import random

n1, n2, n3, n4 = 4, 1, 1, 2
SEED = int(f"{n1}{n2}{n3}{n4}")
vertexes = n3 + 10
width, height, margin, R = 800, 800, 50, 20
random.seed(SEED)
k1 = 1 - n3 * 0.01 - n4 * 0.01 - 0.3
k2 = 1 - n3 * 0.005 - n4 * 0.005 - 0.27

calculate_element = lambda k: math.floor(random.random() * 2 * k)
print_array = lambda arr, text, sep: print(text, "no such vertexes" if not arr else sep.join(map(str, arr)))
print_matrix = lambda m: [print(" ".join(map(str, row))) for row in m]

matrix_multiply = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(len(A))) for j in range(len(A))] for i in range(len(A))]
matrix_add = lambda A, B: [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]

matrix_dir = [[calculate_element(k1) for _ in range(vertexes)] for _ in range(vertexes)]
matrix_undir = [[matrix_dir[i][j] or matrix_dir[j][i] for j in range(vertexes)] for i in range(vertexes)]

root = tk.Tk()
canvas = tk.Canvas(root, width=width, height=height, bg="white")
canvas.pack()

def get_vertex_positions(n):
    pw, ph = width - 2 * margin, height - 2 * margin
    perim, step, dist = 2 * (pw + ph), 2 * (pw + ph) / n, 0
    pos = []
    for _ in range(n):
        if dist < pw: x, y = dist, 0
        elif dist < pw + ph: x, y = pw, dist - pw
        elif dist < 2 * pw + ph: x, y = pw - (dist - pw - ph), ph
        else: x, y = 0, ph - (dist - 2 * pw - ph)
        pos.append((x + margin, y + margin)); dist += step
    return pos

def draw_graph(matrix, n, directed):
    canvas.delete("all")
    pos = get_vertex_positions(n)
    for i, (x, y) in enumerate(pos):
        canvas.create_oval(x - R, y - R, x + R, y + R, fill="white", outline="blue")
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12, "bold"))
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                x1, y1, x2, y2 = *pos[i], *pos[j]
                if i == j:
                    if directed:
                        canvas.create_line(x1, y1 - R, x1 + 30, y1 - R - 30, x1 - 30, y1 - R - 30, x1 - 5, y1 - R + 5,
                                           smooth=tk.TRUE, arrow=tk.LAST, fill="gray", width=2)
                    else:
                        canvas.create_oval(x1 - R, y1 - R - 30, x1 + R, y1 + R - 30, outline="gray", width=2)
                else:
                    dx, dy = x2 - x1, y2 - y1
                    dist, dx, dy = math.hypot(dx, dy), dx / math.hypot(dx, dy), dy / math.hypot(dx, dy)
                    sx, sy = x1 + dx * R, y1 + dy * R
                    ex, ey = x2 - dx * R, y2 - dy * R
                    if directed:
                        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                        cpx, cpy = mx - dy * 15, my + dx * 15
                        canvas.create_line(sx, sy, cpx, cpy, ex, ey, smooth=tk.TRUE, arrow=tk.LAST, width=2, fill="gray")
                    else:
                        canvas.create_line(sx, sy, ex, ey, width=2, fill="gray")

def get_paths_length_2(A):
    A2 = matrix_multiply(A, A)
    return [[i, k, j] for i in range(len(A)) for j in range(len(A)) if A2[i][j] > 0 for k in range(len(A)) if A[i][k] and A[k][j]]

def get_paths_length_3(A):
    A3 = matrix_multiply(matrix_multiply(A, A), A)
    return [[i, k1, k2, j] for i in range(len(A)) for j in range(len(A)) if A3[i][j] > 0
            for k1 in range(len(A)) if A[i][k1] for k2 in range(len(A)) if A[k1][k2] and A[k2][j]]

def reachability_matrix(matrix):
    reach = power = [row[:] for row in matrix]
    for _ in range(len(matrix) - 1):
        power = matrix_multiply(power, matrix)
        reach = matrix_add(reach, power)
    return [[1 if val else 0 for val in row] for row in reach]

def connectivity_matrix(matrix):
    return [[1 if matrix[i][j] and matrix[j][i] else 0 for j in range(len(matrix))] for i in range(len(matrix))]

def find_strong_components(conn):
    visited, comps = [False] * len(conn), []
    for v in range(len(conn)):
        if not visited[v]:
            comp = [u + 1 for u in range(len(conn)) if conn[v][u]]
            for u in comp: visited[u - 1] = True
            comps.append(comp or [v + 1])
    return comps

def condensed_graph_matrix(graph, sccs):
    n = len(sccs)
    condensed = [[0]*n for _ in range(n)]
    v_to_scc = {v: i for i, scc in enumerate(sccs) for v in scc}
    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph[i][j]:
                si, sj = v_to_scc[i + 1], v_to_scc[j + 1]
                if si != sj: condensed[si][sj] = 1
    return condensed

def get_graph_info(matrix, is_directed):
    print()
    if is_directed:
        in_d = [sum(matrix[j][i] for j in range(vertexes)) for i in range(vertexes)]
        out_d = [sum(matrix[i][j] for j in range(vertexes)) for i in range(vertexes)]
        total = [in_d[i] + out_d[i] for i in range(vertexes)]
        print_array(in_d, "Vertex degrees (IN):", " ")
        print_array(out_d, "Vertex degrees (OUT):", " ")
        print_array(total, "Vertex degrees:", " ")
    else:
        total = [sum((2 if i == j else 1) for j in range(vertexes) if matrix[i][j]) for i in range(vertexes)]
        print_array(total, "Vertex degrees:", " ")
    reg = all(d == total[0] for d in total)
    print_array([reg], "Regular:", " ")
    if reg: print_array([total[0]], "Regularity degree:", " ")
    print_array([i + 1 for i, d in enumerate(total) if d == 1], "Leap vertexes:", " ")
    print_array([i + 1 for i, d in enumerate(total) if d == 0], "Isolated vertexes:", " ")

def get_graph_new_info(matrix):
    print()
    in_d = [sum(matrix[j][i] for j in range(vertexes)) for i in range(vertexes)]
    out_d = [sum(matrix[i][j] for j in range(vertexes)) for i in range(vertexes)]
    print_array(in_d, "Vertex degrees (IN):", " ")
    print_array(out_d, "Vertex degrees (OUT):", " ")
    print("\nPaths length 2:")
    for p in get_paths_length_2(matrix): print(p, end=", ")
    print("\n\nPaths length 3:")
    for p in get_paths_length_3(matrix): print(p, end=", ")
    reach = reachability_matrix(matrix)
    print("\nReachability matrix:\n"); print_matrix(reach)
    conn = connectivity_matrix(reach)
    print("\nConnectivity matrix:\n"); print_matrix(conn)
    global condensed_graph, strong_components
    strong_components = find_strong_components(conn)
    print("\nStrong connectivity components:")
    for i, comp in enumerate(strong_components): print(f"{i + 1}) {comp}")
    condensed_graph = condensed_graph_matrix(matrix, strong_components)
    print("\nCondensed graph matrix:"); print_matrix(condensed_graph)

condensed_graph = strong_components = None
new_matrix_dir = [[calculate_element(k2) for _ in range(vertexes)] for _ in range(vertexes)]

frame, status = tk.Frame(root), tk.Label(tk.Frame(root), text="", justify=tk.LEFT)
frame.pack(pady=10); status.master.pack(pady=5); status.pack()

tk.Button(frame, text="Directed", command=lambda: (draw_graph(matrix_dir, vertexes, True), status.config(text="Directed Graph"))).pack(side=tk.LEFT, padx=10)
tk.Button(frame, text="Undirected", command=lambda: (draw_graph(matrix_undir, vertexes, False), status.config(text="Undirected Graph"))).pack(side=tk.LEFT, padx=10)
tk.Button(frame, text="New Directed", command=lambda: (draw_graph(new_matrix_dir, vertexes, True), status.config(text="New Directed Graph"))).pack(side=tk.LEFT, padx=10)
tk.Button(frame, text="Condensed", command=lambda: (draw_graph(condensed_graph, len(condensed_graph), True),status.config(text="Condensed Graph"))).pack(side=tk.LEFT, padx=10)

print("\nDirected matrix:\n"); print_matrix(matrix_dir); get_graph_info(matrix_dir, True)
print("\nUndirected matrix:\n"); print_matrix(matrix_undir); get_graph_info(matrix_undir, False)
print("\nUpdated directed matrix:\n"); print_matrix(new_matrix_dir); get_graph_new_info(new_matrix_dir)
draw_graph(matrix_dir, vertexes, True)
root.mainloop()
