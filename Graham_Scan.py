import numpy
import pandas as pd
import matplotlib.pyplot as plt

def get_lowest_y(li):
    # Überprüfen, ob die Liste leer ist
    if not li:
        return None  # Gibt None zurück, wenn die Liste leer ist

    # Initialisiere die Variable für den kleinsten Y-Wert
    kleinster_y_wert = li[0][1]
    x_wert = li[0][0]

    # Gehe durch jeden Eintrag in der Liste
    for x, y in li:
        # Überprüfe, ob der aktuelle Y-Wert kleiner ist oder bei Gleichheit der X-Wert kleiner ist
        if y < kleinster_y_wert or (y == kleinster_y_wert and x < x_wert):
            kleinster_y_wert = y
            x_wert = x

    return x_wert, kleinster_y_wert

def get_angle(start_x, start_y, x, y):
    # Berechne den Winkel
    angle = numpy.degrees(numpy.arctan2(y - start_y, x - start_x))
    if angle < 0:
        angle += 360  # Winkel von 0 bis 360 Grad
    return angle

def cross_product(o, a, b):
    # Berechne das Kreuzprodukt von OA und OB
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def plot_graham(konvex, points, step):
    plt.cla()  # Lösche die Achsen anstatt ein neues Fenster zu öffnen
    
    # Zeichne alle Punkte
    xs, ys = zip(*[(p[0], p[1]) for p in points])
    plt.scatter(xs, ys, color='blue', label='Punkte')

    # Zeichne die aktuelle Konvex-Hülle
    if len(konvex) > 1:
        konvex_xs, konvex_ys = zip(*konvex)
        plt.plot(konvex_xs, konvex_ys, 'r-', lw=2, label='Aktuelle Kovex-Hülle')
        # Hülle schließen
        plt.plot([konvex[-1][0], konvex[0][0]], [konvex[-1][1], konvex[0][1]], 'r-', lw=2)

    plt.title(f"Graham Scan - Schritt {step}")
    plt.xlabel("X-Wert")
    plt.ylabel("Y-Wert")
    plt.legend()
    plt.pause(0.5)
# Hauptprogramm
test_values = [
    [7, 3],
    [8, 7],
    [4, 8],
    [8, 2],
    [4, 6],
    [3, 9],
    [7, 7],
    [4, 9],
    [6, 6],
    [2, 1]
]

# Finde den Startpunkt
start_x, start_y = get_lowest_y(test_values)

# Berechne den Winkel für jeden Punkt
for point in test_values:
    angle = get_angle(start_x, start_y, point[0], point[1])
    point.append(angle)  # Füge den berechneten Winkel zum Punkt hinzu

# Entferne den Startpunkt aus der Liste
test_values_without_start = [point for point in test_values if not (point[0] == start_x and point[1] == start_y)]

# Sortiere die Liste nach dem Winkel
test_values_sorted = sorted(test_values_without_start, key=lambda point: point[2])

# Füge den Startpunkt am Anfang der sortierten Liste hinzu
test_values_sorted.insert(0, [start_x, start_y, 0])

# Initialisiere den Plot und die Liste für die Konvex-Hülle
plt.figure(figsize=(10, 6))
konvex = [[start_x, start_y]]
step = 1

# Graham-Scan-Algorithmus
for point in test_values_sorted[1:]:
    konvex.append([point[0], point[1]])  # Füge den Punkt zur Konvex Hülle hinzu
    plot_graham(konvex, test_values, step)
    step += 1

    # Prüfe, ob die letzten drei Punkte eine Rechtsdrehung bilden
    while len(konvex) >= 3 and cross_product(konvex[-3], konvex[-2], konvex[-1]) <= 0:
        del konvex[-2]  # Entferne den vorletzten Punkt
        plot_graham(konvex, test_values, step)
        step += 1

# Füge den Startpunkt am Ende hinzu, um die Hülle zu schließen
konvex.append(konvex[0])

# Abschließende Visualisierung der konvexen Hülle
plot_graham(konvex, test_values, step)
plt.show()  # Zeige die finale Hülle an
