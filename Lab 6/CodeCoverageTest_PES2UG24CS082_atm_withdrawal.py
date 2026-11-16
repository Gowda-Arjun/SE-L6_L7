"""
Code Coverage Test Suite for ATM Withdrawal Application
Student Name: Arjun Mohan Gowda
SRN: PES2UG24CS082
Lab 6: Code and Branch Coverage Analysis
"""

import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ==========================================
# Tests for withdraw()
# ==========================================

def test_withdraw_unknown_account():
    """Verify that an unsupported account type raises a ValueError."""
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(balance=10000, amount=1000, account_type="fixed_deposit", own_bank=True)


def test_withdraw_invalid_amount_negative():
    """Verify that negative withdrawal amounts raise a ValueError."""
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(balance=10000, amount=-500, account_type="savings", own_bank=True)


def test_withdraw_limit_exceeded():
    """Verify that withdrawing more than the daily limit returns 'limit exceeded'."""
    assert withdraw(balance=50000, amount=30000, account_type="savings", own_bank=True) == "limit exceeded"


def test_withdraw_other_bank_large_amount():
    """Verify other bank withdrawal (> 10000) incurs 20 + 10 = 30 fee."""
    # 20000 - 15000 - 30 = 4970
    assert withdraw(balance=20000, amount=15000, account_type="savings", own_bank=False) == 4970


def test_withdraw_insufficient_funds():
    """Verify that attempting to withdraw more than available balance returns 'insufficient funds'."""
    assert withdraw(balance=1000, amount=2000, account_type="savings", own_bank=True) == "insufficient funds"


def test_withdraw_success_own_bank():
    """Verify a successful standard withdrawal without fee."""
    assert withdraw(balance=10000, amount=2000, account_type="savings", own_bank=True) == 8000


# ==========================================
# Tests for pin_check()
# ==========================================

def test_pin_blocked_max_attempts():
    """Verify that attempts >= 3 immediately returns 'card blocked'."""
    assert pin_check(entered=1234, actual=1234, attempts=3) == "card blocked"


def test_pin_correct():
    """Verify that entering the correct PIN returns 'ok'."""
    assert pin_check(entered=1234, actual=1234, attempts=0) == "ok"


def test_pin_blocked_after_two_failed_attempts():
    """Verify that a 3rd failed attempt (attempts == 2) blocks the card."""
    assert pin_check(entered=9999, actual=1234, attempts=2) == "card blocked"


def test_pin_retry():
    """Verify that an incorrect PIN with attempts < 2 returns 'retry'."""
    assert pin_check(entered=9999, actual=1234, attempts=1) == "retry"


# ==========================================
# Tests for note_breakup()
# ==========================================

def test_note_breakup_invalid_amount():
    """Verify that amounts not divisible by 100 raise a ValueError."""
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(amount=350)


def test_note_breakup_with_200_notes():
    """Verify note breakup when remaining amount requires Rs 200 note(s)."""
    # 800: 500*1 + 200*1 + 100*1 -> (1, 1, 1)
    assert note_breakup(amount=800) == (1, 1, 1)


def test_note_breakup_without_200_notes():
    """Verify note breakup when remaining amount < 200 (no Rs 200 notes)."""
    # 600: 500*1 + 200*0 + 100*1 -> (1, 0, 1)
    assert note_breakup(amount=600) == (1, 0, 1)
