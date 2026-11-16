"""
Branch Coverage Test Suite for ATM Withdrawal Application
Student Name: Arjun Mohan Gowda
SRN: PES2UG24CS082
Lab 6: Code and Branch Coverage Analysis

This test suite covers all decision structures and conditional branches
in atm_withdrawal.py to achieve 100% Line Coverage and 100% Branch Coverage.
"""

import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ==========================================
# Tests for withdraw() - Branch Coverage
# ==========================================

def test_withdraw_unknown_account_branch():
    """Branch: account_type not in DAILY_LIMIT (True branch)."""
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(balance=50000, amount=1000, account_type="fixed_deposit", own_bank=True)


def test_withdraw_amount_zero():
    """Branch: amount <= 0 evaluates to True (amount = 0)."""
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(balance=50000, amount=0, account_type="savings", own_bank=True)


def test_withdraw_amount_negative():
    """Branch: amount <= 0 evaluates to True (amount < 0)."""
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(balance=50000, amount=-500, account_type="savings", own_bank=True)


def test_withdraw_amount_positive_not_multiple_of_100():
    """Branch: amount <= 0 is False, amount % 100 != 0 is True."""
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(balance=50000, amount=350, account_type="savings", own_bank=True)


def test_withdraw_savings_limit_exceeded():
    """Branch: amount > DAILY_LIMIT['savings'] evaluates to True."""
    assert withdraw(balance=100000, amount=30000, account_type="savings", own_bank=True) == "limit exceeded"


def test_withdraw_current_limit_exceeded():
    """Branch: amount > DAILY_LIMIT['current'] evaluates to True."""
    assert withdraw(balance=100000, amount=60000, account_type="current", own_bank=True) == "limit exceeded"


def test_withdraw_own_bank_success():
    """
    Branches:
    - not own_bank is False (own_bank=True, fee remains 0).
    - amount + fee > balance is False.
    """
    assert withdraw(balance=10000, amount=5000, account_type="savings", own_bank=True) == 5000


def test_withdraw_current_account_own_bank_success():
    """Verify standard withdrawal on a current account within daily limit."""
    assert withdraw(balance=100000, amount=40000, account_type="current", own_bank=True) == 60000


def test_withdraw_other_bank_under_10k():
    """
    Branches:
    - not own_bank is True (fee = 20).
    - amount > 10000 is False (amount <= 10000, fee remains 20).
    - amount + fee > balance is False.
    """
    # 10000 - 5000 - 20 = 4980
    assert withdraw(balance=10000, amount=5000, account_type="savings", own_bank=False) == 4980


def test_withdraw_other_bank_over_10k():
    """
    Branches:
    - not own_bank is True (fee = 20).
    - amount > 10000 is True (fee += 10, total fee = 30).
    - amount + fee > balance is False.
    """
    # 30000 - 15000 - 30 = 14970
    assert withdraw(balance=30000, amount=15000, account_type="savings", own_bank=False) == 14970


def test_withdraw_insufficient_funds_pure_amount():
    """Branch: amount + fee > balance is True (balance < amount, fee = 0)."""
    assert withdraw(balance=1000, amount=2000, account_type="savings", own_bank=True) == "insufficient funds"


def test_withdraw_insufficient_funds_due_to_fee():
    """Branch: amount <= balance but amount + fee > balance (fee tips over balance)."""
    # balance = 5000, amount = 5000, fee = 20 -> 5020 > 5000
    assert withdraw(balance=5000, amount=5000, account_type="savings", own_bank=False) == "insufficient funds"


# ==========================================
# Tests for pin_check() - Branch Coverage
# ==========================================

def test_pin_check_attempts_ge_3():
    """Branch: attempts >= 3 evaluates to True."""
    assert pin_check(entered=1234, actual=1234, attempts=3) == "card blocked"
    assert pin_check(entered=1234, actual=1234, attempts=4) == "card blocked"


def test_pin_check_entered_equals_actual():
    """Branch: attempts < 3 is True, entered == actual is True."""
    assert pin_check(entered=1234, actual=1234, attempts=0) == "ok"
    assert pin_check(entered=9999, actual=9999, attempts=1) == "ok"


def test_pin_check_card_blocked_second_attempt_failure():
    """Branch: attempts < 3 is True, entered != actual is True, attempts == 2 is True."""
    assert pin_check(entered=1111, actual=2222, attempts=2) == "card blocked"


def test_pin_check_retry():
    """Branch: attempts < 3 is True, entered != actual is True, attempts == 2 is False."""
    assert pin_check(entered=1111, actual=2222, attempts=0) == "retry"
    assert pin_check(entered=1111, actual=2222, attempts=1) == "retry"


# ==========================================
# Tests for note_breakup() - Branch Coverage
# ==========================================

def test_note_breakup_invalid_amount():
    """Branch: amount % 100 != 0 evaluates to True."""
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(amount=250)


def test_note_breakup_remaining_ge_200_with_100_remainder():
    """
    Branch: remaining >= 200 is True (remaining = 300).
    300 // 200 = 1, remaining = 100 -> 100 // 100 = 1.
    """
    # 800: notes_500=1, rem=300 -> notes_200=1, rem=100 -> notes_100=1
    assert note_breakup(amount=800) == (1, 1, 1)


def test_note_breakup_remaining_ge_200_no_100_remainder():
    """
    Branch: remaining >= 200 is True (remaining = 400).
    400 // 200 = 2, remaining = 0 -> 0 // 100 = 0.
    """
    # 900: notes_500=1, rem=400 -> notes_200=2, rem=0 -> notes_100=0
    assert note_breakup(amount=900) == (1, 2, 0)


def test_note_breakup_remaining_lt_200_with_100():
    """
    Branch: remaining >= 200 is False (remaining = 100).
    notes_200 = 0, 100 // 100 = 1.
    """
    # 600: notes_500=1, rem=100 -> notes_200=0, notes_100=1
    assert note_breakup(amount=600) == (1, 0, 1)


def test_note_breakup_remaining_zero():
    """
    Branch: remaining >= 200 is False (remaining = 0).
    notes_200 = 0, 0 // 100 = 0.
    """
    # 500: notes_500=1, rem=0 -> notes_200=0, notes_100=0
    assert note_breakup(amount=500) == (1, 0, 0)


def test_note_breakup_under_500():
    """Branch combinations for amounts strictly less than 500."""
    # 300: 0 x 500, rem=300 >= 200 -> 1 x 200, 1 x 100
    assert note_breakup(amount=300) == (0, 1, 1)
    # 200: 0 x 500, rem=200 >= 200 -> 1 x 200, 0 x 100
    assert note_breakup(amount=200) == (0, 1, 0)
    # 100: 0 x 500, rem=100 < 200  -> 0 x 200, 1 x 100
    assert note_breakup(amount=100) == (0, 0, 1)
