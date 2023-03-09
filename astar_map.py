import heapq

# Inisialisasi graph node/kota dan edge beserta costnya
graph = {
    'Surabaya': {'Sidoarjo': 23, 'Gresik': 25, 'Mojokerto': 60, 'Kediri': 135},
    'Sidoarjo': {'Surabaya': 23, 'Gresik': 18},
    'Gresik': {'Surabaya': 25, 'Sidoarjo': 18, 'Mojokerto': 40},
    'Mojokerto': {'Surabaya': 60, 'Gresik': 40, 'Kediri': 60},
    'Kediri': {'Surabaya': 135, 'Mojokerto': 60}
}

# Tentukan start dan goal
start = 'Surabaya'
goal = 'Kediri'

# Generate SLD setiap node ke goal
sld = {
    'Surabaya': 168,
    'Sidoarjo': 155,
    'Gresik': 126,
    'Mojokerto': 55,
    'Kediri': 0
}

def astar(graph, start, goal, sld):
    # Inisialisasi open set dan closed set
    openset = []
    closedset = set()

    # Inisialisasi nilai f, g, dan h untuk node start
    g = {start: 0}
    h = {start: sld[start]}
    f = {start: g[start] + h[start]}

    # Inisialisasi dictionary untuk menyimpan parent dari suatu node
    came_from = {}

    # Inisialisasi dictionary untuk menyimpan cost path
    cost = {start: 0}

    # Masukkan start ke open set
    heapq.heappush(openset, (f[start], start))

    while openset:
        # Ambil node dengan nilai f terkecil dari open set
        current_f, current = heapq.heappop(openset)

        # Jika current adalah goal, kembalikan path dan cost
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, cost[goal]

        # Tandai current sebagai visited dengan memasukkan ke closed set
        closedset.add(current)

        # Expand node
        for neighbor in graph[current]:
            # Skip jika neighbor sudah visited
            if neighbor in closedset:
                continue

            # Hitung nilai g baru
            tentative_g = g[current] + graph[current][neighbor]

            # Jika neighbor belum ada di open set, atau nilai g baru lebih kecil dari nilai g sebelumnya
            if neighbor not in g or tentative_g < g[neighbor]:
                # Update nilai g, h, dan f neighbor
                g[neighbor] = tentative_g
                h[neighbor] = sld[neighbor]
                f[neighbor] = g[neighbor] + h[neighbor]

                # Update cost path
                cost[neighbor] = tentative_g

                # Simpan parent dari neighbor
                came_from[neighbor] = current

                # Masukkan neighbor ke open set
                heapq.heappush(openset, (f[neighbor], neighbor))

    # Jika tidak ada path yang ditemukan, return None
    return None, None

# Panggil fungsi astar dan print hasilnya
path, cost = astar(graph, start, goal, sld)
if path is None:
    print("Tidak ada path")
else:
    # Print jalur
    print("Path:", " -> ".join(path))

    # Print biaya
    print("Cost:", cost)
