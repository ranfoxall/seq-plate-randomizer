# 96-Well Plate Randomizer and Visualizer

This Python tool generates **randomized 96-well plate maps** for biological samples. It is especially useful for sequencing experiments but can be adapted for any type of sample.

---

## Features

- Randomizes samples across multiple plates while **balancing experimental groups**.
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
- Customizable via a simple **configuration file**.

---

## Usage

Run the script from the command line by providing your input CSV and optional config file:

```bash
python make_seq_plate_maps_balanced.py <input_csv> [config_file]
```

- `<input_csv>`: Path to your input CSV file. By default, the script expects the columns:
  `Sample`, `Date`, `Group`, `Cage`, `Box`, and `Box Position`.

###Configuration file (optional, but recommended)

- `[config_file]`: `plate_config_template.txt` used to override
  default column names, balancing variables, or well label content. If no config file is provided,
  the script will run using the default column settings listed above.

Run with config:
```bash
python make_seq_plate_maps_balanced.py <input_csv> plate_config_template.txt
```
---

### What the config file controls

The config file lets you customize three things:

1. What appears on the visual plate maps (2 per plate)
2. How samples are balanced across plates  
3. Reproducibility of randomization  

This allows the script to work for many different experiments without editing the Python code.

---

## Visual Plate Map Settings (what appears on plates)

These settings control what text appears inside each well and in the secondary box-location map.

### Main well labels (text inside each well)
Choose two columns to display on the primary plate map:

WELL_LINE1=Sample  
WELL_LINE2=Date  

These appear as two lines inside each well.

Choose columns that help identify samples during planning:
- Sample + Date  
- MouseID + Genotype  
- Treatment + Timepoint  

---

### Secondary plate map (sample storage location)

This creates the second visual map showing where samples came from (box layout).

BOX_LINE1=Box  
BOX_LINE2=Box Position  

Examples:
- Box + Box Position  
- Freezer + Rack  
- PlateID + Well  

This is especially useful when pulling samples from storage boxes to organize the randomized plates.

---

## Plate balancing settings

These columns control how samples are distributed across plates to avoid bias.

BALANCE_COLUMNS=Group,Cage  

The script spreads these categories as evenly as possible across plates.

Choose variables that should not cluster together:
- Treatment group  
- Cage  
- Batch  
- Sex  
- Timepoint  

You can include multiple columns:
BALANCE_COLUMNS=`Group`,`Cage`,`Sex`

---

## Reproducibility

RANDOM_SEED=`42`  

Use the same seed to recreate the exact same plate layout later.  
Change the seed if you want a new random layout.

---

## Example full config file

WELL_LINE1=`Sample`  
WELL_LINE2=`Date`  
BOX_LINE1=`Box`  
BOX_LINE2=`Box Position`  
BALANCE_COLUMNS=`Group`,`Cage`  
RANDOM_SEED=`42`  

---

## Important notes

- Column names must match your CSV headers exactly (including spaces).
- Do NOT add brackets or quotes.

Correct:
BALANCE_COLUMNS=`Group`,`Cage`  

Incorrect:
BALANCE_COLUMNS=[Group,Cage]  
BALANCE_COLUMNS="Group,Cage"  

If a column listed in the config file does not exist in the CSV, the script will stop and report the missing column.

## Input CSV Requirements

Your CSV must contain the columns referenced in the configuration file (or default columns if no config is used).
At minimum, the CSV must include:

-Two columns for well labels
  Defined by `WELL_LINE1` and `WELL_LINE2`
  These appear inside each well on the primary plate map.

-Two columns for the secondary box-position visual
  Defined by `BOX_LINE1` and `BOX_LINE2`
  These show where each sample originated (e.g., storage box and position).

-One or more balancing columns
  Defined by `BALANCE_COLUMNS`
  These are used to distribute samples evenly across plates and prevent clustering of experimental groups.
  
All column names must match the configuration file exactly (including spaces).

### Default expected columns (if no config file is provided)

If running without a config file, the script expects:

- `Sample` — primary sample identifier
- `Date` — secondary label displayed in wells
- `Group` — used for balancing across plates
- `Cage` — additional balancing variable
- `Box` — storage box identifier
- `Box Position` — position within storage box
At minimum, the CSV must include:
- Two columns to display inside each well (set by `WELL_LINE1` and `WELL_LINE2`)
- Two columns for the secondary box-position visual (set by `BOX_LINE1` and `BOX_LINE2`)
- One or more columns used for balancing across plates (set by `BALANCE_COLUMNS`)

### Default expected columns (if no config file is provided)

If running without a config file, the script expects:

- `Sample` — primary sample identifier
- `Date` — secondary label displayed in wells
- `Group` — used for balancing across plates
- `Cage` — additional balancing variable
- `Box` — storage box identifier
- `Box Position` — position within storage box

### Additional notes

- Column names must match the CSV headers exactly (including spaces).
- Additional columns are allowed and will be preserved in the master randomized sample sheet.
- Numeric IDs or other values are automatically converted to strings in visual maps.
- If any required column is missing, the script will stop and report which column is missing.

## Output Files

All outputs are saved in the same folder as the input CSV:

- `SeqPlate_X_visual_map_with_box.csv`: CSV visual map for each plate (Sample/Date + Box info)
- `SeqPlate_X_map.png`: PNG visual map of each plate
- `SeqPlate_AllPlates.xlsx`: Combined Excel workbook with all plates
- `SeqPlate_Randomized_Samples.csv`: Master randomized sample sheet with plate/well info

---

Example `example_input.csv`:
```txt
Sample,Date,Trial,Cage,MouseID,Genotype,Group,Box,Box Position
S1M.01,2/22/25,2,Cage1,1,WT,Saline,AG-Box1,D7
S2M.01,2/22/25,2,Cage1,2,WT,MS+Nalexogel,AG-Box1,D8
S3M.01,2/22/25,2,Cage1,3,WT,MS,AG-Box1,D9
```
---


