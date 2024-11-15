import numpy as np
import matplotlib.pyplot as plt

# Graham Scan Algorithm
def getMinimum(list):
    if not list:
        return None  # Returns none for an empty list
    
    # Initialize variable for the minimal Y-value
    min_yValue = list[0][1]
    xValue = list[0][0]

    for x, y in list:
        # Find the minimal y value (or, if multiple values are equal, the one with the lowest x value)
        if y < min_yValue or (y == min_yValue and x < xValue):
            min_yValue = y
            xValue = x

    #Return the coordinates of the minimal point
    return xValue, min_yValue

def getAngle(initial_x, initial_y, x, y):
    # Calculate angle
    angle = np.degrees(np.arctan2(y - initial_y, x - initial_x))
    
    if angle < 0:
        angle += 360  # Convert angle to a value between 0 and 360°
    return angle
    
def getOrientation(p1, p2, p3):
    # Calculate the orientation of 3 points per step
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def plotGrahamScan(convex, points, step):
    plt.cla()  # Delete the axes
    
    # Plot all points for the graham scan
    xs, ys = zip(*[(p[0], p[1]) for p in points])
    plt.scatter(xs, ys, color='blue', label='points')

    # Plot the current convex shell
    if len(convex) > 1:
        convex_xs, convex_ys = zip(*convex)
        plt.plot(convex_xs, convex_ys, 'r-', lw=2, label='current convex shell')
        
        # Close the shell
        plt.plot([convex[-1][0], convex[0][0]], [convex[-1][1], convex[0][1]], 'r-', lw=2)

    plt.title(f"Graham Scan - step {step}")
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.legend()
    plt.pause(1.0)

# Main program
points = [
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

# Find the initial point of the graham scan
initial_x, initial_y = getMinimum(points)

# Calculate the angles for all points
for point in points:
    angle = getAngle(initial_x, initial_y, point[0], point[1])
    point.append(angle)  # Add the angles to the corresponding points

# Delete the initial point from the list
pointsWithoutInitial = [point for point in points if not (point[0] == initial_x and point[1] == initial_y)]

# Sort the list regarding ascending angles
pointsSorted = sorted(pointsWithoutInitial, key=lambda point: point[2])

# Add initial point to the sorted list
pointsSorted.insert(0, [initial_x, initial_y, 0])

# Initialize plot
plt.figure(figsize=(10, 6))
convex = [[initial_x, initial_y]]
step = 1

# Graham Scan algorithm
for point in pointsSorted[1:]:
    convex.append([point[0], point[1]])  # Add point to the convex shell
    plotGrahamScan(convex, points, step)
    step += 1

    # Check the orientation of the last 3 points
    while len(convex) >= 3 and getOrientation(convex[-3], convex[-2], convex[-1]) <= 0:
        del convex[-2]  # Delete the second last point
        plotGrahamScan(convex, points, step)
        step += 1

# Add initial point
convex.append(convex[0])

# Final visualization
plotGrahamScan(convex, points, step)
plt.show()