import pandas as pd

# Optional: suppress openpyxl default style warning (BBVA Excel sometimes lacks default styles)
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

class EstadoCuentaAnalyzer:
    """
    Class to analyze a BBVA credit card statement in .xlsx format.
    Provides methods to filter, sort, show, summarize, and compare data.
    """

    def __init__(self, filename):
        """
        Initialize the analyzer with the filename.
        """
        self.filename = filename
        self.df = None  # This will hold the loaded and cleaned DataFrame

    def load_dataframe(self):
        """
        Load the Excel file, clean it, and store the DataFrame in self.df.
        """
        xls = pd.ExcelFile(self.filename)
        sheet_name = xls.sheet_names[0]
        print(f"Using sheet: '{sheet_name}'")

        # Read Excel and rename columns
        df = pd.read_excel(self.filename, sheet_name=sheet_name, header=1)
        df.columns = ['FECHA', 'DESCRIPCIÓN', 'CARGO', 'ABONO', 'SALDO']
        print(f"Renamed columns: {list(df.columns)}")

        # Clean data
        df['ABONO'] = pd.to_numeric(df['ABONO'], errors='coerce')
        df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')

        # Remove rows with negative ABONO
        df_filtered = df[(df['ABONO'].isna()) | (df['ABONO'] >= 0)].copy()

        print(f"Original rows: {len(df)}")
        print(f"Rows after removing negative ABONO: {len(df_filtered)}\n")

        # Store the cleaned DataFrame
        self.df = df_filtered

    def filter_by_date(self, start_date_str, end_date_str):
        """
        Return a DataFrame filtered between start_date and end_date.
        """
        if self.df is None:
            print("Dataframe not loaded. Please run load_dataframe() first.")
            return None

        start_date = pd.to_datetime(start_date_str, format='%d/%m/%Y')
        end_date = pd.to_datetime(end_date_str, format='%d/%m/%Y')

        df_filtered = self.df[(self.df['FECHA'] >= start_date) & (self.df['FECHA'] <= end_date)].copy()

        print(f"Filtered rows between {start_date.date()} and {end_date.date()}: {len(df_filtered)}\n")
        return df_filtered

    def sort_by_descripcion(self, df):
        """
        Return DataFrame sorted by DESCRIPCIÓN.
        """
        df_sorted = df.sort_values(by='DESCRIPCIÓN').reset_index(drop=True)
        print("DataFrame sorted by DESCRIPCIÓN.\n")
        return df_sorted

    def sort_by_date(self, df):
        """
        Return DataFrame sorted by FECHA.
        """
        df_sorted = df.sort_values(by='FECHA').reset_index(drop=True)
        print("DataFrame sorted by FECHA.\n")
        return df_sorted

    def show_dataframe(self, df):
        """
        Display the full DataFrame (all rows and columns).
        """
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        print(df.to_string(index=False))

    def sum_cargo_for_description(self, df, keyword):
        """
        Sum the CARGO for rows where DESCRIPCIÓN contains the keyword (case-insensitive).
        """
        rows = df[df['DESCRIPCIÓN'].str.contains(keyword, case=False, na=False)]
        total = pd.to_numeric(rows['CARGO'], errors='coerce').sum()
        print(f"\nTotal CARGO for DESCRIPCIÓN containing '{keyword}': {total:.2f}")
        return total

    def get_unique_descriptions(self):
        """
        Return and print the list of unique DESCRIPCIÓN entries.
        """
        if self.df is None:
            print("Dataframe not loaded. Please run load_dataframe() first.")
            return []

        unique_descriptions = sorted(self.df['DESCRIPCIÓN'].dropna().unique())
        print(f"\nUnique DESCRIPCIÓN entries ({len(unique_descriptions)} found):")
        for desc in unique_descriptions:
            print(f"- {desc}")
        return unique_descriptions

    def filter_by_description(self, df, keyword):
        """
        Return DataFrame filtered where DESCRIPCIÓN contains the keyword (case-insensitive).
        """
        filtered_df = df[df['DESCRIPCIÓN'].str.contains(keyword, case=False, na=False)].copy()
        print(f"\nFiltered rows where DESCRIPCIÓN contains '{keyword}': {len(filtered_df)} rows.\n")
        return filtered_df

    def get_date_range(self, df):
        """
        Return the oldest and newest dates in the DataFrame.
        """
        oldest_date = df['FECHA'].min()
        newest_date = df['FECHA'].max()

        print(f"\nDate range in this DataFrame:")
        print(f"- Oldest date: {oldest_date.date()}")
        print(f"- Newest date: {newest_date.date()}")

        return oldest_date, newest_date

    def count_description(self, df):
        """
        Count how many times each DESCRIPCIÓN appears.
        Returns a DataFrame with DESCRIPCIÓN and count.
        """
        count_df = df['DESCRIPCIÓN'].value_counts().reset_index()
        count_df.columns = ['DESCRIPCIÓN', 'COUNT']

        print("\nCount of DESCRIPCIÓN entries (descending order):")
        print(count_df.to_string(index=False))

        return count_df

    def sum_total_cargo(self, df):
        """
        Sum the entire CARGO column for the given DataFrame.
        Returns the total sum.
        """
        total_cargo = pd.to_numeric(df['CARGO'], errors='coerce').sum()
        print(f"\nTotal CARGO for this period: {total_cargo:.2f}")
        return total_cargo

    def sum_cargo_per_description(self, df, step=1000):
        """
        Sum CARGO per DESCRIPCIÓN for the given DataFrame.
        Prints running total checkpoints every 'step' amount.
        Shows the ACTUAL running total at each checkpoint.
        Returns a DataFrame with DESCRIPCIÓN and total CARGO, sorted descending.
        """
        # Group by DESCRIPCIÓN and sum CARGO
        sum_df = df.groupby('DESCRIPCIÓN', as_index=False)['CARGO'].sum()

        # Clean possible NaNs
        sum_df['CARGO'] = pd.to_numeric(sum_df['CARGO'], errors='coerce').fillna(0)

        # Sort descending
        sum_df = sum_df.sort_values(by='CARGO', ascending=False).reset_index(drop=True)

        print("\nTotal CARGO per DESCRIPCIÓN (descending):")

        # Initialize running total
        running_total = 0
        next_checkpoint = step

        # Print each row manually with running total
        for index, row in sum_df.iterrows():
            descripcion = row['DESCRIPCIÓN']
            cargo = row['CARGO']
            running_total += cargo

            print(f"- {descripcion}: {cargo:.2f}")

            # Check if we crossed a checkpoint
            if running_total >= next_checkpoint:
                print(f"    → Running total so far: {running_total:.2f}")
                # Move to next checkpoint(s)
                while running_total >= next_checkpoint:
                    next_checkpoint += step

        print(f"\nFINAL total CARGO for this period: {running_total:.2f}")

        return sum_df

    def compare_cargo_per_description(self, df1, label1, df2, label2):
        """
        Compare sum of CARGO per DESCRIPCIÓN between two DataFrames.
        Displays the comparison and returns the merged DataFrame.
        label1 and label2 are names for each period (for display).
        Adds a TREND column: 'INCREASED', 'DECREASED', 'UNCHANGED'.
        """
        # Sum per description for each DataFrame
        sum1 = df1.groupby('DESCRIPCIÓN', as_index=False)['CARGO'].sum()
        sum1['CARGO'] = pd.to_numeric(sum1['CARGO'], errors='coerce').fillna(0)
        sum1 = sum1.rename(columns={'CARGO': f'CARGO_{label1}'})

        sum2 = df2.groupby('DESCRIPCIÓN', as_index=False)['CARGO'].sum()
        sum2['CARGO'] = pd.to_numeric(sum2['CARGO'], errors='coerce').fillna(0)
        sum2 = sum2.rename(columns={'CARGO': f'CARGO_{label2}'})

        # Merge on DESCRIPCIÓN
        merged = pd.merge(sum1, sum2, on='DESCRIPCIÓN', how='outer').fillna(0)

        # Compute difference
        merged['DIFFERENCE'] = merged[f'CARGO_{label2}'] - merged[f'CARGO_{label1}']

        # Add TREND column
        merged['TREND'] = merged['DIFFERENCE'].apply(
            lambda x: 'INCREASED' if x > 0 else ('DECREASED' if x < 0 else 'UNCHANGED')
        )

        # Sort by absolute value of DIFFERENCE (biggest changes first)
        merged = merged.sort_values(by='DIFFERENCE', ascending=False).reset_index(drop=True)

        # Display
        print(f"\nComparison of CARGO per DESCRIPCIÓN between '{label1}' and '{label2}':")
        print(merged.to_string(index=False))

        return merged


# === ORIGINAL EXAMPLE USAGE ===

# Create the analyzer
analyzer = EstadoCuentaAnalyzer('estado_de_cuenta_6enero2025_6_junio2025.xlsx')

# Load the data
analyzer.load_dataframe()

# 1️⃣ See unique DESCRIPCIÓN entries
# analyzer.get_unique_descriptions()

# 2️⃣ Get the date range of the full DataFrame
oldest, newest = analyzer.get_date_range(analyzer.df)

# 3️⃣ Filter by a custom date range (you can use oldest/newest here!)
df_period = analyzer.filter_by_date('05/05/2025', '04/06/2025')

# Count how many times each DESCRIPCIÓN appears
# count_df = analyzer.count_description(df_period)

# 4️⃣ Sort by DESCRIPCIÓN
df_sorted = analyzer.sort_by_descripcion(df_period)

# 5️⃣ Show DataFrame
# analyzer.show_dataframe(df_sorted)

# 6️⃣ Sum CARGO for 'uber trip' (partial match, case-insensitive)
analyzer.sum_cargo_for_description(df_period, 'uber trip')

# 7️⃣ Filter rows that contain 'uber trip'
df_uber = analyzer.filter_by_description(df_period, 'uber trip')

# 8️⃣ Show filtered 'uber trip' rows
# analyzer.show_dataframe(df_uber)

# Sum TOTAL CARGO for this period
analyzer.sum_total_cargo(df_period)

# Sum CARGO per DESCRIPCIÓN (biggest spenders first)
df_cargo_per_description = analyzer.sum_cargo_per_description(df_period, step=1000)


# === NEW EXAMPLE USAGE ===

# Example: compare two periods WITHIN THIS SAME STATEMENT (same .xlsx file)

# Define first period (preferably make it before the second period)
df_period1 = analyzer.filter_by_date('05/04/2025', '04/05/2025')

# Define second period (you can adjust dates; but keep the second period at a later date than the first period)
df_period2 = analyzer.filter_by_date('05/05/2025', '04/06/2025')

# Compare them
analyzer.compare_cargo_per_description(df_period1, 'Period1', df_period2, 'Period2')  # ojo con los pagos a
                                                                                                  # meses sin intereses
                                                                                                  # esos saldrán como
                                                                                                  # que aumentaron
                                                                                                  # (el del periodo 2,
                                                                                                  # el actual) o
                                                                                                  # disminuyeron
                                                                                                  # (el del periodo 1,
                                                                                                  # el anterior), porque
                                                                                                  # son cargos
                                                                                                  # recurrentes;
                                                                                                  # aunque se refieran
                                                                                                  # al mismo pago
                                                                                                  # recurrente, entonces
                                                                                                  # sólo ten esos en
                                                                                                  # cuenta e ignóralos
                                                                                                  # en esa parte


# Example: compare two DIFFERENT statements
# You can uncomment this when you have another .xlsx file:

# analyzer2 = EstadoCuentaAnalyzer('estado_de_cuenta_junio2025_julio2025.xlsx')
# analyzer2.load_dataframe()
# df_other_period = analyzer2.filter_by_date('05/06/2025', '04/07/2025')

# analyzer.compare_cargo_per_description(df_period, 'Current Period', df_other_period, 'Other Period')
