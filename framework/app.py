"""
    For GUI App


""" 

import os
from fileHandling import load_signal
from operations import (
    add_signals,
    subtract_signals,
    multiply_signal_byConst,
    square_signal,
    accumulate_signal,
)
import matplotlib.pyplot as plt

def list_signal_files(folder="."):
    """List all .txt signal files in a folder."""
    return [f for f in os.listdir(folder) if f.endswith(".txt")]


def select_signals(folder="."):
    """Let user choose which signals to load."""
    files = list_signal_files(folder)
    if not files:
        print("❌ No .txt signal files found in this folder.")
        return []

    print("\nAvailable signal files:")
    for i, f in enumerate(files):
        print(f"  [{i}] {f}")

    choices = input("Enter indices of signals to load (comma-separated): ").strip()
    if not choices:
        return []

    indices = [int(i) for i in choices.split(",") if i.strip().isdigit()]
    signals = [load_signal(os.path.join(folder, files[i])) for i in indices]
    return signals




def main():
    print("=== DSP Signal Operations Tester ===")
    folder = input("Enter folder containing .txt signals (default='.'): ").strip() or "."
    print()

    while True:
        print("\nSelect operation:")
        print("1. Add signals")
        print("2. Subtract signals")
        print("3. Multiply signal by constant")
        print("4. Square signal")
        print("5. Accumulate signal")
        print("6. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            signals = select_signals(folder)
            if len(signals) < 2:
                print("❌ Need at least 2 signals to add.")
                continue
            result = add_signals(*signals)
            print("\n✅ Added Signal Info:\n", result)
            result.plot()

        elif choice == "2":
            print("\nSelect the first and second signals for subtraction:")
            signals = select_signals(folder)
            if len(signals) != 2:
                print("❌ Need exactly 2 signals for subtraction.")
                continue
            result = subtract_signals(signals[0], signals[1])
            print("\n✅ Subtracted Signal Info:\n", result)
            result.plot()

        elif choice == "3":
            signals = select_signals(folder)
            if len(signals) != 1:
                print("❌ Select exactly one signal.")
                continue
            const = float(input("Enter multiplication constant: "))
            result = multiply_signal_byConst(signals[0], const)
            print("\n✅ Scaled Signal Info:\n", result)
            result.plot()

        elif choice == "4":
            signals = select_signals(folder)
            if len(signals) != 1:
                print("❌ Select exactly one signal.")
                continue
            result = square_signal(signals[0])
            print("\n✅ Squared Signal Info:\n", result)
            result.plot()

        elif choice == "5":
            signals = select_signals(folder)
            if len(signals) != 1:
                print("❌ Select exactly one signal.")
                continue
            result = accumulate_signal(signals[0])
            print("\n✅ Accumulated Signal Info:\n", result)
            result.plot()

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
