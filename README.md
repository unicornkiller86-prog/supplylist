# IV Ketamine Supply Tracker

Simple command-line tracker to help you manage consumable supplies for IV ketamine patients.

## What it tracks per patient

- 24g needles: **2.5**
- 10ml flush: **1**
- Tourniquet: **1**
- 7" (18cm) smallbore ext set w/ clave: **1**
- Tegaderm: **1**
- 60" microbore ext set: **1**
- 30ml syringe: **1**

## Quick start

Initialize your tracker file:

```bash
python3 supply_tracker.py init
```

Set your current inventory counts (example):

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

Log daily patient count:

```bash
python3 supply_tracker.py log-day 8 --date 2026-02-19
```

Generate low-stock report:

```bash
python3 supply_tracker.py report --low-days 14
```

## Suggested daily workflow

1. At end of each day, run `log-day` with number of IV ketamine patients.
2. Run `report` to see estimated days left for each item.
3. Reorder anything marked `LOW`.
4. When a shipment arrives, update counts with `set-stock` or `set-stock-bulk`.

## Data file

By default the tracker stores data in `inventory_state.json` in this folder.

Use `--file` to keep separate inventories:

```bash
python3 supply_tracker.py --file clinic_a.json init
```
