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
python make_seq_plate_maps_balanced.py <input_csv> plate_config_template.txt
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
You can customize which columns are displayed and how samples are balanced across plates by editing the configuration file:

## Customizing Columns

By default, the script displays **Sample** and **Date** in each well on the visual plate maps.  
You can customize which columns are displayed and how samples are balanced across plates by editing the configuration file:
plate_config_template.txt


### Visual labels in each well
Set which columns appear on the two-line well labels:
```txt
WELL_LINE1=Sample
WELL_LINE2=Date
```
You can replace these with any column names from your CSV (for example `MouseID`, `Genotype`, or `Treatment`).

### Balancing samples across plates
To balance samples across plates by specific metadata (such as treatment group or cage), edit:

```txt
BALANCE_COLUMNS=Group,Cage
```

You may include one or multiple columns separated by commas.

### Secondary plate map information
The secondary visual plate map (showing sample origin such as storage box and position) can also be customized:

```text
BOX_LINE1=Box
BOX_LINE2=Box Position
```

### Important notes
- Column names must **exactly match** the headers in your input CSV file.  
- If a specified column is missing, the corresponding well text will appear blank.  
- All columns from the original CSV are preserved in the **master randomized sample sheet**, including added plate and well assignments.  
- Only the display and balancing behavior changes — your underlying data remain unchanged.

