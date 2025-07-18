import os

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
