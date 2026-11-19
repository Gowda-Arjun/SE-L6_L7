"""
ATM Withdrawal Processor - Hardened against Malformed Inputs
Lab 7: Fuzz Testing
Student Name: Arjun Mohan Gowda
SRN: PES2UG24CS082
Section: B
"""


def notes_needed(amount):
    """
    Calculate the number of 100 denomination notes needed for an amount.
    Hardened against null, non-string, malformed, negative, or non-numeric inputs.
    """
    if not isinstance(amount, str):
        return 0
    cleaned = amount.replace(',', '').strip()
    if not cleaned or not cleaned.lstrip('-+').isdigit():
        return 0
    try:
        val = int(cleaned)
        return max(0, val // 100) if val > 0 else 0
    except (ValueError, OverflowError):
        return 0


def mask_card(card_number):
    """
    Mask a credit/debit card number, revealing only the last group or last 4 digits.
    Hardened against null, short, empty, or irregularly spaced card numbers.
    """
    if not isinstance(card_number, str):
        return "XXXX XXXX XXXX XXXX"
    groups = card_number.split()
    if len(groups) >= 4:
        return "XXXX XXXX XXXX " + groups[3]
    digits = "".join(c for c in card_number if c.isdigit())
    if len(digits) >= 4:
        return "XXXX XXXX XXXX " + digits[-4:]
    return "XXXX XXXX XXXX XXXX"


def average_withdrawal(amounts_csv):
    """
    Calculate the average withdrawal from a comma-separated string of amounts.
    Hardened against null, empty strings, missing values, non-numeric values, and division by zero.
    """
    if not isinstance(amounts_csv, str):
        return 0
    amounts = []
    for a in amounts_csv.split(','):
        cleaned = a.strip().replace(' ', '')
        if cleaned.lstrip('-+').isdigit():
            try:
                amounts.append(int(cleaned))
            except (ValueError, OverflowError):
                pass
    if not amounts:
        return 0
    return sum(amounts) // len(amounts)


def main():
    print("==== Running notes_needed ====")
    user_input = input("Enter an amount (e.g. 2,500): ")
    result = notes_needed(user_input)
    print("Number of 100 Notes:", result)

    print("\n==== Running mask_card ====")
    user_input = input("Enter a card number (e.g. 1234 5678 9012 3456): ")
    result = mask_card(user_input)
    print("Masked Card:", result)

    print("\n==== Running average_withdrawal ====")
    user_input = input("Enter withdrawals as CSV (e.g. 500,1000,2000): ")
    result = average_withdrawal(user_input)
    print("Average Withdrawal:", result)


if __name__ == "__main__":
    main()
