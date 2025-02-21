import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from src.quadtree import Quadtree


def visualize_windows_results(quadtree: Quadtree, points: np.ndarray, windows):
    fig, ax = plt.subplots(figsize=(12, 8))
    quadtree.plot(ax)

    ax.scatter([p.x for p in points], [p.y for p in points], s=5, color='blue', label='Detector Hits')

    for window, count, cluster_hits in windows:
        rect = plt.Rectangle((window.x, window.y),
                             window.width,
                             window.height,
                             fill=True,
                             color='green',
                             alpha=0.3)

        ax.scatter([p.x for p in cluster_hits], [p.y for p in cluster_hits],
                    s=15,
                    color='red')

        ax.add_patch(rect)

    ax.set_title('Sliding Window Query \n (Candidate detection hits)')
    ax.set_xlabel('X position')
    ax.set_ylabel('Y position')

    # Define custom legend handles with colors
    detector_hits_patch = patches.Patch(color='blue', label='Detector Hits')
    cluster_hits_patch = patches.Patch(color='red', label='Cluster Hits')
    window_patch = patches.Patch(color='green', label='Window')

    # Add the legend with custom handles
    ax.legend(handles=[detector_hits_patch, cluster_hits_patch, window_patch])

    #plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()


def visualize_clusters_results(points: np.ndarray, clusters):
    plt.figure(figsize=(12, 6))
    plt.scatter([p.x for p in points], [p.y for p in points], s=5, color='blue', label='Detector Hits')

    colors = {}
    for label in clusters.keys():
        if label == -1:
            colors[label] = 'black'
        else:
            colors[label] = np.random.rand(3,)

    for label, cluster_hits in clusters.items():
        x_cluster = [point[0] for point in cluster_hits]
        y_cluster = [point[1] for point in cluster_hits]

        plt.scatter(x_cluster, y_cluster, s=15, color=colors[label])

    plt.title('DBSCAN Clustering \n (Candidate detection hits)')
    plt.xlabel('X position')
    plt.ylabel('Y position')
    plt.legend(labels=['Detector Hits', 'Cluster Hits'])
    plt.tight_layout()
    plt.show()