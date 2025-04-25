from src.stock_manager import add_stock, show_stock, use_stock
from src.cutting_logic import process_cuts

def print_menu():
    print("\n--- Stock Management Menu ---")
    print("1. Show Current Stock")
    print("2. Add Stock")
    print("3. Use Stock")
    print("4. Process Required Cuts")
    print("5. Exit")
    print("----------------------------")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            show_stock()

        elif choice == '2':
            length = float(input("Enter stock length (m): "))
            quantity = int(input("Enter quantity: "))
            add_stock(length, quantity)

        elif choice == '3':
            length = float(input("Enter stock length to use (m): "))
            quantity = int(input("Enter quantity to use: "))
            use_stock(length, quantity)

        elif choice == '4':
            cuts_input = input("Enter required cuts (e.g., 3.5x7, 2.1x2): ")
            required_cuts = process_cuts(cuts_input)
            print("Cutting Plan:\n")
            print(required_cuts)

        elif choice == '5':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()