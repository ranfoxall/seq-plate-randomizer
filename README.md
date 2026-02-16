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

## Usage

Run the script from the command line by providing your input CSV:

```bash
python make_seq_plate_maps_balanced.py <input_csv>
```
<input_csv>: Path to your CSV file containing at least the columns:
Sample, Date, Group, Cage, Box, Box Position

Outputs will be saved in the same folder, including:
  SeqPlate_X_visual_map_with_box.csv (CSV visual map for each plate)
  SeqPlate_X_map.png (PNG visual of each plate)
  SeqPlate_AllPlates.xlsx (combined Excel workbook with all plates)
  SeqPlate_Randomized_Samples.csv (master randomized sample sheet)
  
Example:
python make_seq_plate_maps_balanced.py example_input.csv
This will generate all outputs for your sample data, ready to inspect or use for sequencing.

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
```
## Customizing Columns

By default, the script displays **Sample** and **Date** in each well on the visual plate maps.  
If you want to change which columns appear (for example, using `MouseID` or `Genotype`), you can update the `LINE1` and `LINE2` variables at the top of the script:

```python
LINE1 = "Sample"  # first line in each well
LINE2 = "Date"    # second line in each well
```
Important:
The column names you set must match exactly the headers in your CSV file.
The script relies on these columns to build the visual map; if a column name does not exist in the CSV, the corresponding well will appear empty.
All other columns in your CSV are preserved in the master randomized sample sheet with plate and well assignments, so you can track additional metadata even if it isn’t displayed in the plate maps.
This allows you to customize your visual output while keeping the underlying data intact for sequencing or analysis.
