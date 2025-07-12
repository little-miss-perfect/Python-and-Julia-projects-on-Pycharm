import csv
import matplotlib.pyplot as plt


def load_column(filepath, column_name):
    """
    Helper function: loads a single column from a CSV file as a list of floats.

    Parameters:
    - filepath: path to the CSV file
    - column_name: string name of the column to extract

    Returns:
    - List of floats
    """
    with open(filepath, mode='r') as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        return [float(row[column_name]) for row in reader if row[column_name] != '']


def plot_error_histogram(filepath='data/logs.csv', bins=10, threshold=None, show_normalized=False):
    """
    Plot a histogram of signed errors from the CSV log.

    Parameters:
    - filepath: path to logs.csv
    - bins: number of histogram bins
    - threshold: optional float, plot a shaded hit zone ±threshold
    - show_normalized: whether to overlay a normalized (PDF-like) histogram
    """
    errors = load_column(filepath, 'error')  # Load the 'error' column

    # Clear previous figure and start new one
    plt.clf()
    plt.figure(figsize=(10, 5))

    # Plot basic histogram (absolute frequency)
    plt.hist(errors, bins=bins, edgecolor='black', alpha=0.7, label='Absolute Error')

    # Overlay probability density curve if requested
    if show_normalized:
        plt.hist(errors, bins=bins, density=True, histtype='step', linewidth=2,
                 color='orange', label='Normalized (PDF)')

    # Shade the hit zone if threshold provided
    if threshold:
        plt.axvspan(-threshold, threshold, color='green', alpha=0.2, label=f'Hit zone (±{threshold} m)')
        plt.axvline(-threshold, color='red', linestyle='--')
        plt.axvline(threshold, color='red', linestyle='--')

    # Axis labels and legend
    plt.title('Histogram of Throwing Errors')
    plt.xlabel('Error Distance (m)')
    plt.ylabel('Frequency / Probability Density')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_hit_x_histogram(filepath='data/logs.csv', bins=10, target_x=None, threshold=None):
    """
    Plot a histogram of horizontal landing positions (hit_x).

    Parameters:
    - filepath: path to logs.csv
    - bins: number of bins
    - target_x: target horizontal position (optional, used to draw target line)
    - threshold: hit tolerance range (optional, used to shade hit zone)
    """
    x_positions = load_column(filepath, 'hit_x')

    # Clear any previous plot
    plt.clf()
    plt.figure(figsize=(10, 5))

    # Main histogram: raw hit positions
    plt.hist(x_positions, bins=bins, edgecolor='black', alpha=0.7, label='Landing positions (x)')

    # If provided, highlight the hit zone
    if target_x is not None and threshold is not None:
        # Shade between target_x - threshold and target_x + threshold
        plt.axvspan(target_x - threshold, target_x + threshold, color='green', alpha=0.2, label='Hit zone')
        plt.axvline(target_x, color='black', linestyle='--', label='🎯 Target')

    # Labels and layout
    plt.title('Histogram of Landing Positions')
    plt.xlabel('Horizontal Distance (m)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_comparison_histogram(list_a, list_b, label_a="Group A", label_b="Group B", title="Comparison of Errors", bins=10):
    """
    Plot a side-by-side histogram comparing two lists of errors or distances.

    Parameters:
    - list_a: first list of numerical data (e.g., errors)
    - list_b: second list of numerical data
    - label_a: label for first group
    - label_b: label for second group
    - title: plot title
    - bins: number of bins
    """
    plt.hist(list_a, bins=bins, alpha=0.6, label=label_a, edgecolor='black')
    plt.hist(list_b, bins=bins, alpha=0.6, label=label_b, edgecolor='black')
    plt.title(title)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.show()
