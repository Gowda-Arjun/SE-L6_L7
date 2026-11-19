# L6_L7_18_atm_withdrawal — ATM Withdrawal

**Lab 7: Fuzz Testing using Hypothesis**  
**Student:** Arjun Mohan Gowda (PES2UG24CS082) — Section B

## About

Fuzz testing ATM input processing functions using Python's `hypothesis` library to discover input validation bugs, crashes, and edge cases, followed by defensive programming to harden the code.

## Deliverables & Files

| File | Description |
|------|-------------|
| `atm_withdrawal.py` | Hardened application code protected against malformed inputs |
| `test_atm_withdrawal.py` | Completed Hypothesis fuzz test suite |
| `processor.py` | Symlink to `atm_withdrawal.py` for standard naming compatibility |
| `test_processor.py` | Symlink to `test_atm_withdrawal.py` for standard naming compatibility |
| `PES2UG24CS082_Output.pdf` | Form submission PDF with all terminal output screenshots |
| `PES2UG24CS082_Lab7_Fuzz_Testing_Report.md` | In-depth analysis report of fuzzing bugs, root causes, and fixes |
| `screenshots/step2_buggy_app_run.png` | Terminal screenshot of running the initial application |
| `screenshots/step4_fuzz_tests_failing.png` | Terminal screenshot of Hypothesis uncovering input validation crashes |
| `screenshots/step5_fixed_app_run.png` | Terminal screenshot of running the hardened application |
| `screenshots/step6_fuzz_tests_passing.png` | Terminal screenshot of all Hypothesis fuzz tests passing cleanly |

## Execution Commands

Ensure dependencies are installed:
```bash
pip install hypothesis pytest
```

### Run Application
```bash
python atm_withdrawal.py
```

### Run Fuzz Tests
```bash
pytest test_atm_withdrawal.py
```
*(All 3 tests pass across hundreds of randomized unicode and null inputs with zero crashes)*
