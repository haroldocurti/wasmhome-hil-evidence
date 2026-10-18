#!/usr/bin/env python3
"""Gera a figura diagnóstica r5 a partir do CSV público sanitizado."""

import csv
import statistics
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/r5-diagnostica-perfis-legados.csv'
SVG = ROOT / 'analysis/figures/r5-diagnostica.svg'
PNG = ROOT / 'analysis/figures/r5-diagnostica.png'
SCENARIOS = [('native', 'Nativo / OTA', '#ba5550'), ('interp', 'WASM interpretado', '#16826a'), ('aot', 'WASM AOT', '#356aa4')]


def main():
    with SOURCE.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 18 or any(sum(r['scenario'] == s for r in rows) != 6 for s, _, _ in SCENARIOS):
        raise ValueError('A figura requer seis observações por cenário.')
    by_key = {(r['block'], r['scenario']): r for r in rows}
    blocks = sorted({r['block'] for r in rows})
    if len(by_key) != 18 or len(blocks) != 6:
        raise ValueError('Blocos ou cenários duplicados ou ausentes.')
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="940" viewBox="0 0 1280 940" role="img" aria-labelledby="title desc">',
             '<title id="title">Fase diagnóstica r5: ativação funcional da v2</title>',
             '<desc id="desc">Dezoito observações em seis blocos. Nativo: zero de seis ativações em 60 segundos; interpretado e AOT: seis de seis.</desc>',
             '<rect width="1280" height="940" fill="white"/>',
             '<text x="55" y="58" font-family="DejaVu Sans,Arial,sans-serif" font-size="30" font-weight="bold" fill="#17324d">Fase diagnóstica r5 — ativação funcional da v2</text>',
             '<text x="55" y="91" font-family="DejaVu Sans,Arial,sans-serif" font-size="17" fill="#435466">18 slots · seis blocos · perfis legados · resultado diagnóstico</text>',
             '<text x="55" y="139" font-family="DejaVu Sans,Arial,sans-serif" font-size="21" font-weight="bold" fill="#17324d">Desfecho por bloco</text>']
    centers = [270, 640, 1010]
    for (scenario, label, color), cx in zip(SCENARIOS, centers):
        parts.append(f'<text x="{cx}" y="177" text-anchor="middle" font-family="DejaVu Sans,Arial,sans-serif" font-size="17" font-weight="bold" fill="#17324d">{escape(label)}</text>')
        for i, block in enumerate(blocks):
            row = by_key[(block, scenario)]
            observed = row['v2_observed_within_60s'] == '1'
            y = 194 + 56*i
            fill = '#e3f4ee' if observed else '#fae8e6'
            stroke = color
            mark = f'{float(row["activation_time_s"]):.3f} s' if observed else 'sem v2 ≤ 60 s'
            parts.append(f'<rect x="{cx-155}" y="{y}" width="310" height="45" rx="8" fill="{fill}" stroke="{stroke}"/>')
            parts.append(f'<text x="{cx}" y="{y+29}" text-anchor="middle" font-family="DejaVu Sans,Arial,sans-serif" font-size="16" fill="#17324d">B{i+1} · {mark}</text>')
    parts.extend(['<text x="55" y="584" font-family="DejaVu Sans,Arial,sans-serif" font-size="21" font-weight="bold" fill="#17324d">Tempo até a primeira v2 correta entre ativações observadas</text>',
                  '<text x="55" y="612" font-family="DejaVu Sans,Arial,sans-serif" font-size="15" fill="#435466">O cenário nativo não tem tempo medido: seis pedidos aceitos, nenhuma ativação no prazo.</text>'])
    x0, width = 280, 860
    for tick in range(0, 11, 2):
        x = x0 + width*tick/10
        parts.append(f'<line x1="{x}" y1="655" x2="{x}" y2="822" stroke="#dce4ea"/>')
        parts.append(f'<text x="{x}" y="849" text-anchor="middle" font-family="DejaVu Sans,Arial,sans-serif" font-size="14" fill="#435466">{tick}</text>')
    parts.append('<text x="710" y="879" text-anchor="middle" font-family="DejaVu Sans,Arial,sans-serif" font-size="15" fill="#435466">Segundos</text>')
    for scenario, label, color in SCENARIOS[1:]:
        y = 690 if scenario == 'interp' else 775
        values = sorted(float(r['activation_time_s']) for r in rows if r['scenario'] == scenario and r['v2_observed_within_60s'] == '1')
        median = statistics.median(values)
        parts.append(f'<text x="55" y="{y+5}" font-family="DejaVu Sans,Arial,sans-serif" font-size="16" fill="#17324d">{escape(label)}</text>')
        parts.append(f'<line x1="{x0+width*min(values)/10}" y1="{y}" x2="{x0+width*max(values)/10}" y2="{y}" stroke="{color}" stroke-width="3"/>')
        for j, value in enumerate(values):
            x = x0 + width*value/10
            offset = [-13, 13, -7, 7, -17, 17][j]
            parts.append(f'<circle cx="{x}" cy="{y+offset}" r="6" fill="{color}"/>')
        parts.append(f'<text x="1225" y="{y+5}" text-anchor="end" font-family="DejaVu Sans,Arial,sans-serif" font-size="15" fill="{color}">mediana {median:.3f} s</text>')
    parts.append('<text x="55" y="920" font-family="DejaVu Sans,Arial,sans-serif" font-size="14" fill="#435466">Fonte: CSV público r5. Adjudicação final pendente; perfis legados não qualificam o nativo schema 2.</text>')
    parts.append('</svg>')
    SVG.write_text('\n'.join(parts) + '\n', encoding='utf-8')
    with PNG.open('wb') as output:
        subprocess.run(['rsvg-convert', '--format', 'png', str(SVG)], stdout=output, check=True)


if __name__ == '__main__':
    main()
