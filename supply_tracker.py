#!/usr/bin/env python3
"""Supply tracker for IV ketamine clinic consumables."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Dict

STATE_FILE = Path("inventory_state.json")

DEFAULT_USAGE_PER_PATIENT: Dict[str, float] = {
    "24g_needle": 2.5,
    "10ml_flush": 1.0,
    "tourniquet": 1.0,
    "smallbore_ext_set_clave": 1.0,
    "tegaderm": 1.0,
    "microbore_ext_set_60in": 1.0,
    "30ml_syringe": 1.0,
}


@dataclass
class InventoryState:
    usage_per_patient: Dict[str, float]
    stock: Dict[str, float]
    history: list

    def to_dict(self) -> Dict:
        return {
            "usage_per_patient": self.usage_per_patient,
            "stock": self.stock,
            "history": self.history,
        }


def load_state(path: Path = STATE_FILE) -> InventoryState:
    if not path.exists():
        return InventoryState(
            usage_per_patient=DEFAULT_USAGE_PER_PATIENT.copy(),
            stock={item: 0.0 for item in DEFAULT_USAGE_PER_PATIENT},
            history=[],
        )

    data = json.loads(path.read_text())
    return InventoryState(
        usage_per_patient=data["usage_per_patient"],
        stock=data["stock"],
        history=data.get("history", []),
    )


def save_state(state: InventoryState, path: Path = STATE_FILE) -> None:
    path.write_text(json.dumps(state.to_dict(), indent=2))


def parse_date(value: str) -> str:
    if value.lower() == "today":
        return date.today().isoformat()
    return datetime.strptime(value, "%Y-%m-%d").date().isoformat()


def cmd_init(args: argparse.Namespace) -> None:
    state = load_state(args.file)
    save_state(state, args.file)
    print(f"Initialized tracker state at {args.file}")


def cmd_set_stock(args: argparse.Namespace) -> None:
    state = load_state(args.file)
    if args.item not in state.stock:
        raise ValueError(f"Unknown item: {args.item}")
    state.stock[args.item] = args.count
    save_state(state, args.file)
    print(f"Set {args.item} stock to {args.count}")


def cmd_bulk_set(args: argparse.Namespace) -> None:
    state = load_state(args.file)
    for assignment in args.values:
        if "=" not in assignment:
            raise ValueError(f"Expected item=count, got: {assignment}")
        item, count = assignment.split("=", 1)
        if item not in state.stock:
            raise ValueError(f"Unknown item: {item}")
        state.stock[item] = float(count)
    save_state(state, args.file)
    print("Updated stock counts.")


def cmd_log_day(args: argparse.Namespace) -> None:
    state = load_state(args.file)
    visit_date = parse_date(args.date)
    patients = args.patients

    usage_today: Dict[str, float] = {}
    for item, per_patient in state.usage_per_patient.items():
        used = per_patient * patients
        usage_today[item] = used
        state.stock[item] = round(state.stock[item] - used, 2)

    state.history.append(
        {
            "date": visit_date,
            "patients": patients,
            "usage": usage_today,
        }
    )
    save_state(state, args.file)

    print(f"Logged {patients} IV ketamine patient(s) for {visit_date}.")
    print("Stock after update:")
    for item, count in state.stock.items():
        print(f"  - {item}: {count}")


def average_patients_per_day(history: list) -> float:
    if not history:
        return 0.0
    return sum(entry["patients"] for entry in history) / len(history)


def cmd_report(args: argparse.Namespace) -> None:
    state = load_state(args.file)
    avg_patients = average_patients_per_day(state.history)

    print("Current stock report")
    print("====================")
    print(f"Days logged: {len(state.history)}")
    print(f"Average patients/day: {avg_patients:.2f}")
    print("")

    for item, on_hand in state.stock.items():
        daily_use = state.usage_per_patient[item] * avg_patients
        if daily_use <= 0:
            status = "NO DATA"
            days_left = float("inf")
        else:
            days_left = on_hand / daily_use
            status = "LOW" if days_left < args.low_days else "OK"
        days_left_txt = "n/a" if days_left == float("inf") else f"{days_left:.1f}"
        print(
            f"- {item}: {on_hand} on hand | est. days left: {days_left_txt} | status: {status}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track IV ketamine supply inventory")
    parser.add_argument("--file", type=Path, default=STATE_FILE, help="Path to state JSON")

    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create state file with default items")
    p_init.set_defaults(func=cmd_init)

    p_set = sub.add_parser("set-stock", help="Set one item's stock count")
    p_set.add_argument("item", choices=DEFAULT_USAGE_PER_PATIENT.keys())
    p_set.add_argument("count", type=float)
    p_set.set_defaults(func=cmd_set_stock)

    p_bulk = sub.add_parser("set-stock-bulk", help="Set many counts: item=count item=count")
    p_bulk.add_argument("values", nargs="+", help="Pairs like 24g_needle=100")
    p_bulk.set_defaults(func=cmd_bulk_set)

    p_log = sub.add_parser("log-day", help="Log daily IV ketamine patient volume")
    p_log.add_argument("patients", type=int, help="Number of IV ketamine patients today")
    p_log.add_argument("--date", default="today", help="Date in YYYY-MM-DD or 'today'")
    p_log.set_defaults(func=cmd_log_day)

    p_report = sub.add_parser("report", help="Show current low-stock risk")
    p_report.add_argument(
        "--low-days",
        type=float,
        default=14,
        help="Flag LOW when estimated days of stock is below this value",
    )
    p_report.set_defaults(func=cmd_report)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
