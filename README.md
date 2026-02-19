# IV Ketamine Supply Tracker

Simple command-line tracker to help you manage consumable supplies for IV ketamine patients.

## Where do I go to use this?

You use this tool in a **Terminal/Command Prompt**, inside the folder that contains `supply_tracker.py`.

### Option A: Mac
1. Open **Terminal**.
2. Go to the project folder:
   ```bash
   cd /workspace/supplylist
   ```
3. Run commands like:
   ```bash
   python3 supply_tracker.py report
   ```

### Option B: Windows
1. Open **PowerShell**.
2. Go to your project folder (example):
   ```powershell
   cd C:\path\to\supplylist
   ```
3. Run commands like:
   ```powershell
   py supply_tracker.py report
   ```

---

## What it tracks per patient

- 24g needles: **2.5**
- 10ml flush: **1**
- Tourniquet: **1**
- 7" (18cm) smallbore ext set w/ clave: **1**
- Tegaderm: **1**
- 60" microbore ext set: **1**
- 30ml syringe: **1**

## How to use it (first time)

### 1) Initialize
```bash
python3 supply_tracker.py init
```

### 2) Enter your current stock counts
```bash
python3 supply_tracker.py set-stock-bulk \
  24g_needle=500 \
  10ml_flush=300 \
  tourniquet=250 \
  smallbore_ext_set_clave=220 \
  tegaderm=260 \
  microbore_ext_set_60in=210 \
  30ml_syringe=290
```

### 3) Log patients each day
```bash
python3 supply_tracker.py log-day 8 --date 2026-02-19
```

### 4) Check low stock
```bash
python3 supply_tracker.py report --low-days 14
```

Anything below 14 estimated days remaining is marked `LOW`.

## Fast daily routine (recommended)

At the end of each day run:

```bash
python3 supply_tracker.py log-day <NUMBER_OF_PATIENTS>
python3 supply_tracker.py report --low-days 14
```

Example:

```bash
python3 supply_tracker.py log-day 6
python3 supply_tracker.py report --low-days 14
```

## Google Sheets connection

Yes — the tool can import patient counts from Google Sheets.

## Exactly what to copy/paste into Google Sheets

In Google Sheets cell **A1**, paste this exactly:

```text
date,patients
2026-02-17,7
2026-02-18,9
2026-02-19,6
```

Then:
1. Highlight column A.
2. Click **Data → Split text to columns**.
3. Your sheet should now have 2 columns with headers: `date` and `patients`.

You can also type directly into two columns like this:

| date       | patients |
|------------|----------|
| 2026-02-17 | 7        |
| 2026-02-18 | 9        |
| 2026-02-19 | 6        |

### Sheet format required
Headers in row 1 must be exactly:

- `date`
- `patients`

### Share setting required
The sheet must be viewable by the tool (for example: **Anyone with the link can view**).

### Import from Google Sheets
```bash
python3 supply_tracker.py import-patients-google "https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit#gid=0"
```

Optional tab id:

```bash
python3 supply_tracker.py import-patients-google "https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit" --gid 123456789
```

Optional replace existing history:

```bash
python3 supply_tracker.py import-patients-google "<SHEET_URL>" --reset-history
```

## Import from local CSV

```bash
python3 supply_tracker.py import-patients-csv patient_log.csv
```

CSV must contain headers: `date,patients`.

## Useful command

See all available commands:

```bash
python3 supply_tracker.py --help
```

## Data file

By default the tracker stores data in `inventory_state.json` in this folder.

Use `--file` to keep separate inventories:

```bash
python3 supply_tracker.py --file clinic_a.json init
```
