import numpy as np
import cv2

"""
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

def draw_plan(world, plan):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.imshow(world)
    for state in plan:
        points = state.car_as_triangle()
        points = points + [points[0]]

        codes = [Path.MOVETO,
                 Path.LINETO,
                 Path.LINETO,
                 Path.CLOSEPOLY]

        path = Path(points, codes)
        patch = patches.PathPatch(path, facecolor='orange', lw=0.0)
        ax.add_patch(patch)

    plt.show()
"""

def draw_plan(world, plan, bgr=(255,0,0), thickness=1):
    img = np.copy(world)
    for t in range(len(plan)-1):
        pt0 = (int(plan[t].x), int(plan[t].y))
        pt1 = (int(plan[t+1].x), int(plan[t+1].y))

        cv2.line(img, pt0, pt1, bgr, thickness)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_plan_and_save(world, plan, visited_states, save_path, bgr=(255,0,0), thickness=1):
    img = np.copy(world)

    # Plot visited states:
    for state in visited_states:
        pt = (int(state.x), int(state.y))
        cv2.circle(img, pt, 1, (0,0,255), thickness)

    # Plot path:
    for t in range(len(plan)-1):
        pt0 = (int(plan[t].x), int(plan[t].y))
        pt1 = (int(plan[t+1].x), int(plan[t+1].y))

        cv2.line(img, pt0, pt1, bgr, thickness)
    
    

    # Added the following to save img:
    cv2.imwrite(save_path, img)
    
    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
