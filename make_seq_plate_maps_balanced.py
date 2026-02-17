import pandas as pd
import random
import math
import matplotlib.pyplot as plt
from collections import defaultdict
import sys

# =============================
# COMMAND LINE INPUTS
# =============================
if len(sys.argv) < 2:
    print("\nUsage:")
    print("python make_seq_plate_maps_balanced.py <input_csv> [config_file]\n")
    sys.exit(1)

INPUT_CSV = sys.argv[1]
CONFIG_FILE = sys.argv[2] if len(sys.argv) >= 3 else None

# =============================
# DEFAULT SETTINGS
# =============================
# these will be overwritten by config if provided
LINE1 = "Sample"
LINE2 = "Date"
BALANCE_COLUMNS = ["Group","Cage"]
BOX_LINE1 = "Box"
BOX_LINE2 = "Box Position"
RANDOM_SEED = 42

# =============================
# LOAD CONFIG IF PROVIDED
# =============================
if CONFIG_FILE:
    print(f"\nUsing config file: {CONFIG_FILE}")
    config = {}
    with open(CONFIG_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")  # remove quotes if any
            config[key] = value

    # overwrite defaults
    LINE1 = config.get("WELL_LINE1", LINE1)
    LINE2 = config.get("WELL_LINE2", LINE2)
    BALANCE_COLUMNS = [c.strip().strip('"').strip("'") for c in config.get("BALANCE_COLUMNS", ",".join(BALANCE_COLUMNS)).split(",")]
    BOX_LINE1 = config.get("BOX_LINE1", BOX_LINE1)
    BOX_LINE2 = config.get("BOX_LINE2", BOX_LINE2)
    RANDOM_SEED = int(config.get("RANDOM_SEED", RANDOM_SEED))

print(f"Balancing by: {BALANCE_COLUMNS}")
print(f"Well label: {LINE1} + {LINE2}\n")
random.seed(RANDOM_SEED)

# =============================
# SETTINGS
# =============================
CONTROL_WELLS = {"H10": "DNA", "H11": "Extract", "H12": "Dup"}
OUTPUT_PREFIX = "SeqPlate"

rows = list("ABCDEFGH")
cols = list(range(1,13))
all_wells = [f"{r}{c}" for r in rows for c in cols]
usable_wells = [w for w in all_wells if w not in CONTROL_WELLS]
SAMPLES_PER_PLATE = len(usable_wells)

# =============================
# READ CSV
# =============================
df = pd.read_csv(INPUT_CSV)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # remove extra unnamed cols

# Check required columns exist
required_cols = [LINE1, LINE2, BOX_LINE1, BOX_LINE2] + BALANCE_COLUMNS
missing = [c for c in required_cols if c not in df.columns]
if missing:
    print(f"Error: The following required columns are missing from CSV: {missing}")
    sys.exit(1)

# =============================
# HELPER: ASSIGN PLATES (full first plates)
# =============================
def assign_plates_full_first(df):
    total_samples = len(df)
    n_total_plates = math.ceil(total_samples / SAMPLES_PER_PLATE)
    plates = [[] for _ in range(n_total_plates)]

    # Shuffle all samples
    all_samples = df.to_dict('records')
    random.shuffle(all_samples)

    # Fill plates
    idx = 0
    for p in range(n_total_plates):
        n_to_assign = SAMPLES_PER_PLATE if p < n_total_plates - 1 else total_samples - SAMPLES_PER_PLATE * (n_total_plates - 1)
        for _ in range(n_to_assign):
            plates[p].append(all_samples[idx])
            idx += 1
    return plates

plates = assign_plates_full_first(df)
print(f"Total plates: {len(plates)}, Samples per plate (usable wells): {SAMPLES_PER_PLATE}\n")

# =============================
# WELL ORDER
# =============================
def get_plate_wells(n):
    return [w for w in all_wells if w not in CONTROL_WELLS][:n]

# =============================
# EXCEL WRITER
# =============================
writer = pd.ExcelWriter(f"{OUTPUT_PREFIX}_AllPlates.xlsx", engine="openpyxl")
assignment_rows = []

# =============================
# GENERATE PLATES
# =============================
for pnum, plate_samples in enumerate(plates, start=1):
    plate_name = f"{OUTPUT_PREFIX}_{pnum}"
    print(f"Creating {plate_name}")
    well_list = get_plate_wells(len(plate_samples))
    plate_map = {w: "" for w in all_wells}

    # Assign samples to wells
    for sample, well in zip(plate_samples, well_list):
        sample["Seq_Plate_Num"] = pnum
        sample["Seq_Plate_Well"] = well
        plate_map[well] = f"{sample[LINE1]}\n{sample[LINE2]}"
        assignment_rows.append(sample.copy())

    # Assign control wells
    for well, label in CONTROL_WELLS.items():
        plate_map[well] = label

    # Build grids: sample labels + Box info
    grid = []
    grid_box = []
    for r in rows:
        rowvals = []
        rowvals_box = []
        for c in cols:
            well = f"{r}{c}"
            rowvals.append(plate_map.get(well, ""))
            assignment = next((s for s in plate_samples if s.get("Seq_Plate_Well") == well), None)
            if assignment:
                rowvals_box.append(f"{assignment[BOX_LINE1]}\n{assignment[BOX_LINE2]}")
            elif well in CONTROL_WELLS:
                rowvals_box.append(CONTROL_WELLS[well])
            else:
                rowvals_box.append("")
        grid.append(rowvals)
        grid_box.append(rowvals_box)

    # Combine grids vertically: Sample layer + blank + Box info layer
    combined_grid = grid + [[""]*12] + grid_box
    combined_df = pd.DataFrame(
        combined_grid,
        index=[f"{r}_Sample" for r in rows] + [""] + [f"{r}_Box" for r in rows],
        columns=cols
    )

    # Save CSV & Excel
    combined_df.to_csv(f"{plate_name}_visual_map_with_box.csv", index=False)
    combined_df.to_excel(writer, sheet_name=plate_name)

    # PNG visual
    fig, ax = plt.subplots(figsize=(12,8))
    ax.axis('off')
    table = ax.table(cellText=grid, rowLabels=rows, colLabels=cols, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1,2)
    plt.title(plate_name, fontsize=16)
    plt.savefig(f"{plate_name}_map.png", bbox_inches='tight')
    plt.close()

# =============================
# MASTER RANDOMIZED SHEET
# =============================
final_df = pd.DataFrame(assignment_rows)
final_df.to_csv(f"{OUTPUT_PREFIX}_Randomized_Samples.csv", index=False)
final_df.to_excel(writer, sheet_name="Randomized_All_Samples", index=False)
writer.close()

print("\nDONE — files created:")
print("• Randomized sample sheet with plate+well")
print("• Visual plate CSVs (96-well layout, with Box info)")
print("• PNG plate maps")
print("• Master Excel workbook\n")
