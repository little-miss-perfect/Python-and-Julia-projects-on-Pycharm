import pandas as pd
import os
import warnings

# Suppress openpyxl warning about missing default styles
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


class StatementManager:
    """
    Manages user interaction with available .xlsx files in the 'statements/' directory.
    """

    def __init__(self, directory='statements'):
        self.directory = directory

    def list_statement_files(self):
        if not os.path.isdir(self.directory):
            print(f"Directory '{self.directory}' not found.")
            return []
        files = [
            f for f in os.listdir(self.directory)
            if f.endswith('.xlsx') and not f.startswith('~$')
        ]
        return sorted(files)

    def prompt_file_selection(self, allow_multiple=True):
        files = self.list_statement_files()
        if not files:
            print("No .xlsx files found.")
            return []

        print("\nAvailable statement files:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")

        while True:
            try:
                selection = input(
                    "\nEnter file number(s) to select (e.g. '1' or '1,3'): "
                ).strip()
                indexes = [int(i.strip()) for i in selection.split(',')]
                selected_files = [os.path.join(self.directory, files[i - 1]) for i in indexes]

                if not allow_multiple and len(selected_files) > 1:
                    print("Please select only one file.")
                    continue

                return selected_files
            except (ValueError, IndexError):
                print("Invalid input. Try again.")


class EstadoCuentaAnalyzer:
    """[Your full class definition here — same as before]"""
    # [Truncated here for brevity; keep your full class as-is above this comment]


# ===================== MAIN FLOW =====================

def prompt_for_date_range():
    print("\nEnter the date range (format: dd/mm/yyyy)")
    start = input("Start date: ").strip()
    end = input("End date: ").strip()
    return start, end

def analyze_single_file(analyzer):
    analyzer.load_dataframe()
    start_date, end_date = prompt_for_date_range()
    df = analyzer.filter_by_date(start_date, end_date)
    analyzer.get_date_range(df)
    analyzer.sum_total_cargo(df)
    analyzer.sum_cargo_per_description(df)
    keyword = input("Enter a keyword to filter DESCRIPCIÓN (e.g., 'uber'): ").strip()
    analyzer.sum_cargo_for_description(df, keyword)
    df_filtered = analyzer.filter_by_description(df, keyword)
    # Optional: show full DataFrame
    # analyzer.show_dataframe(df_filtered)

def compare_two_periods_in_file(analyzer):
    analyzer.load_dataframe()
    print("\nDefine first period:")
    start1, end1 = prompt_for_date_range()
    print("\nDefine second period:")
    start2, end2 = prompt_for_date_range()
    df1 = analyzer.filter_by_date(start1, end1)
    df2 = analyzer.filter_by_date(start2, end2)
    analyzer.compare_cargo_per_description(df1, "Period1", df2, "Period2")

def compare_two_files(path1, path2):
    analyzer1 = EstadoCuentaAnalyzer(path1)
    analyzer2 = EstadoCuentaAnalyzer(path2)
    analyzer1.load_dataframe()
    analyzer2.load_dataframe()
    print(f"\nFile 1: {os.path.basename(path1)}")
    start1, end1 = prompt_for_date_range()
    print(f"\nFile 2: {os.path.basename(path2)}")
    start2, end2 = prompt_for_date_range()
    df1 = analyzer1.filter_by_date(start1, end1)
    df2 = analyzer2.filter_by_date(start2, end2)
    analyzer1.compare_cargo_per_description(df1, "File1", df2, "File2")


# Start here
if __name__ == "__main__":
    manager = StatementManager()
    selected = manager.prompt_file_selection(allow_multiple=True)

    if not selected:
        print("No files selected. Exiting.")
    elif len(selected) == 1:
        analyzer = EstadoCuentaAnalyzer(selected[0])
        print(f"\nSelected: {os.path.basename(selected[0])}")
        print("\nWhat would you like to do?")
        print("1. Analyze a single time period")
        print("2. Compare two periods in this same file")
        choice = input("Enter 1 or 2: ").strip()
        if choice == "1":
            analyze_single_file(analyzer)
        elif choice == "2":
            compare_two_periods_in_file(analyzer)
        else:
            print("Invalid choice.")
    elif len(selected) == 2:
        compare_two_files(selected[0], selected[1])
    else:
        print("You selected more than 2 files — currently only 1 or 2 are supported.")
