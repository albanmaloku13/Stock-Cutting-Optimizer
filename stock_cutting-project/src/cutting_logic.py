from src.stock_manager import load_stock, use_stock, add_stock
from itertools import combinations

def can_cut(table_length, cut_length):
    return table_length >= cut_length

def cut_table(table_length, cut_length):
    return table_length - cut_length

def handle_scrap(leftover):
    if leftover > 1.5:
        print(f"Leftover of {leftover:.2f}m added back to stock.")
        add_stock(leftover, 1)  # Add leftover > 1.5m back to stock
    elif leftover <= 0.3:
        print(f"Leftover of {leftover:.2f}m is acceptable scrap. Discarded.")
    else:
        print(f"Leftover of {leftover:.2f}m is non-acceptable scrap. Discarded.")

def parse_required_cuts(cuts_input):
    required_cuts = []
    try:
        # Parse the input cuts, splitting by commas and processing each item
        for item in cuts_input.split(","):
            length, qty = item.strip().split("x")
            length = float(length.strip())  # Convert length to float
            qty = int(qty.strip())  # Convert quantity to int
            required_cuts.extend([length] * qty)  # Add 'length' qty times
    except Exception as e:
        raise ValueError(f"Error parsing cuts: {e}")
    return required_cuts

def process_cuts(cuts_input):
    # Parse cuts input
    required_cuts = parse_required_cuts(cuts_input)

    stock = load_stock()
    result = []

    print("\nAvailable stock:")
    for length in sorted(stock.keys(), key=lambda x: -float(x)):
        print(f"{length}m x {stock[length]}")

    cuts_remaining = required_cuts[:]

    for length in sorted(stock.keys(), key=lambda x: -float(x)):
        table_length = float(length)
        qty_available = stock[length]

        while qty_available > 0 and cuts_remaining:
            best_combo = find_best_combination(cuts_remaining, table_length)
            if best_combo:
                total_cut = sum(best_combo)
                leftover = table_length - total_cut
                for cut in best_combo:
                    cuts_remaining.remove(cut)
                result.append(f"Used {length}m table for cuts: {best_combo}, leftover: {leftover:.2f}m")
                handle_scrap(leftover)
                qty_available -= 1
                stock[length] -= 1
            else:
                break

    for cut in cuts_remaining:
        result.append(f"Unfulfilled cut: {cut}m — No suitable stock found.")

    result.append("\nRemaining stock after cuts:")
    for length in sorted(stock.keys(), key=lambda x: -float(x)):
        result.append(f"{length}m x {stock[length]}")

    return "\n".join(result)

def find_best_combination(cuts, table_length):
    best_fit = None
    min_leftover = table_length

    # Go through combinations of cuts, starting with the largest possible
    for r in range(1, min(6, len(cuts)) + 1):
        for combo in combinations(cuts, r):
            combo_floats = [float(cut) for cut in combo]  # Ensure all are floats here
            total = sum(combo_floats)
            leftover = table_length - total
            if leftover >= 0:
                # Select combinations with acceptable or minimal scrap
                if leftover <= 0.3 or leftover > 1.5:
                    if leftover < min_leftover:
                        best_fit = combo_floats
                        min_leftover = leftover

    return list(best_fit) if best_fit else None