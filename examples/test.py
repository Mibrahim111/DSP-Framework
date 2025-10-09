import os
import matplotlib.pyplot as plt
from framework.signals import Signal
from framework.signals import generate_signal

def list_gen_files(folder="."):
    """List all signal generation parameter files (.txt)."""
    return [f for f in os.listdir(folder) if f.endswith(".txt")]


def main():
    print("=== DSP Signal Generator Tester ===")
    folder = input("Enter folder containing generation files (default='.'): ").strip() or "."
    print()

    files = list_gen_files(folder)
    if not files:
        print("❌ No generation files (.txt) found.")
        return

    print("Available generation parameter files:")
    for i, f in enumerate(files):
        print(f"  [{i}] {f}")

    choice = input("Enter index of file to generate signal from: ").strip()
    if not choice.isdigit() or int(choice) not in range(len(files)):
        print("❌ Invalid selection.")
        return

    file_path = os.path.join(folder, files[int(choice)])
    print(f"\n📄 Reading parameters from: {file_path}\n")

    # preview file contents
    with open(file_path, "r") as f:
        print("--- File Contents ---")
        print(f.read())
        print("---------------------\n")

    try:
        sig = generate_signal(file_path)
        print("✅ Signal generated successfully!\n")
        print(sig)

        plot_choice = input("\nShow plot? (y/n): ").strip().lower()
        if plot_choice == "y":
            sig.plot()

        save_choice = input("Save signal to file? (y/n): ").strip().lower()
        if save_choice == "y":
            out_path = os.path.join(folder, sig.name + "_generated.txt")
            with open(out_path, "w") as f:
                f.write(str(sig))
            print(f"💾 Signal info saved to {out_path}")

    except Exception as e:
        print(f"❌ Error during signal generation: {e}")


if __name__ == "__main__":
    main()
