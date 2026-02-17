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
- Customizable via a simple **configuration file**.

---

## Usage

Run the script from the command line by providing your input CSV and optional config file:

```bash
python make_seq_plate_maps_balanced.py <input_csv> [config_file]
```

- `<input_csv>`: Path to your CSV file containing at least the columns Sample, Date, Group, Cage, Box, Box Position  
- `[config_file]`: Optional config file (plate_config_template.txt) to override default settings

Example:

```python
python make_seq_plate_maps_balanced.py example_input.csv plate_config_template.txt
```


This will generate all outputs for your sample data, ready to inspect or use for sequencing.

---

## Output Files

All outputs are saved in the same folder as the input CSV:

- SeqPlate_X_visual_map_with_box.csv: CSV visual map for each plate (Sample/Date + Box info)
- SeqPlate_X_map.png: PNG visual map of each plate
- SeqPlate_AllPlates.xlsx: Combined Excel workbook with all plates
- SeqPlate_Randomized_Samples.csv: Master randomized sample sheet with plate/well info

---

## Input CSV Requirements

Your CSV must include the following columns:

- Sample: Unique sample identifier (string)
- Date: Date of sample collection or secondary label to appear in wells
- Group: Experimental group for balancing across plates
- Cage: Cage or sub-group for additional balancing
- Box: Storage box identifier
- Box Position: Position within the storage box

Additional columns are allowed and are preserved in the master randomized sample sheet. Numeric IDs or other values are automatically converted to strings in visual maps.

Example `example_input.csv`:

```txt

This will generate all outputs for your sample data, ready to inspect or use for sequencing.

---

## Output Files

All outputs are saved in the same folder as the input CSV:

- SeqPlate_X_visual_map_with_box.csv: CSV visual map for each plate (Sample/Date + Box info)
- SeqPlate_X_map.png: PNG visual map of each plate
- SeqPlate_AllPlates.xlsx: Combined Excel workbook with all plates
- SeqPlate_Randomized_Samples.csv: Master randomized sample sheet with plate/well info

---

## Input CSV Requirements

Your CSV must include the following columns:

- Sample: Unique sample identifier (string)
- Date: Date of sample collection or secondary label to appear in wells
- Group: Experimental group for balancing across plates
- Cage: Cage or sub-group for additional balancing
- Box: Storage box identifier
- Box Position: Position within the storage box

Additional columns are allowed and are preserved in the master randomized sample sheet. Numeric IDs or other values are automatically converted to strings in visual maps.

Example `example_input.csv`:
```txt
Sample,Date,Trial,Cage,MouseID,Genotype,Group,Box,Box Position
S1M.01,2/22/25,2,Cage1,1,WT,Saline,AG-Box1,D7
S2M.01,2/22/25,2,Cage1,2,WT,MS+Nalexogel,AG-Box1,D8
S3M.01,2/22/25,2,Cage1,3,WT,MS,AG-Box1,D9
```
---

## Customizing Columns and Behavior

You can control which columns are used for well labels, balancing, and secondary visual information by editing the configuration file (`plate_config_template.txt`).

```txt
WELL_LINE1=Sample
WELL_LINE2=Date
```

- WELL_LINE1 and WELL_LINE2 define the text shown in each well (two lines).  
- You can replace these with any column from your CSV (e.g., MouseID, Genotype, Treatment).

### Balancing samples across plates
```txt
BALANCE_COLUMNS=Group,Cage
```

- Controls how samples are distributed across plates to balance experimental groups or cages.  
- Multiple columns can be separated by commas.

### Secondary plate map (Box info)
```txt
BOX_LINE1=Box
BOX_LINE2=Box Position
```

- Determines which columns appear in the secondary layer of the visual plate map.

### Notes

- Column names in the config must exactly match your CSV headers, including spaces.  
- If a column is missing, the corresponding well will appear blank.  
- All CSV columns are preserved in the master randomized sample sheet; only display and balancing behavior changes.



