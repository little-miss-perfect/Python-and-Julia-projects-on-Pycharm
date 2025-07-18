import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


# ======================
# === StatementManager
# ======================
class StatementManager:
    """
    Manages user interaction with available .xlsx files in the 'statements/' directory.
    """

    def __init__(self, directory='statements'):
        self.directory = directory

    def list_statement_files(self):
        """
        Return a list of .xlsx files in the directory.
        """
        if not os.path.isdir(self.directory):
            print(f"Directory '{self.directory}' not found.")
            return []

        files = [
            f for f in os.listdir(self.directory)
            if f.endswith('.xlsx') and not f.startswith('~$')
        ]
        return sorted(files)

    def prompt_file_selection(self, allow_multiple=True):
        """
        Prompt the user to select one or more .xlsx files by index.
        Returns a list of selected filenames (with full paths).
        """
        files = self.list_statement_files()

        if not files:
            print("No .xlsx files found in the statements directory.")
            return []

        print("\nAvailable .xlsx statement files:")
        for idx, file in enumerate(files, 1):
            print(f"{idx}. {file}")

        while True:
            try:
                selection = input(
                    f"\nEnter the number(s) of the file(s) to analyze "
                    f"(comma-separated for multiple, e.g., 1,3): "
                ).strip()

                indexes = [int(i.strip()) for i in selection.split(',')]
                selected_files = [os.path.join(self.directory, files[i - 1]) for i in indexes]

                if not allow_multiple and len(selected_files) > 1:
                    print("Please select only one file.")
                    continue

                return selected_files

            except (ValueError, IndexError):
                print("Invalid input. Please enter valid file number(s).")


# =========================
# === EstadoCuentaAnalyzer
# =========================
class EstadoCuentaAnalyzer:
    """
    Class to analyze a BBVA credit card statement in .xlsx format.
    Provides methods to filter, sort, show, summarize, and compare data.
    """

    def __init__(self, filename):
        self.filename = filename
        self.df = None

    def load_dataframe(self):
        xls = pd.ExcelFile(self.filename)
        sheet_name = xls.sheet_names[0]
        print(f"\n📄 Analyzing file: {self.filename}")
        print(f"Using sheet: '{sheet_name}'")

        df = pd.read_excel(self.filename, sheet_name=sheet_name, header=1)
        df.columns = ['FECHA', 'DESCRIPCIÓN', 'CARGO', 'ABONO', 'SALDO']

        df['ABONO'] = pd.to_numeric(df['ABONO'], errors='coerce')
        df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')

        df_filtered = df[(df['ABONO'].isna()) | (df['ABONO'] >= 0)].copy()

        print(f"Original rows: {len(df)}")
        print(f"Rows after filtering: {len(df_filtered)}")

        self.df = df_filtered

    def get_date_range(self, df):
        oldest_date = df['FECHA'].min()
        newest_date = df['FECHA'].max()
        print(f"\n📆 Date range in file:")
        print(f"- Oldest date: {oldest_date.date()}")
        print(f"- Newest date: {newest_date.date()}")
        return oldest_date, newest_date

    def filter_by_date(self, start_date_str, end_date_str):
        start_date = pd.to_datetime(start_date_str, format='%d/%m/%Y')
        end_date = pd.to_datetime(end_date_str, format='%d/%m/%Y')
        df_filtered = self.df[(self.df['FECHA'] >= start_date) & (self.df['FECHA'] <= end_date)].copy()
        print(f"\n📊 Filtered {len(df_filtered)} rows between {start_date.date()} and {end_date.date()}")
        return df_filtered

    def sum_total_cargo(self, df):
        total = pd.to_numeric(df['CARGO'], errors='coerce').sum()
        print(f"\n💰 Total CARGO in this period: {total:.2f}")
        return total

    def get_unique_descriptions(self):
        descs = sorted(self.df['DESCRIPCIÓN'].dropna().unique())
        print(f"\n🧾 Unique DESCRIPCIÓN entries ({len(descs)} found):")
        for d in descs:
            print(f"- {d}")
        return descs

    def sum_cargo_for_description(self, df, keyword):
        rows = df[df['DESCRIPCIÓN'].str.contains(keyword, case=False, na=False)]
        total = pd.to_numeric(rows['CARGO'], errors='coerce').sum()
        print(f"\n🔍 CARGO total for DESCRIPCIÓN containing '{keyword}': {total:.2f}")
        return total

    def compare_cargo_per_description(self, df1, label1, df2, label2):
        sum1 = df1.groupby('DESCRIPCIÓN', as_index=False)['CARGO'].sum()
        sum2 = df2.groupby('DESCRIPCIÓN', as_index=False)['CARGO'].sum()
        sum1['CARGO'] = pd.to_numeric(sum1['CARGO'], errors='coerce').fillna(0)
        sum2['CARGO'] = pd.to_numeric(sum2['CARGO'], errors='coerce').fillna(0)
        sum1 = sum1.rename(columns={'CARGO': f'CARGO_{label1}'})
        sum2 = sum2.rename(columns={'CARGO': f'CARGO_{label2}'})
        merged = pd.merge(sum1, sum2, on='DESCRIPCIÓN', how='outer').fillna(0)
        merged['DIFFERENCE'] = merged[f'CARGO_{label2}'] - merged[f'CARGO_{label1}']
        merged['TREND'] = merged['DIFFERENCE'].apply(
            lambda x: 'INCREASED' if x > 0 else ('DECREASED' if x < 0 else 'UNCHANGED')
        )
        merged = merged.sort_values(by='DIFFERENCE', ascending=False).reset_index(drop=True)
        print(f"\n📊 Comparison of CARGO per DESCRIPCIÓN ({label1} vs {label2}):")
        print(merged.to_string(index=False))
        return merged


def analyze_date_coverage(analyzers):
    """
    Check for overlaps or gaps between the date ranges of multiple loaded statements.
    Assumes each analyzer has already loaded its dataframe.
    """
    print("\n📆 Analyzing date coverage across all selected statements...")

    date_ranges = []

    for analyzer in analyzers:
        start = analyzer.df['FECHA'].min()
        end = analyzer.df['FECHA'].max()
        label = os.path.basename(analyzer.filename)
        date_ranges.append((start, end, label))

    # Sort by start date
    date_ranges.sort(key=lambda x: x[0])

    for i, (start, end, label) in enumerate(date_ranges):
        print(f"🗂️  {label}: {start.date()} → {end.date()}")

        if i > 0:
            prev_end = date_ranges[i - 1][1]
            gap = (start - prev_end).days

            if gap > 1:
                print(f"   ⛔ GAP of {gap} days between previous file and this one.")
            elif gap <= 0:
                overlap = abs(gap) + 1
                print(f"   ⚠️ OVERLAP of {overlap} days with previous file.")


# =====================
# === MAIN EXECUTION
# =====================
if __name__ == '__main__':
    manager = StatementManager()
    selected_files = manager.prompt_file_selection(allow_multiple=True)

    analyzers = []
    for filepath in selected_files:
        analyzer = EstadoCuentaAnalyzer(filepath)
        analyzer.load_dataframe()
        analyzers.append(analyzer)

        # Show available date range
        oldest, newest = analyzer.get_date_range(analyzer.df)

        # Ask user to define period for this file
        start = input("🗓️  Enter start date (dd/mm/yyyy): ")
        end = input("🗓️  Enter end date (dd/mm/yyyy): ")
        df_period = analyzer.filter_by_date(start, end)

        # Show total cargo and common descriptions
        analyzer.sum_total_cargo(df_period)
        analyzer.get_unique_descriptions()

        # Ask user if they want to search a keyword (e.g., 'uber')
        keyword = input("🔍 Enter keyword to analyze specific DESCRIPCIÓN (or press Enter to skip): ").strip()
        if keyword:
            analyzer.sum_cargo_for_description(df_period, keyword)

    # NEW — analyze date coverage across selected files
    if len(analyzers) > 1:
        analyze_date_coverage(analyzers)

    # Compare two selected files (optional)
    if len(analyzers) == 2:
        should_compare = input("\nWould you like to compare these two statements? (y/n): ").strip().lower()
        if should_compare == 'y':
            label1 = os.path.basename(analyzers[0].filename).replace('.xlsx', '')
            label2 = os.path.basename(analyzers[1].filename).replace('.xlsx', '')
            df1 = analyzers[0].df
            df2 = analyzers[1].df
            analyzers[0].compare_cargo_per_description(df1, label1, df2, label2)
