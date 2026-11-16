# L6_L7_18_atm_withdrawal — ATM Withdrawal

**Lab 6: Code and Branch Coverage Analysis**  
**Student:** Arjun Mohan Gowda (PES2UG24CS082) — Section B

## About

A Python module that processes ATM withdrawals with daily limits and fees, checks PIN attempts, and computes note breakups.

## Deliverables & Files

| File | Description |
|------|-------------|
| `atm_withdrawal.py` | The module under test |
| `test_atm_withdrawal.py` | Complete test file covering 100% statements and 100% branches |
| `CodeCoverageTest_PES2UG24CS082_atm_withdrawal.py` | Test suite for Code Coverage (100% line coverage) |
| `BranchCoverageTest_PES2UG24CS082_atm_withdrawal.py` | Test suite for Branch Coverage (100% branch coverage) |
| `PES2UG24CS082_Lab6_Coverage_Analysis.md` | In-depth coverage analysis report & decision matrix |
| `PES2UG24CS082_Lab6_Report.pdf` | Comprehensive PDF submission report with terminal screenshots |
| `screenshots/code_coverage_analysis.png` | Terminal output screenshot for Code Coverage |
| `screenshots/branch_coverage_analysis.png` | Terminal output screenshot for Branch Coverage |

## Running the Coverage Analysis

Ensure dependencies are installed:
```bash
pip install coverage pytest
```

### 1. Code Coverage
```bash
coverage run -m pytest CodeCoverageTest_PES2UG24CS082_atm_withdrawal.py
coverage report -m
```
Achieves **100%** statement coverage (34/34 statements).

### 2. Branch Coverage
```bash
coverage run --branch -m pytest BranchCoverageTest_PES2UG24CS082_atm_withdrawal.py
coverage report -m
```
Achieves **100%** statement coverage and **100%** branch coverage (22/22 branches).
