# 96-Well Plate Randomizer and Visualizer

This Python tool generates **randomized 96-well plate maps** for biological samples. It is especially useful for sequencing experiments but can be adapted for any type of sample.

---

## Features

- Randomizes samples across multiple plates while **balancing experimental groups and cages**.
- Automatically fills early plates completely (93 samples + 3 control wells), leaving extra space in the last plate for additional samples.
- Adds **3 control wells per plate**:
  - `H10`: PCR Control
  - `H11`: DNA Extraction Control
  - `H12`: Duplication
- Generates:
  - **CSV visual maps** (Sample/Date + Box/Box Position layers)
  - **PNG images** of the plate maps
  - **Master Excel workbook** with all plates
  - **Master randomized sample sheet** with plate and well info
- Fully reproducible randomization with a fixed seed for testing.

---

## Input CSV Requirements

The input CSV file should contain at least the following columns:

| Column        | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `Sample`      | Unique sample identifier (string)                                           |
| `Date`        | Date of sample collection or any secondary label to appear in wells         |
| `Group`       | Experimental group for balancing across plates                              |
| `Cage`        | Cage or sub-group for additional balancing                                   |
| `Box`         | Storage box identifier                                                       |
| `Box Position`| Position within the storage box                                             |

- Additional columns are allowed and will be preserved in the output CSV.
- Numeric IDs or other values are automatically converted to strings in visual maps.

**Example `example_input.csv`:**

```csv
Sample,Date,Trial,Cage,MouseID,Genotype,Group,Box,Box Position
S1M.01,2/22/25,2,Cage1,1,WT,Saline,AG-Box1,D7
S2M.01,2/22/25,2,Cage1,2,WT,MS+Nalexogel,AG-Box1,D8
S3M.01,2/22/25,2,Cage1,3,WT,MS,AG-Box1,D9
