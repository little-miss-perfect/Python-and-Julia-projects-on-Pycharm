import os
import csv


def save_k_value(name, k_value, l0,
                 filepath='experimental/data/processed/estimated_k.csv'):
    """
    Append a named spring-constant entry to CSV, with nice ', ' spacing.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Does file need a header?
    write_header = not os.path.exists(filepath) or os.stat(filepath).st_size == 0

    with open(filepath, 'a', newline='') as f:
        if write_header:
            f.write("name, unstretched_length, k\n")
        f.write(f"{name}, {l0}, {k_value}\n")

    print(f"✅ Saved k = {k_value:.2f} N/m under name '{name}'")
    print(f"💾 File updated: {filepath}")


def load_all_k_values(filepath='data/estimated_k.csv'):
    """
    Load all saved k values from CSV.

    Returns:
    - A list of dictionaries: [{'name': ..., 'unstretched_length': ..., 'k': ...}, ...]
    """
    if not os.path.exists(filepath):
        return []

    with open(filepath, mode='r') as f:
        reader = csv.DictReader(f)
        return [
            {
                'name': row['name'],
                'unstretched_length': float(row['unstretched_length']),
                'k': float(row['k'])
            }
            for row in reader
        ]

def load_saved_k(filepath='experimental/data/processed/estimated_k.csv'):
    """
    Prompt user to choose one of the saved spring constants from CSV.

    Parameters:
    - filepath: path to the CSV file

    Returns:
    - A dictionary with keys: 'name', 'l0', 'k', or None if canceled.
    """
    if not os.path.exists(filepath):
        print("⚠️ No k values have been saved yet.")
        return None

    entries = []
    with open(filepath, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                entries.append({
                    'name': row['name'].strip(),
                    'l0': float(row['unstretched_length']),
                    'k': float(row['k'])
                })
            except (ValueError, KeyError):
                continue  # skip malformed rows

    if not entries:
        print("⚠️ No valid entries found in the file.")
        return None

    print("\n📂 Available spring constants:")
    for idx, entry in enumerate(entries):
        print(f"  [{idx + 1}] {entry['name']} — l₀ = {entry['l0']} m, k = {entry['k']} N/m")

    while True:
        try:
            choice = int(input("\n🔢 Select a k value by number (or 0 to cancel): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(entries):
                return entries[choice - 1]
            else:
                print("❗ Invalid choice. Try again.")
        except ValueError:
            print("❗ Please enter a valid number.")
