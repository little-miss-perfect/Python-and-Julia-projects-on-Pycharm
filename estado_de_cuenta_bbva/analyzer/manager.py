import os

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
