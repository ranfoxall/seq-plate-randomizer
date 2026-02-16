import pandas as pd
import random
import math
import matplotlib.pyplot as plt
from collections import defaultdict
import sys

# =============================
# SETTINGS
# =============================
if len(sys.argv) < 2:
    print("Usage: python make_seq_plate_maps_balanced.py <input_csv>")
    sys.exit(1)

INPUT_CSV = sys.argv[1]
LINE1 = "Sample"   # top label in well
LINE2 = "Date"     # bottom label in well

random.seed(42)  # reproducible randomization

CONTROL_WELLS = {"H10": "DNA", "H11": "Extract", "H12": "Dup"}
OUTPUT_PREFIX = "SeqPlate"

# Plate structure
rows = list("ABCDEFGH")
cols = list(range(1,13))
all_wells = [f"{r}{c}" for r in rows for c in cols]
usable_wells = [w for w in all_wells if w not in CONTROL_WELLS]
SAMPLES_PER_PLATE = len(usable_wells)

# =============================
# Read CSV
# =============================
df = pd.read_csv(INPUT_CSV)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # remove extra unnamed cols

# =============================
# Helper: assign plates (full first plates)
# =============================
def assign_plates_full_first(df):
    groups = df['Group'].unique()
    group_samples = {g: df[df['Group']==g].to_dict('records') for g in groups}

    total_samples = len(df)
    n_full_plates = total_samples // SAMPLES_PER_PLATE
    n_total_plates = math.ceil(total_samples / SAMPLES_PER_PLATE)
    plates = [[] for _ in range(n_total_plates)]
    cage_counts = [defaultdict(int) for _ in plates]

    # Flatten all samples in random order
    all_samples = []
    for g, samples in group_samples.items():
        random.shuffle(samples)
        all_samples.extend(samples)
    random.shuffle(all_samples)

    # Assign samples to plates 1 to n_full_plates fully
    sample_idx = 0
    for p in range(n_total_plates):
        n_to_assign = SAMPLES_PER_PLATE if p < n_total_plates - 1 else total_samples - SAMPLES_PER_PLATE * (n_total_plates - 1)
        for _ in range(n_to_assign):
            sample = all_samples[sample_idx]
            plates[p].append(sample)
            cage_counts[p][sample['Cage']] += 1
            sample_idx += 1

    return plates

plates = assign_plates_full_first(df)
n_plates = len(plates)
print(f"Total plates: {n_plates}, Samples per plate: {SAMPLES_PER_PLATE}")

# =============================
# Ordered well fill
# =============================
def get_plate_wells_for_samples(n):
    ordered = [f"{r}{c}" for r in rows for c in cols if f"{r}{c}" not in CONTROL_WELLS]
    return ordered[:n]

# =============================
# Excel writer
# =============================
writer = pd.ExcelWriter(f"{OUTPUT_PREFIX}_AllPlates.xlsx", engine="openpyxl")
assignment_rows = []

# =============================
# Generate plates
# =============================
for pnum, plate_samples in enumerate(plates, start=1):
    plate_name = f"{OUTPUT_PREFIX}_{pnum}"
    print(f"Creating {plate_name}")

    well_list = get_plate_wells_for_samples(len(plate_samples))
    plate_map = {w: "" for w in all_wells}

    # Assign samples to wells
    for sample, well in zip(plate_samples, well_list):
        sample["Seq_Plate_Num"] = pnum
        sample["Seq_Plate_Well"] = well
        label = f"{str(sample.get(LINE1,''))}\n{str(sample.get(LINE2,''))}"
        plate_map[well] = label
        assignment_rows.append(sample.copy())

    # Assign control wells
    for well, ctrl_label in CONTROL_WELLS.items():
        plate_map[well] = ctrl_label

    # Build grids: sample labels + Box info
    grid = []
    grid_box = []
    for r in rows:
        rowvals = []
        rowvals_box = []
        for c in cols:
            well = f"{r}{c}"
            rowvals.append(plate_map.get(well,""))
            assignment = next((s for s in plate_samples if s.get("Seq_Plate_Well")==well), None)
            if assignment:
                rowvals_box.append(f"{assignment.get('Box','')}\n{assignment.get('Box Position','')}")
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
    combined_df.to_csv(f"{plate_name}_visual_map_with_box.csv")
    combined_df.to_excel(writer, sheet_name=plate_name)

    # =============================
    # PNG visual (Sample/Date only)
    # =============================
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
# Master randomized sheet
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
