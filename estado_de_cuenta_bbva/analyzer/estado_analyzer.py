import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


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