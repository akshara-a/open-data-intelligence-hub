# Tax Input Reconciliation Audit

> Educational example only. Not a tax filing, tax advice, or a determination of property classification, bonus-depreciation eligibility, or elections.

## Processing summary

- Normalized assets: 101
- Jurisdiction/tax year: US federal / 2025
- Rule source: IRS Publication 946 (2025), MACRS percentage tables (Table A-1): https://www.irs.gov/publications/p946
- Ruleset ID: US-FEDERAL-2025-PUB946-MACRS-GDS-HY-DEMO-v1
- Reconciliation key: exact asset ID
- Conflicting non-empty source values: rejected; no precedence was guessed
- Special-depreciation percentage: supplied as an explicit assumption; eligibility and elections are not determined by this tool
- Optional narrative route: deterministic fallback (cloud/local generation unavailable)

## Generated overview

If present, the optional model-generated narrative is non-authoritative; use the source records and calculations below for verification.

> The optional language-model narrative was unavailable; the mathematical audit below was generated deterministically.

## Calculation details

The bundled demonstration implements the IRS Publication 946 (2025) MACRS GDS half-year percentage table for explicitly supplied 5- or 7-year recovery classes. Reported year: 2025. It does not classify assets or determine bonus eligibility, section 179, listed property limits, business-use qualification, or other elections.

`business depreciable basis = cost x business use %`

`special allowance = business depreciable basis x supplied special-depreciation %`

`MACRS amount = (business depreciable basis - special allowance) x Table A-1 rate`

Amounts are rounded to two decimal places using round-half-up for this demonstration. The supplied residual value is not used by MACRS. Calculations reject non-zero residual values rather than silently applying straight-line salvage assumptions.

### Asset DEMO-001

- Description: Office workstation
- Source files: demo_asset.txt, sample_assets.csv:2
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-01-15
- Cost: 1250.00
- Business use: 100.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 1250.00
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 1250.00
- MACRS depreciation amount: 250.00
- Total annual depreciation estimate: 250.00

### Asset DEMO-002

- Description: Laptop computer
- Source files: sample_assets.csv:3
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-01-01
- Cost: 480.00
- Business use: 70.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 336.00
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 336.00
- MACRS depreciation amount: 48.01
- Total annual depreciation estimate: 48.01

### Asset DEMO-003

- Description: Desktop workstation
- Source files: sample_assets.csv:4
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-02-02
- Cost: 1223.01
- Business use: 75.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 917.26
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 917.26
- MACRS depreciation amount: 183.45
- Total annual depreciation estimate: 183.45

### Asset DEMO-004

- Description: Office printer
- Source files: sample_assets.csv:5
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-03-03
- Cost: 1966.02
- Business use: 80.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 1572.82
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 1572.82
- MACRS depreciation amount: 314.56
- Total annual depreciation estimate: 314.56

### Asset DEMO-005

- Description: Network switch
- Source files: sample_assets.csv:6
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-04-04
- Cost: 2709.03
- Business use: 85.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 2302.68
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 2302.68
- MACRS depreciation amount: 460.54
- Total annual depreciation estimate: 460.54

### Asset DEMO-006

- Description: Office desk
- Source files: sample_assets.csv:7
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-05-05
- Cost: 3452.04
- Business use: 90.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 3106.84
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 3106.84
- MACRS depreciation amount: 443.97
- Total annual depreciation estimate: 443.97

### Asset DEMO-007

- Description: Conference table
- Source files: sample_assets.csv:8
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-06-06
- Cost: 4195.05
- Business use: 95.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 3985.30
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 3985.30
- MACRS depreciation amount: 797.06
- Total annual depreciation estimate: 797.06

### Asset DEMO-008

- Description: Task chair
- Source files: sample_assets.csv:9
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-07-07
- Cost: 4938.06
- Business use: 100.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 4938.06
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 4938.06
- MACRS depreciation amount: 987.61
- Total annual depreciation estimate: 987.61

### Asset DEMO-009

- Description: Filing cabinet
- Source files: sample_assets.csv:10
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-08-08
- Cost: 5681.07
- Business use: 70.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 3976.75
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 3976.75
- MACRS depreciation amount: 795.35
- Total annual depreciation estimate: 795.35

### Asset DEMO-010

- Description: Power tool set
- Source files: sample_assets.csv:11
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-09-09
- Cost: 6424.08
- Business use: 75.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 4818.06
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 4818.06
- MACRS depreciation amount: 688.50
- Total annual depreciation estimate: 688.50

### Asset DEMO-011

- Description: Diagnostic equipment
- Source files: sample_assets.csv:12
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-10-10
- Cost: 7167.09
- Business use: 80.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 5733.67
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 5733.67
- MACRS depreciation amount: 1146.73
- Total annual depreciation estimate: 1146.73

### Asset DEMO-012

- Description: Delivery equipment
- Source files: sample_assets.csv:13
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-11-11
- Cost: 7910.10
- Business use: 85.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 6723.59
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 6723.59
- MACRS depreciation amount: 1344.72
- Total annual depreciation estimate: 1344.72

### Asset DEMO-013

- Description: Server equipment
- Source files: sample_assets.csv:14
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-12-12
- Cost: 8653.11
- Business use: 90.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 7787.80
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 7787.80
- MACRS depreciation amount: 1557.56
- Total annual depreciation estimate: 1557.56

### Asset DEMO-014

- Description: Telephone system
- Source files: sample_assets.csv:15
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-01-13
- Cost: 9396.12
- Business use: 95.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 8926.31
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 8926.31
- MACRS depreciation amount: 1275.57
- Total annual depreciation estimate: 1275.57

### Asset DEMO-015

- Description: Point-of-sale terminal
- Source files: sample_assets.csv:16
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-02-14
- Cost: 10139.13
- Business use: 100.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 10139.13
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 10139.13
- MACRS depreciation amount: 2027.83
- Total annual depreciation estimate: 2027.83

### Asset DEMO-016

- Description: Workshop machinery
- Source files: sample_assets.csv:17
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-03-15
- Cost: 10882.14
- Business use: 70.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 7617.50
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 7617.50
- MACRS depreciation amount: 1523.50
- Total annual depreciation estimate: 1523.50

### Asset DEMO-017

- Description: Storage shelving
- Source files: sample_assets.csv:18
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-04-16
- Cost: 11625.15
- Business use: 75.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 8718.86
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 8718.86
- MACRS depreciation amount: 1743.77
- Total annual depreciation estimate: 1743.77

### Asset DEMO-018

- Description: Camera equipment
- Source files: sample_assets.csv:19
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-05-17
- Cost: 12368.16
- Business use: 80.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 9894.53
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 9894.53
- MACRS depreciation amount: 1413.93
- Total annual depreciation estimate: 1413.93

### Asset DEMO-019

- Description: Laboratory equipment
- Source files: sample_assets.csv:20
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-06-18
- Cost: 13111.17
- Business use: 85.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 11144.49
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 11144.49
- MACRS depreciation amount: 2228.90
- Total annual depreciation estimate: 2228.90

### Asset DEMO-020

- Description: Warehouse equipment
- Source files: sample_assets.csv:21
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-07-19
- Cost: 13854.18
- Business use: 90.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 12468.76
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 12468.76
- MACRS depreciation amount: 2493.75
- Total annual depreciation estimate: 2493.75

### Asset DEMO-021

- Description: Office equipment
- Source files: sample_assets.csv:22
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-08-20
- Cost: 14597.19
- Business use: 95.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 13867.33
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 13867.33
- MACRS depreciation amount: 2773.47
- Total annual depreciation estimate: 2773.47

### Asset DEMO-022

- Description: Laptop computer
- Source files: sample_assets.csv:23
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-09-21
- Cost: 590.20
- Business use: 100.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 590.20
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 590.20
- MACRS depreciation amount: 84.34
- Total annual depreciation estimate: 84.34

### Asset DEMO-023

- Description: Desktop workstation
- Source files: sample_assets.csv:24
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-10-22
- Cost: 1333.21
- Business use: 70.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 933.25
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 933.25
- MACRS depreciation amount: 186.65
- Total annual depreciation estimate: 186.65

### Asset DEMO-024

- Description: Office printer
- Source files: sample_assets.csv:25
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-11-23
- Cost: 2076.22
- Business use: 75.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 1557.17
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 1557.17
- MACRS depreciation amount: 311.43
- Total annual depreciation estimate: 311.43

### Asset DEMO-025

- Description: Network switch
- Source files: sample_assets.csv:26
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-12-24
- Cost: 2819.23
- Business use: 80.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 2255.38
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 2255.38
- MACRS depreciation amount: 451.08
- Total annual depreciation estimate: 451.08

### Asset DEMO-026

- Description: Office desk
- Source files: sample_assets.csv:27
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-01-25
- Cost: 3562.24
- Business use: 85.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 3027.90
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 3027.90
- MACRS depreciation amount: 432.69
- Total annual depreciation estimate: 432.69

### Asset DEMO-027

- Description: Conference table
- Source files: sample_assets.csv:28
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-02-26
- Cost: 4305.25
- Business use: 90.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 3874.73
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 3874.73
- MACRS depreciation amount: 774.95
- Total annual depreciation estimate: 774.95

### Asset DEMO-028

- Description: Task chair
- Source files: sample_assets.csv:29
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-03-27
- Cost: 5048.26
- Business use: 95.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 4795.85
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 4795.85
- MACRS depreciation amount: 959.17
- Total annual depreciation estimate: 959.17

### Asset DEMO-029

- Description: Filing cabinet
- Source files: sample_assets.csv:30
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-04-01
- Cost: 5791.27
- Business use: 100.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 5791.27
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 5791.27
- MACRS depreciation amount: 1158.25
- Total annual depreciation estimate: 1158.25

### Asset DEMO-030

- Description: Power tool set
- Source files: sample_assets.csv:31
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-05-02
- Cost: 6534.28
- Business use: 70.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 4574.00
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 4574.00
- MACRS depreciation amount: 653.62
- Total annual depreciation estimate: 653.62

### Asset DEMO-031

- Description: Diagnostic equipment
- Source files: sample_assets.csv:32
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-06-03
- Cost: 7277.29
- Business use: 75.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 5457.97
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 5457.97
- MACRS depreciation amount: 1091.59
- Total annual depreciation estimate: 1091.59

### Asset DEMO-032

- Description: Delivery equipment
- Source files: sample_assets.csv:33
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-07-04
- Cost: 8020.30
- Business use: 80.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 6416.24
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 6416.24
- MACRS depreciation amount: 1283.25
- Total annual depreciation estimate: 1283.25

### Asset DEMO-033

- Description: Server equipment
- Source files: sample_assets.csv:34
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-08-05
- Cost: 8763.31
- Business use: 85.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 7448.81
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 7448.81
- MACRS depreciation amount: 1489.76
- Total annual depreciation estimate: 1489.76

### Asset DEMO-034

- Description: Telephone system
- Source files: sample_assets.csv:35
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-09-06
- Cost: 9506.32
- Business use: 90.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 8555.69
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 8555.69
- MACRS depreciation amount: 1222.61
- Total annual depreciation estimate: 1222.61

### Asset DEMO-035

- Description: Point-of-sale terminal
- Source files: sample_assets.csv:36
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-10-07
- Cost: 10249.33
- Business use: 95.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 9736.86
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 9736.86
- MACRS depreciation amount: 1947.37
- Total annual depreciation estimate: 1947.37

### Asset DEMO-036

- Description: Workshop machinery
- Source files: sample_assets.csv:37
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-11-08
- Cost: 10992.34
- Business use: 100.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 10992.34
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 10992.34
- MACRS depreciation amount: 2198.47
- Total annual depreciation estimate: 2198.47

### Asset DEMO-037

- Description: Storage shelving
- Source files: sample_assets.csv:38
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-12-09
- Cost: 11735.35
- Business use: 70.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 8214.75
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 8214.75
- MACRS depreciation amount: 1642.95
- Total annual depreciation estimate: 1642.95

### Asset DEMO-038

- Description: Camera equipment
- Source files: sample_assets.csv:39
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-01-10
- Cost: 12478.36
- Business use: 75.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 9358.77
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 9358.77
- MACRS depreciation amount: 1337.37
- Total annual depreciation estimate: 1337.37

### Asset DEMO-039

- Description: Laboratory equipment
- Source files: sample_assets.csv:40
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-02-11
- Cost: 13221.37
- Business use: 80.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 10577.10
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 10577.10
- MACRS depreciation amount: 2115.42
- Total annual depreciation estimate: 2115.42

### Asset DEMO-040

- Description: Warehouse equipment
- Source files: sample_assets.csv:41
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-03-12
- Cost: 13964.38
- Business use: 85.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 11869.72
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 11869.72
- MACRS depreciation amount: 2373.94
- Total annual depreciation estimate: 2373.94

### Asset DEMO-041

- Description: Office equipment
- Source files: sample_assets.csv:42
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-04-13
- Cost: 14707.39
- Business use: 90.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 13236.65
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 13236.65
- MACRS depreciation amount: 2647.33
- Total annual depreciation estimate: 2647.33

### Asset DEMO-042

- Description: Laptop computer
- Source files: sample_assets.csv:43
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-05-14
- Cost: 700.40
- Business use: 95.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 665.38
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 665.38
- MACRS depreciation amount: 95.08
- Total annual depreciation estimate: 95.08

### Asset DEMO-043

- Description: Desktop workstation
- Source files: sample_assets.csv:44
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-06-15
- Cost: 1443.41
- Business use: 100.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 1443.41
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 1443.41
- MACRS depreciation amount: 288.68
- Total annual depreciation estimate: 288.68

### Asset DEMO-044

- Description: Office printer
- Source files: sample_assets.csv:45
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-07-16
- Cost: 2186.42
- Business use: 70.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 1530.49
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 1530.49
- MACRS depreciation amount: 306.10
- Total annual depreciation estimate: 306.10

### Asset DEMO-045

- Description: Network switch
- Source files: sample_assets.csv:46
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-08-17
- Cost: 2929.43
- Business use: 75.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 2197.07
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 2197.07
- MACRS depreciation amount: 439.41
- Total annual depreciation estimate: 439.41

### Asset DEMO-046

- Description: Office desk
- Source files: sample_assets.csv:47
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-09-18
- Cost: 3672.44
- Business use: 80.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 2937.95
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 2937.95
- MACRS depreciation amount: 419.83
- Total annual depreciation estimate: 419.83

### Asset DEMO-047

- Description: Conference table
- Source files: sample_assets.csv:48
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-10-19
- Cost: 4415.45
- Business use: 85.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 3753.13
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 3753.13
- MACRS depreciation amount: 750.63
- Total annual depreciation estimate: 750.63

### Asset DEMO-048

- Description: Task chair
- Source files: sample_assets.csv:49
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-11-20
- Cost: 5158.46
- Business use: 90.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 4642.61
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 4642.61
- MACRS depreciation amount: 928.52
- Total annual depreciation estimate: 928.52

### Asset DEMO-049

- Description: Filing cabinet
- Source files: sample_assets.csv:50
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-12-21
- Cost: 5901.47
- Business use: 95.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 5606.40
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 5606.40
- MACRS depreciation amount: 1121.28
- Total annual depreciation estimate: 1121.28

### Asset DEMO-050

- Description: Power tool set
- Source files: sample_assets.csv:51
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-01-22
- Cost: 6644.48
- Business use: 100.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 6644.48
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 6644.48
- MACRS depreciation amount: 949.50
- Total annual depreciation estimate: 949.50

### Asset DEMO-051

- Description: Diagnostic equipment
- Source files: sample_assets.csv:52
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-02-23
- Cost: 7387.49
- Business use: 70.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 5171.24
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 5171.24
- MACRS depreciation amount: 1034.25
- Total annual depreciation estimate: 1034.25

### Asset DEMO-052

- Description: Delivery equipment
- Source files: sample_assets.csv:53
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-03-24
- Cost: 8130.50
- Business use: 75.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 6097.88
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 6097.88
- MACRS depreciation amount: 1219.58
- Total annual depreciation estimate: 1219.58

### Asset DEMO-053

- Description: Server equipment
- Source files: sample_assets.csv:54
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-04-25
- Cost: 8873.51
- Business use: 80.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 7098.81
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 7098.81
- MACRS depreciation amount: 1419.76
- Total annual depreciation estimate: 1419.76

### Asset DEMO-054

- Description: Telephone system
- Source files: sample_assets.csv:55
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-05-26
- Cost: 9616.52
- Business use: 85.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 8174.04
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 8174.04
- MACRS depreciation amount: 1168.07
- Total annual depreciation estimate: 1168.07

### Asset DEMO-055

- Description: Point-of-sale terminal
- Source files: sample_assets.csv:56
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-06-27
- Cost: 10359.53
- Business use: 90.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 9323.58
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 9323.58
- MACRS depreciation amount: 1864.72
- Total annual depreciation estimate: 1864.72

### Asset DEMO-056

- Description: Workshop machinery
- Source files: sample_assets.csv:57
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-07-01
- Cost: 11102.54
- Business use: 95.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 10547.41
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 10547.41
- MACRS depreciation amount: 2109.48
- Total annual depreciation estimate: 2109.48

### Asset DEMO-057

- Description: Storage shelving
- Source files: sample_assets.csv:58
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-08-02
- Cost: 11845.55
- Business use: 100.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 11845.55
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 11845.55
- MACRS depreciation amount: 2369.11
- Total annual depreciation estimate: 2369.11

### Asset DEMO-058

- Description: Camera equipment
- Source files: sample_assets.csv:59
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-09-03
- Cost: 12588.56
- Business use: 70.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 8811.99
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 8811.99
- MACRS depreciation amount: 1259.23
- Total annual depreciation estimate: 1259.23

### Asset DEMO-059

- Description: Laboratory equipment
- Source files: sample_assets.csv:60
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-10-04
- Cost: 13331.57
- Business use: 75.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 9998.68
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 9998.68
- MACRS depreciation amount: 1999.74
- Total annual depreciation estimate: 1999.74

### Asset DEMO-060

- Description: Warehouse equipment
- Source files: sample_assets.csv:61
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-11-05
- Cost: 14074.58
- Business use: 80.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 11259.66
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 11259.66
- MACRS depreciation amount: 2251.93
- Total annual depreciation estimate: 2251.93

### Asset DEMO-061

- Description: Office equipment
- Source files: sample_assets.csv:62
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-12-06
- Cost: 14817.59
- Business use: 85.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 12594.95
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 12594.95
- MACRS depreciation amount: 2518.99
- Total annual depreciation estimate: 2518.99

### Asset DEMO-062

- Description: Laptop computer
- Source files: sample_assets.csv:63
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-01-07
- Cost: 810.60
- Business use: 90.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 729.54
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 729.54
- MACRS depreciation amount: 104.25
- Total annual depreciation estimate: 104.25

### Asset DEMO-063

- Description: Desktop workstation
- Source files: sample_assets.csv:64
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-02-08
- Cost: 1553.61
- Business use: 95.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 1475.93
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 1475.93
- MACRS depreciation amount: 295.19
- Total annual depreciation estimate: 295.19

### Asset DEMO-064

- Description: Office printer
- Source files: sample_assets.csv:65
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-03-09
- Cost: 2296.62
- Business use: 100.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 2296.62
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 2296.62
- MACRS depreciation amount: 459.32
- Total annual depreciation estimate: 459.32

### Asset DEMO-065

- Description: Network switch
- Source files: sample_assets.csv:66
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-04-10
- Cost: 3039.63
- Business use: 70.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 2127.74
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 2127.74
- MACRS depreciation amount: 425.55
- Total annual depreciation estimate: 425.55

### Asset DEMO-066

- Description: Office desk
- Source files: sample_assets.csv:67
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-05-11
- Cost: 3782.64
- Business use: 75.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 2836.98
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 2836.98
- MACRS depreciation amount: 405.40
- Total annual depreciation estimate: 405.40

### Asset DEMO-067

- Description: Conference table
- Source files: sample_assets.csv:68
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-06-12
- Cost: 4525.65
- Business use: 80.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 3620.52
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 3620.52
- MACRS depreciation amount: 724.10
- Total annual depreciation estimate: 724.10

### Asset DEMO-068

- Description: Task chair
- Source files: sample_assets.csv:69
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-07-13
- Cost: 5268.66
- Business use: 85.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 4478.36
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 4478.36
- MACRS depreciation amount: 895.67
- Total annual depreciation estimate: 895.67

### Asset DEMO-069

- Description: Filing cabinet
- Source files: sample_assets.csv:70
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-08-14
- Cost: 6011.67
- Business use: 90.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 5410.50
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 5410.50
- MACRS depreciation amount: 1082.10
- Total annual depreciation estimate: 1082.10

### Asset DEMO-070

- Description: Power tool set
- Source files: sample_assets.csv:71
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-09-15
- Cost: 6754.68
- Business use: 95.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 6416.95
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 6416.95
- MACRS depreciation amount: 916.98
- Total annual depreciation estimate: 916.98

### Asset DEMO-071

- Description: Diagnostic equipment
- Source files: sample_assets.csv:72
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-10-16
- Cost: 7497.69
- Business use: 100.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 7497.69
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 7497.69
- MACRS depreciation amount: 1499.54
- Total annual depreciation estimate: 1499.54

### Asset DEMO-072

- Description: Delivery equipment
- Source files: sample_assets.csv:73
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-11-17
- Cost: 8240.70
- Business use: 70.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 5768.49
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 5768.49
- MACRS depreciation amount: 1153.70
- Total annual depreciation estimate: 1153.70

### Asset DEMO-073

- Description: Server equipment
- Source files: sample_assets.csv:74
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-12-18
- Cost: 8983.71
- Business use: 75.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 6737.78
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 6737.78
- MACRS depreciation amount: 1347.56
- Total annual depreciation estimate: 1347.56

### Asset DEMO-074

- Description: Telephone system
- Source files: sample_assets.csv:75
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-01-19
- Cost: 9726.72
- Business use: 80.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 7781.38
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 7781.38
- MACRS depreciation amount: 1111.96
- Total annual depreciation estimate: 1111.96

### Asset DEMO-075

- Description: Point-of-sale terminal
- Source files: sample_assets.csv:76
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-02-20
- Cost: 10469.73
- Business use: 85.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 8899.27
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 8899.27
- MACRS depreciation amount: 1779.85
- Total annual depreciation estimate: 1779.85

### Asset DEMO-076

- Description: Workshop machinery
- Source files: sample_assets.csv:77
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-03-21
- Cost: 11212.74
- Business use: 90.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 10091.47
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 10091.47
- MACRS depreciation amount: 2018.29
- Total annual depreciation estimate: 2018.29

### Asset DEMO-077

- Description: Storage shelving
- Source files: sample_assets.csv:78
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-04-22
- Cost: 11955.75
- Business use: 95.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 11357.96
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 11357.96
- MACRS depreciation amount: 2271.59
- Total annual depreciation estimate: 2271.59

### Asset DEMO-078

- Description: Camera equipment
- Source files: sample_assets.csv:79
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-05-23
- Cost: 12698.76
- Business use: 100.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 12698.76
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 12698.76
- MACRS depreciation amount: 1814.65
- Total annual depreciation estimate: 1814.65

### Asset DEMO-079

- Description: Laboratory equipment
- Source files: sample_assets.csv:80
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-06-24
- Cost: 13441.77
- Business use: 70.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 9409.24
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 9409.24
- MACRS depreciation amount: 1881.85
- Total annual depreciation estimate: 1881.85

### Asset DEMO-080

- Description: Warehouse equipment
- Source files: sample_assets.csv:81
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-07-25
- Cost: 14184.78
- Business use: 75.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 10638.59
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 10638.59
- MACRS depreciation amount: 2127.72
- Total annual depreciation estimate: 2127.72

### Asset DEMO-081

- Description: Office equipment
- Source files: sample_assets.csv:82
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-08-26
- Cost: 14927.79
- Business use: 80.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 11942.23
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 11942.23
- MACRS depreciation amount: 2388.45
- Total annual depreciation estimate: 2388.45

### Asset DEMO-082

- Description: Laptop computer
- Source files: sample_assets.csv:83
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-09-27
- Cost: 920.80
- Business use: 85.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 782.68
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 782.68
- MACRS depreciation amount: 111.84
- Total annual depreciation estimate: 111.84

### Asset DEMO-083

- Description: Desktop workstation
- Source files: sample_assets.csv:84
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-10-01
- Cost: 1663.81
- Business use: 90.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 1497.43
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 1497.43
- MACRS depreciation amount: 299.49
- Total annual depreciation estimate: 299.49

### Asset DEMO-084

- Description: Office printer
- Source files: sample_assets.csv:85
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-11-02
- Cost: 2406.82
- Business use: 95.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 2286.48
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 2286.48
- MACRS depreciation amount: 457.30
- Total annual depreciation estimate: 457.30

### Asset DEMO-085

- Description: Network switch
- Source files: sample_assets.csv:86
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-12-03
- Cost: 3149.83
- Business use: 100.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 3149.83
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 3149.83
- MACRS depreciation amount: 629.97
- Total annual depreciation estimate: 629.97

### Asset DEMO-086

- Description: Office desk
- Source files: sample_assets.csv:87
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-01-04
- Cost: 3892.84
- Business use: 70.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 2724.99
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 2724.99
- MACRS depreciation amount: 389.40
- Total annual depreciation estimate: 389.40

### Asset DEMO-087

- Description: Conference table
- Source files: sample_assets.csv:88
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-02-05
- Cost: 4635.85
- Business use: 75.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 3476.89
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 3476.89
- MACRS depreciation amount: 695.38
- Total annual depreciation estimate: 695.38

### Asset DEMO-088

- Description: Task chair
- Source files: sample_assets.csv:89
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-03-06
- Cost: 5378.86
- Business use: 80.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 4303.09
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 4303.09
- MACRS depreciation amount: 860.62
- Total annual depreciation estimate: 860.62

### Asset DEMO-089

- Description: Filing cabinet
- Source files: sample_assets.csv:90
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-04-07
- Cost: 6121.87
- Business use: 85.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 5203.59
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 5203.59
- MACRS depreciation amount: 1040.72
- Total annual depreciation estimate: 1040.72

### Asset DEMO-090

- Description: Power tool set
- Source files: sample_assets.csv:91
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-05-08
- Cost: 6864.88
- Business use: 90.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 6178.39
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 6178.39
- MACRS depreciation amount: 882.89
- Total annual depreciation estimate: 882.89

### Asset DEMO-091

- Description: Diagnostic equipment
- Source files: sample_assets.csv:92
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-06-09
- Cost: 7607.89
- Business use: 95.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 7227.50
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 7227.50
- MACRS depreciation amount: 1445.50
- Total annual depreciation estimate: 1445.50

### Asset DEMO-092

- Description: Delivery equipment
- Source files: sample_assets.csv:93
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-07-10
- Cost: 8350.90
- Business use: 100.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 8350.90
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 8350.90
- MACRS depreciation amount: 1670.18
- Total annual depreciation estimate: 1670.18

### Asset DEMO-093

- Description: Server equipment
- Source files: sample_assets.csv:94
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-08-11
- Cost: 9093.91
- Business use: 70.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 6365.74
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 6365.74
- MACRS depreciation amount: 1273.15
- Total annual depreciation estimate: 1273.15

### Asset DEMO-094

- Description: Telephone system
- Source files: sample_assets.csv:95
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-09-12
- Cost: 9836.92
- Business use: 75.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 7377.69
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 7377.69
- MACRS depreciation amount: 1054.27
- Total annual depreciation estimate: 1054.27

### Asset DEMO-095

- Description: Point-of-sale terminal
- Source files: sample_assets.csv:96
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-10-13
- Cost: 10579.93
- Business use: 80.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 8463.94
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 8463.94
- MACRS depreciation amount: 1692.79
- Total annual depreciation estimate: 1692.79

### Asset DEMO-096

- Description: Workshop machinery
- Source files: sample_assets.csv:97
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-11-14
- Cost: 11322.94
- Business use: 85.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 9624.50
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 9624.50
- MACRS depreciation amount: 1924.90
- Total annual depreciation estimate: 1924.90

### Asset DEMO-097

- Description: Storage shelving
- Source files: sample_assets.csv:98
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-12-15
- Cost: 12065.95
- Business use: 90.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 10859.36
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 10859.36
- MACRS depreciation amount: 2171.87
- Total annual depreciation estimate: 2171.87

### Asset DEMO-098

- Description: Camera equipment
- Source files: sample_assets.csv:99
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-01-16
- Cost: 12808.96
- Business use: 95.00%
- Recovery period: 7.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 12168.51
- Table A-1 MACRS rate for tax year: 14.29%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 12168.51
- MACRS depreciation amount: 1738.88
- Total annual depreciation estimate: 1738.88

### Asset DEMO-099

- Description: Laboratory equipment
- Source files: sample_assets.csv:100
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-02-17
- Cost: 13551.97
- Business use: 100.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 13551.97
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 13551.97
- MACRS depreciation amount: 2710.39
- Total annual depreciation estimate: 2710.39

### Asset DEMO-100

- Description: Warehouse equipment
- Source files: sample_assets.csv:101
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-03-18
- Cost: 14294.98
- Business use: 70.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 10006.49
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 10006.49
- MACRS depreciation amount: 2001.30
- Total annual depreciation estimate: 2001.30

### Asset DEMO-101

- Description: Office equipment
- Source files: sample_assets.csv:102
- Region (informational only): US-FEDERAL-EDUCATIONAL
- Placed-in-service date (informational): 2025-04-19
- Cost: 15037.99
- Business use: 75.00%
- Recovery period: 5.00 years
- Supplied special-depreciation rate: 0.00%
- Business depreciable basis: 11278.49
- Table A-1 MACRS rate for tax year: 20.00%
- Special-depreciation amount: 0.00
- MACRS basis after special depreciation: 11278.49
- MACRS depreciation amount: 2255.70
- Total annual depreciation estimate: 2255.70

## Total

- Sum of displayed annual estimates: 123385.17
