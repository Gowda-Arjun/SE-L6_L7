# Lab 7: Fuzzing for Input Validation Bugs — Analysis Report

**Student Name:** Arjun Mohan Gowda  
**SRN:** PES2UG24CS082  
**Section:** B  
**Course:** Software Engineering  
**Application Under Test:** ATM Withdrawal Processor (`atm_withdrawal.py`)  

---

## 1. Objective and Overview

The objective of this lab is to explore **Fuzz Testing** as a security and quality assurance technique using Python's **Hypothesis** property-based testing library. We identify input validation vulnerabilities and unhandled crashes in naive string/numeric parsing functions and harden them through defensive programming.

---

## 2. Functions Under Test

The application consists of three primary helper functions for ATM operations:

1. `notes_needed(amount)`: Calculates the number of Rs. 100 denomination notes needed.
2. `mask_card(card_number)`: Masks a 16-digit card number, displaying only the last group of four digits.
3. `average_withdrawal(amounts_csv)`: Computes the integer average of a comma-separated list of withdrawal amounts.

---

## 3. Discovered Vulnerabilities via Fuzzing (Step 4)

When fuzz testing with `@given(st.text() | st.none())`, Hypothesis generated diverse malformed inputs and minimized them to minimal falsifying examples:

| Function | Malformed Input (`s`) | Unhandled Exception | Root Cause |
|---|---|---|---|
| `notes_needed` | `None` | `AttributeError: 'NoneType' object has no attribute 'replace'` | Missing null/type check before calling string methods. |
| `notes_needed` | `""` (empty string) | `ValueError: invalid literal for int() with base 10: ''` | Naive `int()` conversion without verifying numeric characters. |
| `mask_card` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` | Missing null/type check before calling `.split()`. |
| `mask_card` | `""` or short strings | `IndexError: list index out of range` | Assumed `.split()` always returns at least 4 space-separated elements (`groups[3]`). |
| `average_withdrawal` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` | Missing null/type check. |
| `average_withdrawal` | `""` | `ValueError: invalid literal for int() with base 10: ''` | `"".split(',')` results in `['']`, causing `int('')` to crash. |
| `average_withdrawal` | `",,"` or non-numeric | `ZeroDivisionError` / `ValueError` | Empty or non-numeric lists cause `len(amounts) == 0` or conversion failure. |

---

## 4. Hardening and Defensive Programming Fixes (Step 5)

Each function was refactored with robust defensive validation:

1. **`notes_needed(amount)` Fix:**
   - Type verification: validates `isinstance(amount, str)`. Returns `0` for `None` or non-strings.
   - Cleans formatting (commas, leading/trailing whitespace).
   - Validates that the remaining characters form a valid non-negative integer.
   - Safe parsing with `try...except (ValueError, OverflowError)` returning `0` on any parsing abnormality.

2. **`mask_card(card_number)` Fix:**
   - Type verification: returns default mask `"XXXX XXXX XXXX XXXX"` for `None` or non-strings.
   - Inspects space-separated groups: if $\ge 4$ groups exist, retains the last group.
   - If not standard 4 groups, extracts numeric digits: if $\ge 4$ digits exist, masks all but the last 4 digits.
   - Defaults safely to `"XXXX XXXX XXXX XXXX"` without throwing `IndexError`.

3. **`average_withdrawal(amounts_csv)` Fix:**
   - Type verification: returns `0` for `None` or non-strings.
   - Iterates through comma-separated tokens, stripping whitespace and validating each token individually.
   - Ignores empty or malformed tokens (e.g. `"500,,1000"` safely parses `[500, 1000]`).
   - Guards against `ZeroDivisionError`: checks `if not amounts: return 0` before computing `sum(amounts) // len(amounts)`.

---

## 5. Fuzz Testing Verification (Step 6)

Re-running `pytest test_atm_withdrawal.py` executes hundreds of fuzzing iterations per test with random unicode text and null inputs:
```
============================== 3 passed in 0.17s ===============================
```
All functions demonstrated 100% resilience against arbitrary and malicious inputs with zero crashes.

---

## 6. Deliverables Reference

- **Hardened Application:** [atm_withdrawal.py](file:///home/cow/github/SE-L6_L7/Lab%207/atm_withdrawal.py)
- **Hypothesis Fuzz Test Suite:** [test_atm_withdrawal.py](file:///home/cow/github/SE-L6_L7/Lab%207/test_atm_withdrawal.py)
- **Screenshots Submission PDF:** [PES2UG24CS082_Output.pdf](file:///home/cow/github/SE-L6_L7/Lab%207/PES2UG24CS082_Output.pdf)
- **Terminal Screenshots:**
  - [Step 2 Screenshot](file:///home/cow/github/SE-L6_L7/Lab%207/screenshots/step2_buggy_app_run.png)
  - [Step 4 Screenshot](file:///home/cow/github/SE-L6_L7/Lab%207/screenshots/step4_fuzz_tests_failing.png)
  - [Step 5 Screenshot](file:///home/cow/github/SE-L6_L7/Lab%207/screenshots/step5_fixed_app_run.png)
  - [Step 6 Screenshot](file:///home/cow/github/SE-L6_L7/Lab%207/screenshots/step6_fuzz_tests_passing.png)
