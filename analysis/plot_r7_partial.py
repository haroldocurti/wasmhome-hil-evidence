#!/usr/bin/env python3
"""Render the partial r7 schema-2 figure from its sanitized CSV."""
import argparse, csv, html, subprocess
from pathlib import Path

COLORS={"native":"#C6532E","interp":"#2672A8","aot":"#23835B"}
LABELS={"native":"Nativo","interp":"Interpretado","aot":"AOT"}
SERIES=[("activation_time_s","Tempo até v2 observada (s)",20,5),("max_control_gap_s","Maior intervalo entre respostas de controle (s)",5.5,1),("max_telemetry_gap_s","Maior intervalo entre mensagens de telemetria (s)",5.5,1)]

def render(rows, svg_path, png_path=None):
    W,H=1200,930; left,right=145,1135; top0=150; panel_h=205; gap=32
    esc=lambda x: html.escape(str(x),quote=True)
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="#fff"/>','<style>text{font-family:Arial,Helvetica,sans-serif;fill:#182433}.title{font-size:27px;font-weight:700}.sub{font-size:16px;fill:#425466}.panel-title{font-size:18px;font-weight:700}.tick{font-size:14px;fill:#425466}.axis{stroke:#586777;stroke-width:1.4}.grid{stroke:#dce3ea;stroke-width:1}.note{font-size:15px;fill:#334155}.legend{font-size:15px}</style>','<text class="title" x="70" y="44">r7 schema 2 - oito slots com resumo completo</text>','<text class="sub" x="70" y="72">Corte: 17/10/2026 | 8 de 18 slots planejados | v2 observada em 8/8 dentro de 60 s</text>']
    x=70
    for sc in ("native","interp","aot"):
        out += [f'<circle cx="{x+8}" cy="108" r="7" fill="{COLORS[sc]}"/>',f'<text class="legend" x="{x+24}" y="113">{LABELS[sc]}</text>']; x+=165
    xb=left+38; xs=(right-left-76)/5; xo={"native":-17,"interp":0,"aot":17}
    for j,(field,title,ymax,step) in enumerate(SERIES):
        y0=top0+j*(panel_h+gap); yt=y0+28; yb=y0+panel_h-28
        out.append(f'<text class="panel-title" x="{left}" y="{y0+5}">{esc(title)}</text>')
        val=0
        while val<=ymax+1e-6:
            y=yb-(val/ymax)*(yb-yt)
            out += [f'<line class="grid" x1="{xb}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}"/>',f'<text class="tick" x="{left+20}" y="{y+5:.1f}" text-anchor="end">{val:g}</text>']; val+=step
        out += [f'<line class="axis" x1="{xb}" y1="{yt}" x2="{xb}" y2="{yb}"/>',f'<line class="axis" x1="{xb}" y1="{yb}" x2="{right}" y2="{yb}"/>']
        for b in range(1,7):
            x=xb+(b-1)*xs
            out += [f'<line class="grid" x1="{x:.1f}" y1="{yt}" x2="{x:.1f}" y2="{yb}"/>',f'<text class="tick" x="{x:.1f}" y="{yb+22}" text-anchor="middle">B{b:02d}</text>']
        for row in rows:
            b=int(row["block_id"][1:]); x=xb+(b-1)*xs+xo[row["scenario"]]; v=float(row[field]); y=yb-(v/ymax)*(yb-yt)
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{COLORS[row["scenario"]]}" stroke="#fff" stroke-width="2"><title>{esc(row["slot_id"])}: {v:.3f} s</title></circle>')
        if j==0: out.append(f'<text class="tick" x="{right}" y="{yt-9}" text-anchor="end">Eixo limitado a 20 s; prazo do protocolo: 60 s</text>')
    out += ['<text class="note" x="70" y="892">Sem ponto = sem resumo final no corte, não falha. Cinco registros também têm erro em desafio UART auxiliar; classificação pendente.</text>','</svg>']
    svg_path.parent.mkdir(parents=True,exist_ok=True); svg_path.write_text("\n".join(out)+"\n",encoding="utf-8")
    if png_path:
        png_path.parent.mkdir(parents=True,exist_ok=True)
        subprocess.run(["rsvg-convert","-w",str(W),"-h",str(H),"-o",str(png_path),str(svg_path)],check=True)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--csv",required=True,type=Path); ap.add_argument("--svg",required=True,type=Path); ap.add_argument("--png",type=Path); a=ap.parse_args()
    with a.csv.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
    render(rows,a.svg,a.png)
if __name__=="__main__": main()
