#!/usr/bin/env python3
"""Render aggregate r8 pilot activation summaries from the sanitized CSV."""
import argparse
import csv
import html
import subprocess
from pathlib import Path

COLORS = {"native": "#C6532E", "interp": "#2672A8", "aot": "#23835B"}
LABELS = {"native": "Nativo", "interp": "Interpretado", "aot": "AOT"}
ORDER = ("native", "interp", "aot")


def render(rows, svg_path, png_path=None):
    width, height = 1200, 710
    left, right = 150, 1130
    top, bottom = 175, 555
    y_max = 20.0
    scale = (bottom - top) / y_max
    x_positions = {"native": 330, "interp": 650, "aot": 970}
    by_scenario = {row["scenario"]: row for row in rows}
    esc = lambda value: html.escape(str(value), quote=True)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#182433}.title{font-size:28px;font-weight:700}.sub{font-size:16px;fill:#425466}.panel{font-size:17px;font-weight:700}.tick{font-size:14px;fill:#425466}.axis{stroke:#586777;stroke-width:1.4}.grid{stroke:#dce3ea;stroke-width:1}.note{font-size:15px;fill:#334155}.category{font-size:17px;font-weight:700}.value{font-size:14px;font-weight:700}</style>',
        '<text class="title" x="70" y="48">r8 — tempo até a ativação observada da v2</text>',
        '<text class="sub" x="70" y="78">Piloto fechado em 18/10/2026 | 18/18 slots válidos | n=6 por cenário | todas as ativações em até 60 s</text>',
        '<text class="panel" x="70" y="130">Faixa mínima–máxima, intervalo interquartil (caixa) e mediana (ponto), em segundos</text>',
    ]
    tick = 0
    while tick <= y_max:
        y = bottom - tick * scale
        out += [
            f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}"/>',
            f'<text class="tick" x="{left-18}" y="{y+5:.1f}" text-anchor="end">{tick}</text>',
        ]
        tick += 5
    out += [
        f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{bottom}"/>',
        f'<line class="axis" x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}"/>',
        f'<text class="tick" x="30" y="{(top+bottom)/2:.1f}" transform="rotate(-90 30 {(top+bottom)/2:.1f})" text-anchor="middle">Disparo até primeira resposta v2 correta (s)</text>',
    ]
    for scenario in ORDER:
        row = by_scenario[scenario]
        x = x_positions[scenario]
        color = COLORS[scenario]
        y_min = bottom - float(row["activation_min_s"]) * scale
        y_q1 = bottom - float(row["activation_q1_s"]) * scale
        y_med = bottom - float(row["activation_median_s"]) * scale
        y_q3 = bottom - float(row["activation_q3_s"]) * scale
        y_max_row = bottom - float(row["activation_max_s"]) * scale
        out += [
            f'<line x1="{x}" y1="{y_max_row:.1f}" x2="{x}" y2="{y_min:.1f}" stroke="{color}" stroke-width="3"/>',
            f'<line x1="{x-17}" y1="{y_max_row:.1f}" x2="{x+17}" y2="{y_max_row:.1f}" stroke="{color}" stroke-width="3"/>',
            f'<line x1="{x-17}" y1="{y_min:.1f}" x2="{x+17}" y2="{y_min:.1f}" stroke="{color}" stroke-width="3"/>',
            f'<rect x="{x-38}" y="{y_q3:.1f}" width="76" height="{y_q1-y_q3:.1f}" fill="{color}" fill-opacity="0.22" stroke="{color}" stroke-width="2"/>',
            f'<circle cx="{x}" cy="{y_med:.1f}" r="8" fill="{color}" stroke="#fff" stroke-width="2"><title>{esc(LABELS[scenario])}: mediana {float(row["activation_median_s"]):.3f} s; faixa {float(row["activation_min_s"]):.3f}–{float(row["activation_max_s"]):.3f} s</title></circle>',
            f'<text class="value" x="{x}" y="{y_med-15:.1f}" text-anchor="middle">{float(row["activation_median_s"]):.3f} s</text>',
            f'<text class="category" x="{x}" y="{bottom+35}" text-anchor="middle">{esc(LABELS[scenario])}</text>',
            f'<text class="tick" x="{x}" y="{bottom+57}" text-anchor="middle">6/6 válidas</text>',
        ]
    out += [
        '<text class="note" x="70" y="680">Resumo agregado por cenário; registros individuais e logs brutos permanecem privados. Não combina r5 nem o corte parcial r7.</text>',
        '</svg>',
    ]
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text("\n".join(out) + "\n", encoding="utf-8")
    if png_path:
        png_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["rsvg-convert", "-w", str(width), "-h", str(height), "-o", str(png_path), str(svg_path)], check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--svg", required=True, type=Path)
    parser.add_argument("--png", type=Path)
    args = parser.parse_args()
    with args.csv.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if {row["scenario"] for row in rows} != set(ORDER):
        raise SystemExit("CSV must contain exactly one aggregate row for native, interp, and aot")
    render(rows, args.svg, args.png)


if __name__ == "__main__":
    main()
