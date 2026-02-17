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

## Configuration file (optional, but recommended)

- `[config_file]`: `plate_config_template.txt` used to override
  default column names, balancing variables, or well label content. If no config file is provided,
  the script will run using the default column settings listed above.

Run with config:
```bash
python make_seq_plate_maps_balanced.py <input_csv> plate_config_template.txt
```
---

## What the config file controls

The config file lets you customize three things:

1. What appears on the visual plate maps (2 per plate)
2. How samples are balanced across plates  
3. Reproducibility of randomization  

This allows the script to work for many different experiments without editing the Python code.

---

## Visual Plate Map Settings (what appears on plates)

These settings control what text appears inside each well and in the secondary box-location map.

## Main well labels (text inside each well)
Choose two columns to display on the primary plate map:

WELL_LINE1=`Sample`  
WELL_LINE2=`Date`  

These appear as two lines inside each well.

Choose columns that help identify samples during planning:
- `Sample` + `Date`  
- `MouseID` + `Genotype`  
- `Treatment` + `Timepoint`  

---

## Secondary plate map (sample storage location)

This creates the second visual map showing where samples came from (box layout).

BOX_LINE1=`Box`  
BOX_LINE2=`Box Position`  

Examples:
- `Box` + `Box Position`  
- `Freezer` + `Rack`  
- `PlateID` + `Well`  

This is especially useful when pulling samples from storage boxes to organize the randomized plates.

---

## Plate balancing settings

These columns control how samples are distributed across plates to avoid bias.

BALANCE_COLUMNS=`Group`,`Cage`  

The script spreads these categories as evenly as possible across plates.

Choose variables that should not cluster together:
- `Treatment group`  
- `Cage`  
- `Batch`  
- `Sex`  
- `Timepoint`  

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

## Default expected columns (if no config file is provided)

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

Additional notes:
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
## Example Primary Plate Map (Sample + Date)

This map shows the main well labels for each sample (two lines per well: Sample ID and Date).

```markdown
        1            2            3            4            5            6            7            8            9            10           11           12
A   S1M.01|2/22/25  S2M.01|2/22/25  S3M.01|2/22/25  S4M.01|2/22/25  S5M.01|2/22/25  S6M.01|2/22/25  S7M.01|2/22/25  S8M.01|2/22/25  S9M.01|2/22/25  S10M.01|2/22/25  S11M.01|2/22/25  S12M.01|2/22/25
B   S13M.01|2/22/25  S14M.01|2/22/25  S15M.01|2/22/25  S16M.01|2/22/25  S17M.01|2/22/25  S18M.01|2/22/25  S19M.01|2/22/25  S20M.01|2/22/25  S21M.01|2/22/25  S22M.01|2/22/25  S23M.01|2/22/25  S24M.01|2/22/25
D   S25M.01|2/22/25  S26M.01|2/22/25  S27M.01|2/22/25  S28M.01|2/22/25  S29M.01|2/22/25  S30M.01|2/22/25  S31M.01|2/22/25  S32M.01|2/22/25  S33M.01|2/22/25  S34M.01|2/22/25  S35M.01|2/22/25  S36M.01|2/22/25
E   S37M.01|2/22/25  S38M.01|2/22/25  S39M.01|2/22/25  S40M.01|2/22/25  S41M.01|2/22/25  S42M.01|2/22/25  S43M.01|2/22/25  S44M.01|2/22/25  S45M.01|2/22/25  S46M.01|2/22/25  S47M.01|2/22/25  S48M.01|2/22/25
F   S49M.01|2/22/25  S50M.01|2/22/25  S51M.01|2/22/25  S52M.01|2/22/25  S53M.01|2/22/25  S54M.01|2/22/25  S55M.01|2/22/25  S56M.01|2/22/25  S57M.01|2/22/25  S58M.01|2/22/25  S59M.01|2/22/25  S60M.01|2/22/25
G   S61M.01|2/22/25  S62M.01|2/22/25  S63M.01|2/22/25  S64M.01|2/22/25  S65M.01|2/22/25  S66M.01|2/22/25  S67M.01|2/22/25  S68M.01|2/22/25  S69M.01|2/22/25  S70M.01|2/22/25  S71M.01|2/22/25  S72M.01|2/22/25
H   S73M.01|2/22/25  S74M.01|2/22/25  S75M.01|2/22/25  S76M.01|2/22/25  S77M.01|2/22/25  S78M.01|2/22/25  S79M.01|2/22/25  S80M.01|2/22/25  S81M.01|2/22/25  PCR      EXT      DUP
```
Format inside each well:
- Line 1 = `Sample ID`  
- Line 2 = `Date`  
- Control wells:
  - H10 = PCR Control  
  - H11 = Extraction Control  
  - H12 = Duplicate  



## Example Secondary Plate Map (Box + Position)

This map shows where each sample originated from in storage (box layout).

```markdown
        1            2            3            4            5            6            7            8            9            10           11           12
A   Box1|A1     Box1|A2     Box1|A3     Box1|A4     Box1|A5     Box1|A6     Box1|A7     Box1|A8     Box1|A9     Box1|A10    Box1|A11    Box1|A12
B   Box1|B1     Box1|B2     Box1|B3     Box1|B4     Box1|B5     Box1|B6     Box1|B7     Box1|B8     Box1|B9     Box1|B10    Box1|B11    Box1|B12
C   Box2|C1     Box2|C2     Box2|C3     Box2|C4     Box2|C5     Box2|C6     Box2|C7     Box2|C8     Box2|C9     Box2|C10    Box2|C11    Box2|C12
D   Box2|D1     Box2|D2     Box2|D3     Box2|D4     Box2|D5     Box2|D6     Box2|D7     Box2|D8     Box2|D9     Box2|D10    Box2|D11    Box2|D12
E   Box3|E1     Box3|E2     Box3|E3     Box3|E4     Box3|E5     Box3|E6     Box3|E7     Box3|E8     Box3|E9     Box3|E10    Box3|E11    Box3|E12
F   Box3|F1     Box3|F2     Box3|F3     Box3|F4     Box3|F5     Box3|F6     Box3|F7     Box3|F8     Box3|F9     Box3|F10    Box3|F11    Box3|F12
G   Box4|G1     Box4|G2     Box4|G3     Box4|G4     Box4|G5     Box4|G6     Box4|G7     Box4|G8     Box4|G9     Box4|G10    Box4|G11    Box4|G12
H   Box4|H1     Box4|H2     Box4|H3     Box4|H4     Box4|H5     Box4|H6     Box4|H7     Box4|H8     Box4|H9     PCR         EXT         DUP
```
Format inside each well:

Line 1 = `Box`  
Line 2 = `Box Position`  

Control wells:
- H10 = PCR Control  
- H11 = Extraction Control  
- H12 = Duplicate  
