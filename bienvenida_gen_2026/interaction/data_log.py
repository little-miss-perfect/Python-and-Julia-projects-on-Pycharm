import csv
import os
from datetime import datetime

class DataLogger:
    """
    Class to handle logging of throw results to a CSV file.

    Each row includes:
    - participant ID
    - launch angle (degrees)
    - launch speed (m/s)
    - hit position (x, y)
    - target position (x only)
    - absolute error
    - timestamp
    """

    def __init__(self, filepath='data/logs.csv'):
        """
        Initialize the logger with a file path. Creates the file with header if it doesn't exist.

        Parameters:
        - filepath: relative or absolute path to the CSV file
        """
        self.filepath = filepath

        # If the file does not exist yet, create it and write the header row
        if not os.path.exists(self.filepath):
            with open(self.filepath, mode='w', newline='') as f:
                header = ['timestamp',
                          'participant',
                          'theta_deg',
                          'v0',
                          'hit_x',
                          'hit_y',
                          'target_x',
                          'error']
                # join with ", " and add a newline
                f.write(', '.join(header) + '\n')

    def log_throw(self, participant, theta_deg, v0, hit_x, hit_y, target_x):
        """
        Record a new throw in the CSV file.

        Parameters:
        - participant: string identifier (e.g., name or desk number)
        - theta_deg: launch angle in degrees
        - v0: launch speed in m/s
        - hit_x, hit_y: projectile landing position
        - target_x: intended horizontal distance
        """
        error = abs(hit_x - target_x)  # compute absolute error
        timestamp = datetime.now().isoformat(timespec='seconds')  # current time

        # Open file in append mode and write one row
        with open(self.filepath, mode='a', newline='') as f:
            row = [timestamp,
                   participant,
                   theta_deg,
                   v0,
                   hit_x,
                   hit_y,
                   target_x,
                   error]
            # make sure everything is a string
            str_row = [str(item) for item in row]
            f.write(', '.join(str_row) + '\n')

    def load_all(self):
        """
        Load all throw data from the CSV file into a list of dictionaries.

        Returns:
        - List[Dict] with keys matching the column headers
        """
        with open(self.filepath, mode='r') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def reset_log(self):
        """
        Wipe the log file and re-write the header row.
        Use with caution.
        """
        with open(self.filepath, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp',
                'participant',
                'theta_deg',
                'v0',
                'hit_x',
                'hit_y',
                'target_x',
                'error'
            ])
