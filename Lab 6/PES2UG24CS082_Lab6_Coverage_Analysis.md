# Lab 6: Code and Branch Coverage Analysis Report

**Student Name:** Arjun Mohan Gowda  
**SRN:** PES2UG24CS082  
**Section:** B  
**Course:** Software Engineering  
**Application Under Test:** ATM Withdrawal System (`atm_withdrawal.py`)  

---

## 1. Executive Summary

This report documents the code and branch coverage analysis for the ATM Withdrawal system (`atm_withdrawal.py`). Starting from an initial baseline of **41% line coverage** and **38% branch coverage**, comprehensive test suites were developed using `pytest` and Python's `coverage` library to systematically eliminate untested code paths.

- **Code Coverage Achieved:** **100%** (34/34 statements)
- **Branch Coverage Achieved:** **100%** (22/22 branches covered)
- **All Test Suites Passed:** 22/22 test cases passing with zero failures.

---

## 2. System Under Test (`atm_withdrawal.py`)

The application consists of three critical financial transaction functions:

1. `withdraw(balance, amount, account_type, own_bank)`:
   - Validates supported account types (`savings`, `current`).
   - Validates withdrawal amounts (positive values, multiples of Rs. 100).
   - Enforces daily limits (`Rs. 25,000` for savings, `Rs. 50,000` for current).
   - Computes ATM fees (`Rs. 0` for own bank; `Rs. 20` flat fee + `Rs. 10` surcharge for amounts > `Rs. 10,000` on other banks).
   - Verifies sufficient account balance including applicable fees.

2. `pin_check(entered, actual, attempts)`:
   - Enforces 3-strike security policy.
   - Blocks card immediately if prior failed attempts $\ge 3$.
   - Authenticates matching PIN (`"ok"`).
   - Blocks card on 3rd failed attempt (`attempts == 2`).
   - Allows retry if attempts $< 2$.

3. `note_breakup(amount)`:
   - Validates amount denomination (must be multiple of Rs. 100).
   - Greedy algorithm allocating denominations of Rs. 500, Rs. 200, and Rs. 100 notes.

---

## 3. Coverage Analysis Progression

### 3.1 Initial Baseline Coverage
The starter test file (`test_atm_withdrawal.py`) contained only two test cases:
```
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
atm_withdrawal.py           34     20    41%   6, 8, 10, 13-15, 17, 23, 26-28, 32-41
TOTAL                       40     20    50%

Name                     Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------
atm_withdrawal.py           34     20     22      7    38%   6, 8, 10, 13-15, 17, 23, 26-28, 32-41
TOTAL                       40     20     22      7    44%
```
**Observation:** More than half of the code remained untested, including all edge-case validations, error handling, other-bank fee calculations, PIN locking logic, and denomination breakups.

---

### 3.2 Step 1: Code (Line) Coverage ($\ge 90\%$)

**Test Suite:** `CodeCoverageTest_PES2UG24CS082_atm_withdrawal.py`  
**Goal:** Execute every single line of source code.

#### Commands Executed:
```bash
coverage run -m pytest CodeCoverageTest_PES2UG24CS082_atm_withdrawal.py
coverage report -m
```

#### Code Coverage Results:
```
============================== 13 passed in 0.04s ==============================
Name                                               Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------
CodeCoverageTest_PES2UG24CS082_atm_withdrawal.py      31      0   100%
atm_withdrawal.py                                     34      0   100%
--------------------------------------------------------------------------------
TOTAL                                                 65      0   100%
```

#### Line Coverage vs Branch Coverage Insight:
When running `--branch` on this initial 100% line coverage suite:
```
Name                   Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------
atm_withdrawal.py         34      0     22      1    98%   14->16
```
Even though **100% line coverage** was achieved, branch coverage flagged `14->16` as missing.
- **Line 14:** `if amount > 10000:` inside `if not own_bank:`.
- In the line-coverage test, an amount $> 10000$ was used to execute line 15 (`fee += 10`). This executed every statement in the function, giving 100% line coverage!
- However, the decision branch where `not own_bank` is true but `amount <= 10000` was **never exercised**. The line `14->16` (bypassing line 15 when condition is false) was completely untested.
- This demonstrates why line coverage alone provides a false sense of security.

---

### 3.3 Step 2: Branch Coverage ($\ge 90\% \rightarrow 100\%$)

**Test Suite:** `BranchCoverageTest_PES2UG24CS082_atm_withdrawal.py`  
**Goal:** Exercise every branch of every decision condition to both `True` and `False`, including compound conditions and edge cases.

#### Commands Executed:
```bash
coverage run --branch -m pytest BranchCoverageTest_PES2UG24CS082_atm_withdrawal.py
coverage report -m
```

#### Branch Coverage Results:
```
============================== 22 passed in 0.05s ==============================
Name                                                 Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------------------------------------
BranchCoverageTest_PES2UG24CS082_atm_withdrawal.py      56      0      0      0   100%
atm_withdrawal.py                                       34      0     22      0   100%
------------------------------------------------------------------------------------------------
TOTAL                                                   90      0     22      0   100%
```

**Outcome:** Achieved complete **100% Statement Coverage** and **100% Branch Coverage** across all 22 control flow branches.

---

## 4. Branch Traceability Matrix

The table below maps each control structure in `atm_withdrawal.py` to the corresponding test cases exercising both boolean branches:

| Function | Line | Decision Condition | True Path Test Case | False Path Test Case |
|---|---|---|---|---|
| `withdraw` | 5 | `if account_type not in DAILY_LIMIT` | `test_withdraw_unknown_account_branch` | `test_withdraw_own_bank_success` |
| `withdraw` | 7 | `if amount <= 0` | `test_withdraw_amount_zero`, `test_withdraw_amount_negative` | `test_withdraw_own_bank_success` |
| `withdraw` | 7 | `or amount % 100 != 0` | `test_withdraw_amount_positive_not_multiple_of_100` | `test_withdraw_own_bank_success` |
| `withdraw` | 9 | `if amount > DAILY_LIMIT[account_type]` | `test_withdraw_savings_limit_exceeded`, `test_withdraw_current_limit_exceeded` | `test_withdraw_own_bank_success` |
| `withdraw` | 12 | `if not own_bank` | `test_withdraw_other_bank_under_10k`, `test_withdraw_other_bank_over_10k` | `test_withdraw_own_bank_success` |
| `withdraw` | 14 | `if amount > 10000` (under `not own_bank`) | `test_withdraw_other_bank_over_10k` (fee = 30) | `test_withdraw_other_bank_under_10k` (fee = 20) |
| `withdraw` | 16 | `if amount + fee > balance` | `test_withdraw_insufficient_funds_pure_amount`, `test_withdraw_insufficient_funds_due_to_fee` | `test_withdraw_own_bank_success` |
| `pin_check` | 22 | `if attempts >= 3` | `test_pin_check_attempts_ge_3` | `test_pin_check_entered_equals_actual` |
| `pin_check` | 24 | `if entered == actual` | `test_pin_check_entered_equals_actual` | `test_pin_check_card_blocked_second_attempt_failure` |
| `pin_check` | 26 | `if attempts == 2` | `test_pin_check_card_blocked_second_attempt_failure` | `test_pin_check_retry` |
| `note_breakup` | 32 | `if amount % 100 != 0` | `test_note_breakup_invalid_amount` | `test_note_breakup_remaining_ge_200_with_100_remainder` |
| `note_breakup` | 36 | `if remaining >= 200` | `test_note_breakup_remaining_ge_200_with_100_remainder`, `test_note_breakup_remaining_ge_200_no_100_remainder` | `test_note_breakup_remaining_lt_200_with_100`, `test_note_breakup_remaining_zero` |

---

## 5. Key Learnings & Takeaways

1. **Line Coverage is Necessary but Insufficient:** A test suite can touch 100% of code lines while skipping vital decision branches. For example, testing only the branch where `amount > 10000` executes line 15, but leaves the standard non-surcharged path untested.
2. **Short-Circuit Evaluation in Compound Conditions:** In `amount <= 0 or amount % 100 != 0`, testing negative values satisfies the condition early without testing the modulo check. A dedicated test with positive numbers not divisible by 100 (e.g., 350) is mandatory for branch completeness.
3. **Boundary Value Testing:** Critical boundaries were tested:
   - Exact daily limit vs daily limit + 1
   - Zero amount vs negative amount
   - Attempts at threshold (attempts = 2 vs attempts = 3)
   - Balance exactly covering amount vs balance short due to fee addition.
