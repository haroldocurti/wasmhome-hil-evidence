#!/usr/bin/env python3
"""Render paired r8 observations and medians from public sanitized CSVs."""
import argparse
import csv
import html
import subprocess
from decimal import Decimal
from pathlib import Path
from summarize_r8_pilot import summarize

ORDER = ('native', 'interp', 'aot')
LABELS = {'native': 'Nativo / OTA', 'interp': 'WASM interpretado', 'aot': 'WASM AOT'}
COLORS = ('#0072B2', '#D55E00', '#009E73', '#AA4499', '#8A6500', '#394B59')
DASHES = ('', '8 4', '3 3', '10 3 2 3', '6 3', '2 4')


def render(rows, slots, svg_path, png_path=None):
    calculated = summarize(slots)
    if rows != [{key: str(value) for key, value in row.items()} for row in calculated]:
        raise ValueError('Aggregate CSV differs from the individual observations.')
    blocks = sorted({r['block_id'] for r in slots})
    indexed = {(r['block_id'], r['scenario']): r for r in slots}
    if any(r['instrument_status'] != 'valid' or r['adjudication'] != 'valid'
           or not r['activation_time_s'] for r in slots):
        raise ValueError('This r8 figure requires all 18 adjudicated activation observations.')
    if any(not Decimal(r['activation_time_s']).is_finite()
           or not 0 <= Decimal(r['activation_time_s']) <= 20 for r in slots):
        raise ValueError('Activation observation outside the displayed 0–20 s range.')
    width, height = 1280, 870
    left, right, top, bottom = 140, 1180, 215, 650
    xpos = dict(zip(ORDER, (300, 650, 1000)))
    y = lambda value: bottom - float(value) * (bottom - top) / 20
    esc = lambda value: html.escape(str(value), quote=True)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Piloto r8: tempos individuais de ativação da v2, pareados por bloco</title>',
        '<desc id="desc">Seis blocos com três cenários cada. Cada ponto é um slot; as linhas unem o mesmo bloco. As medianas de cada cenário são informadas abaixo do eixo. A ordem no eixo não representa a ordem de execução.</desc>',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:DejaVu Sans,Arial,sans-serif;fill:#182433}.title{font-size:28px;font-weight:700}.sub{font-size:17px;fill:#425466}.tick{font-size:15px;fill:#425466}.label{font-size:18px;font-weight:700}.note{font-size:16px;fill:#334155}</style>',
        '<text class="title" x="60" y="48">Piloto — tempo até a primeira resposta correta da v2</text>',
        '<text class="sub" x="60" y="82">18 slots válidos · seis blocos pareados · seis observações por cenário · rodada r8</text>',
        '<text class="sub" x="60" y="114">Cada ponto representa um slot. Linhas e cores identificam observações do mesmo bloco.</text>',
    ]
    for i, block in enumerate(blocks):
        x = 155 + i * 175
        dash = f' stroke-dasharray="{DASHES[i]}"' if DASHES[i] else ''
        out += [f'<line x1="{x}" y1="155" x2="{x+42}" y2="155" stroke="{COLORS[i]}" stroke-width="2"{dash}/>',
                f'<circle cx="{x+21}" cy="155" r="5" fill="{COLORS[i]}"/>',
                f'<text class="tick" x="{x+50}" y="160">{esc(block)}</text>']
    for tick in range(0, 21, 5):
        out += [f'<line x1="{left}" y1="{y(tick)}" x2="{right}" y2="{y(tick)}" stroke="#dce3ea"/>',
                f'<text class="tick" x="{left-18}" y="{y(tick)+5}" text-anchor="end">{tick}</text>']
    out.append(f'<text class="tick" transform="translate(45 {(top+bottom)/2}) rotate(-90)" text-anchor="middle">Disparo até primeira resposta v2 correta (s)</text>')
    # A small, fixed horizontal offset per block separates nearby observations;
    # it is repeated across categories and does not encode another measurement.
    for i, block in enumerate(blocks):
        offset = (i - 2.5) * 12
        points = [(xpos[s] + offset, y(indexed[block, s]['activation_time_s'])) for s in ORDER]
        dash = f' stroke-dasharray="{DASHES[i]}"' if DASHES[i] else ''
        coords = ' '.join(f'{x:.2f},{v:.2f}' for x, v in points)
        out.append(f'<polyline points="{coords}" fill="none" stroke="{COLORS[i]}" stroke-width="1.8" opacity="0.65"{dash}/>')
    for i, block in enumerate(blocks):
        for scenario in ORDER:
            r = indexed[block, scenario]
            x = xpos[scenario] + (i - 2.5) * 12
            out.append(f'<circle cx="{x}" cy="{y(r["activation_time_s"]):.2f}" r="5.8" fill="{COLORS[i]}" stroke="white" stroke-width="1.3"><title>{esc(block)} · {esc(LABELS[scenario])}: {esc(r["activation_time_s"])} s; posição {esc(r["order_in_block"])} no bloco</title></circle>')
    summaries = {r['scenario']: r for r in rows}
    for scenario in ORDER:
        x = xpos[scenario]
        median = summaries[scenario]['activation_median_s'].replace('.', ',')
        out += [f'<text class="label" x="{x}" y="690" text-anchor="middle">{esc(LABELS[scenario])}</text>',
                f'<text class="sub" x="{x}" y="720" text-anchor="middle">Mediana: {median} s · n = 6</text>']
    out += [
        '<text class="note" x="60" y="770">As linhas indicam pareamento, não evolução temporal; a ordem de execução varia entre blocos.</text>',
        '<text class="note" x="60" y="796">Pontos deslocados levemente na horizontal para legibilidade. Todas as ativações ocorreram em até 60 s.</text>',
        '<text class="note" x="60" y="832">Fonte: 18 slots públicos da r8. Resultado descritivo do piloto; não combina a fase diagnóstica ou a r7.</text>',
        '</svg>',
    ]
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text('\n'.join(out) + '\n', encoding='utf-8')
    if png_path:
        png_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['rsvg-convert', '-o', str(png_path), str(svg_path)], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', required=True, type=Path, help='scenario aggregate CSV')
    parser.add_argument('--slots', required=True, type=Path, help='individual slot CSV')
    parser.add_argument('--svg', required=True, type=Path)
    parser.add_argument('--png', type=Path)
    args = parser.parse_args()
    def read(path):
        with path.open(encoding='utf-8-sig', newline='') as handle:
            return list(csv.DictReader(handle))
    render(read(args.csv), read(args.slots), args.svg, args.png)


if __name__ == '__main__':
    main()
