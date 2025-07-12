import numpy as np
import matplotlib.pyplot as plt
import csv


def compute_statistics(distances):
    """
    Compute basic stats from a list of distances (e.g. errors from the target).
    Returns a dictionary with mean, std, min, max, etc.
    """
    distances = np.array(distances)
    return {
        'mean': np.mean(distances),
        'std': np.std(distances),
        'min': np.min(distances),
        'max': np.max(distances),
        'count': len(distances)
    }

def evaluate_accuracy(x_final, target_x, tolerance=0.1):
    """
    Determine if a projectile hit the target within a tolerance.
    Returns a tuple: (is_hit: bool, error: float)
    """
    error = abs(x_final - target_x)
    return (error <= tolerance, error)

def generate_histogram(data, bins=10, title='Histogram', xlabel='Error (m)', ylabel='Frequency'):
    """
    Plot a histogram from a dataset.
    """
    plt.hist(data, bins=bins, edgecolor='black', alpha=0.7)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

def compare_real_vs_sim(real_data, sim_data, bins=10):
    """
    Overlay histograms of real and simulated data for visual comparison.
    """
    plt.hist(real_data, bins=bins, alpha=0.5, label='Real Data', edgecolor='black')
    plt.hist(sim_data, bins=bins, alpha=0.5, label='Simulated', edgecolor='black')
    plt.title('Real vs Simulated Distances')
    plt.xlabel('Distance (m)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.show()

def show_leaderboard(filepath='data/logs.csv', top_n=3, hit_only=False, tolerance=0.1, export_csv=False, show_chart=False):
    """
    Display a leaderboard of most accurate throws (lowest error).

    Parameters:
    - filepath: path to the CSV log file
    - top_n: number of top participants to display
    - hit_only: if True, only include throws with error ≤ tolerance
    - tolerance: maximum allowed error to count as a "hit" (in meters)
    - export_csv: if True, export the leaderboard to a separate CSV file
    - show_chart: if True, display a bar chart of the top performers
    """

    # Open the log file and load all rows into a list of dictionaries
    with open(filepath, mode='r') as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        throws = list(reader)

    # If no data is found, exit early
    if not throws:
        print("📭 No data found in logs.csv")
        return

    # Convert the 'error' values from strings to floats for numeric processing
    for row in throws:
        row['error'] = float(row['error'])

    # If hit_only is enabled, filter to only include rows with error ≤ tolerance
    if hit_only:
        throws = [row for row in throws if row['error'] <= tolerance]
        if not throws:
            print(f"❌ No throws within ±{tolerance:.2f} m tolerance.")
            return  # Exit if no qualifying hits

    # Sort all throws by lowest error (most accurate first)
    throws.sort(key=lambda row: row['error'])

    # Slice to keep only the top N performers
    top_throws = throws[:top_n]

    # Print leaderboard header
    print("\n🏆 Top Performers" + (" (HITS ONLY)" if hit_only else ""))
    print("-" * 50)
    print(f"{'Rank':<5} {'Participant':<15} {'Error (m)':<10} {'Hit_x (m)':<10}")
    print("-" * 50)

    # Print each top participant's data in a formatted row
    for i, row in enumerate(top_throws):
        print(f"{i + 1:<5} {row['participant']:<15} {row['error']:<10.3f} {row['hit_x']:<10}")

    # Print footer line
    print("-" * 50)

    # === Optional: export to a new CSV file ===
    if export_csv:
        with open('data/leaderboard.csv', mode='w', newline='') as f_out:
            writer = csv.writer(f_out)
            # Write column headers
            writer.writerow(['Rank', 'Participant', 'Error (m)', 'Hit_x (m)'])
            # Write each top entry
            for i, row in enumerate(top_throws):
                writer.writerow([i + 1, row['participant'], row['error'], row['hit_x']])
        print("📄 Leaderboard exported to data/leaderboard.csv")

    # === Optional: display bar chart ===
    if show_chart:
        # Extract names and error values for the plot
        names = [row['participant'] for row in top_throws]
        errors = [row['error'] for row in top_throws]

        # Create a bar chart
        plt.bar(names, errors, color='skyblue', edgecolor='black')

        # Add labels and title
        plt.xlabel('Participant')
        plt.ylabel('Error (m)')
        plt.title('Top Performers (Least Error)')
        plt.grid(True, axis='y')

        # Rotate x-axis labels if needed
        plt.xticks(rotation=45)
        plt.tight_layout()  # Adjust layout to avoid cutting off labels
        plt.show()
