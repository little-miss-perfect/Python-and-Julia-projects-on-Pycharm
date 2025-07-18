import os
import warnings
from analyzer.manager import StatementManager
from analyzer.estado_analyzer import EstadoCuentaAnalyzer
from helpers.date_utils import analyze_date_coverage


warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

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
