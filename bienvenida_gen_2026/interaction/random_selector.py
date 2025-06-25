import random  # Built-in module to select random elements

class RandomSelector:
    """
    Class to randomly select participants from a list of IDs (desk numbers, names, etc.).
    Optionally prevents repeated selection until the list is reset.
    """

    def __init__(self, ids: list, allow_repeats=False):
        """
        Initialize the selector.

        Parameters:
        - ids: list of participant identifiers (e.g., ["A1", "A2", "A3"])
        - allow_repeats: if True, participants can be selected multiple times;
                         if False, each one is selected only once per cycle
        """
        self.original_ids = ids.copy()     # Store the full original list
        self.remaining_ids = ids.copy()    # Working list to track unused IDs (if repeats are off)
        self.allow_repeats = allow_repeats # Whether repeated selection is allowed
        self.history = []                  # Track who has been selected so far

    def pick_random(self):
        """
        Select a random participant.

        Returns:
        - One identifier (e.g. desk number) randomly selected

        Behavior:
        - If repeats are allowed → pick from the full list every time
        - If repeats are not allowed → pick from unused list until it's empty
        """
        if self.allow_repeats:
            # Choose from the full original list, even if already picked
            choice = random.choice(self.original_ids)
        else:
            # If everyone has already been picked once, raise an error
            if not self.remaining_ids:
                raise ValueError("All participants have been selected. Call reset() to restart.")

            # Choose from the remaining unused IDs
            choice = random.choice(self.remaining_ids)

            # Remove chosen ID from remaining list
            self.remaining_ids.remove(choice)

        # Save the selection in the history log
        self.history.append(choice)

        return choice

    def remove_participant(self, name):
        """
        Safely remove a participant from the remaining list (used when repeats are not allowed).

        Parameters:
        - name: identifier (e.g., desk number or name) to remove
        """
        # Only modify the pool if repeat selections are not allowed
        if not self.allow_repeats:
            # Only remove if the participant is still in the list
            if name in self.remaining_ids:
                self.remaining_ids.remove(name)

    def reset(self):
        """
        Reset the internal state so selection can begin again from the full list.
        """
        self.remaining_ids = self.original_ids.copy()  # Restore all options
        self.history = []                              # Clear selection history

    def get_history(self):
        """
        Return the list of all selected participants so far.

        Returns:
        - List of previously selected identifiers
        """
        return self.history
