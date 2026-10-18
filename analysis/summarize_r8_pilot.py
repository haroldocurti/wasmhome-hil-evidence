#!/usr/bin/env python3
"""Recalculate the public r8 scenario summary from sanitized slot observations."""

import argparse
import csv
import io
import sys
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


SCENARIOS = ("native", "interp", "aot")
LABELS = {"native": "Native", "interp": "Interp", "aot": "AOT"}
FIELDS = (
    "scenario", "scenario_label", "planned_slots", "valid_slots",
    "complete_successful_updates", "v2_within_60s", "activation_min_s",
    "activation_median_s", "activation_q1_s", "activation_q3_s",
    "activation_max_s", "accept_rtt_median_ms", "accept_rtt_min_ms",
    "accept_rtt_max_ms", "control_timeouts", "late_responses",
    "max_control_gap_s", "max_telemetry_gap_s", "stable_post_windows",
    "baseline_restored_slots",
)
REQUIRED = {
    "block_id", "scenario", "order_in_block", "pre_window_passed",
    "update_request_accepted", "accepted_attempt_status", "slot_success",
    "instrument_status", "adjudication", "v2_observed_within_60s",
    "activation_time_s", "accept_rtt_ms", "control_timeout_count",
    "late_response_count", "max_control_gap_s", "max_telemetry_gap_s",
    "post_window_status", "baseline_restored",
}


def boolean(value):
    if value not in ("true", "false"):
        raise ValueError(f"expected true or false, received {value!r}")
    return value == "true"


def number(value):
    return None if value == "" else Decimal(value)


def quantile_inclusive(values, fraction):
    """Linear interpolation at (n - 1) * fraction, as in statistics.quantiles inclusive."""
    ordered = sorted(values)
    if not ordered:
        return None
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    weight = position - lower
    if lower == len(ordered) - 1:
        return ordered[-1]
    return ordered[lower] * (1 - weight) + ordered[lower + 1] * weight


def shown(value):
    if value is None:
        return ""
    return str(value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


def summarize(rows):
    groups = defaultdict(list)
    positions = defaultdict(set)
    seen = set()
    for row in rows:
        scenario = row["scenario"]
        block = row["block_id"]
        order = row["order_in_block"]
        if scenario not in SCENARIOS or order not in ("1", "2", "3"):
            raise ValueError(f"invalid scenario or order in block {block}")
        if (block, scenario) in seen or order in positions[block]:
            raise ValueError(f"duplicate scenario or order in block {block}")
        seen.add((block, scenario))
        positions[block].add(order)
        for field in ("pre_window_passed", "update_request_accepted", "slot_success",
                      "v2_observed_within_60s", "baseline_restored"):
            boolean(row[field])
        groups[scenario].append(row)
    if len(positions) != 6 or any(len(g) != 3 for g in positions.values()):
        raise ValueError("r8 requires six complete paired blocks of three scenarios")

    result = []
    for scenario in SCENARIOS:
        slots = groups[scenario]
        valid = [r for r in slots if r["instrument_status"] == "valid" and r["adjudication"] == "valid"]
        activation = [number(r["activation_time_s"]) for r in valid
                      if r["activation_time_s"] != ""]
        accept_rtt = [number(r["accept_rtt_ms"]) for r in valid
                      if r["accept_rtt_ms"] != ""]
        control_gaps = [number(r["max_control_gap_s"]) for r in slots
                        if r["max_control_gap_s"] != ""]
        telemetry_gaps = [number(r["max_telemetry_gap_s"]) for r in slots
                          if r["max_telemetry_gap_s"] != ""]
        if any(boolean(r["v2_observed_within_60s"]) and number(r["activation_time_s"]) is None for r in slots):
            raise ValueError(f"timely v2 observation without activation time in {scenario}")
        if any(boolean(r["v2_observed_within_60s"]) and number(r["activation_time_s"]) > 60 for r in slots):
            raise ValueError(f"activation exceeds 60 seconds in {scenario}")
        if any(boolean(r["update_request_accepted"]) and not r["accept_rtt_ms"] for r in slots):
            raise ValueError(f"accepted request without RTT in {scenario}")
        result.append({
            "scenario": scenario,
            "scenario_label": LABELS[scenario],
            "planned_slots": len(slots),
            "valid_slots": len(valid),
            "complete_successful_updates": sum(r["accepted_attempt_status"] == "success" for r in valid),
            "v2_within_60s": sum(boolean(r["v2_observed_within_60s"]) for r in valid),
            "activation_min_s": shown(min(activation) if activation else None),
            "activation_median_s": shown(quantile_inclusive(activation, Decimal("0.5"))),
            "activation_q1_s": shown(quantile_inclusive(activation, Decimal("0.25"))),
            "activation_q3_s": shown(quantile_inclusive(activation, Decimal("0.75"))),
            "activation_max_s": shown(max(activation) if activation else None),
            "accept_rtt_median_ms": shown(quantile_inclusive(accept_rtt, Decimal("0.5"))),
            "accept_rtt_min_ms": shown(min(accept_rtt) if accept_rtt else None),
            "accept_rtt_max_ms": shown(max(accept_rtt) if accept_rtt else None),
            "control_timeouts": sum(int(r["control_timeout_count"]) for r in slots),
            "late_responses": sum(int(r["late_response_count"]) for r in slots),
            "max_control_gap_s": shown(max(control_gaps) if control_gaps else None),
            "max_telemetry_gap_s": shown(max(telemetry_gaps) if telemetry_gaps else None),
            "stable_post_windows": sum(r["post_window_status"] == "stable" for r in valid),
            "baseline_restored_slots": sum(boolean(r["baseline_restored"]) for r in slots),
        })
    return result


def render(rows):
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True, help="sanitized slot CSV")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--output", type=Path, help="write scenario summary CSV")
    action.add_argument("--check", type=Path, help="compare with existing summary without writing")
    args = parser.parse_args()
    with args.csv.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED - set(reader.fieldnames or ())
        if missing:
            parser.error("missing columns: " + ", ".join(sorted(missing)))
        rows = list(reader)
    try:
        output = render(summarize(rows))
    except (ValueError, ArithmeticError) as error:
        parser.error(str(error))
    if args.check:
        expected = args.check.read_text(encoding="utf-8-sig")
        if output != expected:
            print(f"summary differs from {args.check}", file=sys.stderr)
            return 1
        print(f"summary matches {args.check}")
    else:
        args.output.write_text(output, encoding="utf-8", newline="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
