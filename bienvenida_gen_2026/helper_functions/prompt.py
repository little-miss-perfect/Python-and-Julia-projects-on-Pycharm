def prompt_yes_no(message):
    """
    Prompt user for a yes/no question until valid input ('y' or 'n') is received.

    Returns:
    - True if user entered 'y'
    - False if user entered 'n'
    """
    while True:
        response = input(message + " (y/n): ").strip().lower()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            print("❗ Please enter 'y' for yes or 'n' for no.")
