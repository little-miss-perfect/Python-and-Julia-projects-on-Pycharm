# experimental/main_k.py

from experimental.k_fit import SpringEstimator
from helper_functions.k_database import save_k_value
from helper_functions.prompt import prompt_yes_no


def main():
    print("\n🔬 Bungee Cord Calibration: Estimate Spring Constant (k)\n")

    # Prompt for unstretched bungee length
    while True:
        try:
            l0 = float(input("Enter the unstretched length of the bungee cord (in meters): "))
            if l0 > 0:
                break
            else:
                print("❗ Please enter a positive value.")
        except ValueError:
            print("❗ Invalid input. Please enter a number.")

    # Initialize estimator: fresh session (no reused data)
    estimator = SpringEstimator(l0=l0, load_previous=False)

    print("\n✅ Ready to record measurements. Type 'q' to quit at any time.\n")

    # Loop for user input
    while True:
        mass_input = input("Enter mass (in kg) or 'q' to quit: ").strip().lower()
        if mass_input == 'q':
            break

        try:
            mass = float(mass_input)
            length = float(input("Enter stretched length (in meters): "))
        except ValueError:
            print("❗ Invalid input. Try again.\n")
            continue

        estimator.add_measurement(mass, length)
        print("✔️ Measurement recorded.")

        # Show updated estimate
        k = estimator.estimate_k()
        if k is not None:
            print(f"🧮 Current estimated spring constant: k = {k:.2f} N/m\n")
        else:
            print("ℹ️ Not enough data to estimate yet.\n")

    # After exiting loop, offer to save final result
    k_final = estimator.estimate_k()
    if k_final is not None:
        if prompt_yes_no("💾 Do you want to save this k value for future use?"):
            name = input("📝 Enter a name for this bungee cord (e.g., cord_A): ").strip().strip("'\"")
            save_k_value(name=name, k_value=k_final, l0=l0)
            print(f"✅ Saved k = {k_final:.2f} N/m under name '{name}'\n")
    else:
        print("⚠️ Not enough valid data to save k.")

    print("📁 Done.\n")


if __name__ == '__main__':
    main()
