import pandas as pd
from matplotlib import pyplot as plt

def visualize_samples(df_samples: pd.DataFrame):
    plt.figure(figsize=(12, 6))
    plt.scatter(df_samples['x'], df_samples['y'], s=5, color='blue', label='Detector Hits')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Detected Particle Collisions')
    plt.legend()
    plt.show()

def save_dataframe_as_image(df, path):
    fig, ax = plt.subplots(figsize=(12, 6))  # Set the size of the figure
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)  # Adjust the scale of the table
    plt.savefig(path, bbox_inches='tight', pad_inches=0.1)