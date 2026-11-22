"""Figuras do minicurso 'Estatística para Ciência de Dados com Python' (EMASC 2026).
Todas as figuras usam a base fictícia de 12 alunos (Sexo, Idade, Altura), definida abaixo.
Gera também alunos.csv. Uso: python make_figs.py  ->  figuras/*.png + alunos.csv
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
from scipy import stats

C = dict(night='#0E103E', indigo='#2C2084', sky='#0391BF', cyan='#34E0C8', teal='#008C96',
         orange='#FFB014', amber='#E27800', mist='#F3F4FB', gray='#262848', soft='#737696',
         red='#D6336C', line='#D0D3E8')
plt.rcParams.update({'font.size': 13, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.edgecolor': C['soft'], 'text.color': C['gray'], 'axes.labelcolor': C['gray'],
                     'xtick.color': C['soft'], 'ytick.color': C['soft'], 'axes.titleweight': 'bold',
                     'axes.titlecolor': C['indigo']})
os.makedirs('figuras', exist_ok=True)
rng = np.random.default_rng(42)


def br(v, d=2):
    """Número com vírgula decimal."""
    return f'{v:.{d}f}'.replace('.', ',').replace('-', '−')


def save(name):
    for a in plt.gcf().axes:
        for ax_ in (a.xaxis, a.yaxis):
            if isinstance(ax_.get_major_formatter(), matplotlib.ticker.ScalarFormatter):
                ax_.set_major_formatter(matplotlib.ticker.FuncFormatter(
                    lambda v, p: f'{v:g}'.replace('.', ',').replace('-', '−')))
    plt.savefig(f'figuras/{name}.png', dpi=200, bbox_inches='tight')
    plt.close()


def stack(v):
    seen, out = {}, []
    for t in v:
        seen[t] = seen.get(t, 0) + 1
        out.append(seen[t])
    return out


def clean_y(ax):
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)



# ------------------------------------------------------------------ base fictícia (12 alunos)
ALUNOS = [('Ana', 'F', 12, 150), ('Bruno', 'M', 12, 153), ('Carla', 'F', 13, 156), ('Diego', 'M', 13, 158),
          ('Elisa', 'F', 14, 160), ('Fabíola', 'F', 14, 165), ('Gabi', 'F', 15, 162), ('Hugo', 'M', 15, 171),
          ('Íris', 'F', 16, 165), ('João', 'M', 16, 176), ('Karen', 'F', 17, 163), ('Lucas', 'M', 17, 201)]
with open('alunos.csv', 'w', encoding='utf-8') as f:
    f.write('Aluno,Sexo,Idade,Altura\n')
    f.writelines(f'{a},{s_},{i_},{h_}\n' for a, s_, i_, h_ in ALUNOS)

sexo = np.array([a[1] for a in ALUNOS]); idade = np.array([a[2] for a in ALUNOS]); alt = np.array([a[3] for a in ALUNOS])
x = np.sort(alt)
n = len(x)
m = x.mean()                                  # 165
s = x.std(ddof=1)                             # 13,45
med = np.median(x)                            # 162,5
q1, q3 = np.median(x[:n // 2]), np.median(x[n // 2:])   # 157 e 168
lo, hi = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)     # 140,5 e 184,5
XL = 'altura (cm)'
x11 = x[:-1]                                  # sem o 201


def levels(v, w=2.0):
    """Nível de empilhamento: valores mais próximos que w ficam em níveis diferentes."""
    lv, out = [], []
    for t in v:
        k = 0
        while any(abs(t - u) < w for u, kk in lv if kk == k):
            k += 1
        lv.append((t, k)); out.append(k)
    return np.array(out)


# ---------- gangorra: cada aluno é um bloco sobre a prancha; o apoio é a média (ou a mediana)
def seesaw(v, name, pivot, label, tilt=False, ghost=None, note=None):
    v = np.sort(np.asarray(v, float))
    fig, ax = plt.subplots(figsize=(8, 3.3))
    ax.set_aspect('equal')
    left, right = (pivot - v[v < pivot]).sum(), (v[v > pivot] - pivot).sum()
    th = np.radians(np.sign(left - right) * 6) if tilt else 0.0
    R = lambda px, py: (pivot + (px - pivot) * np.cos(th) - py * np.sin(th),
                        (px - pivot) * np.sin(th) + py * np.cos(th))
    poly = lambda pts, **kw: ax.add_patch(plt.Polygon([R(*p) for p in pts], closed=True, **kw))
    poly([(144, -1.3), (208, -1.3), (208, 0), (144, 0)], fc=C['soft'], ec=C['gray'], lw=1.2, zorder=2)
    bw, bh = 1.35, 3.3
    lv = levels(v, 2 * bw)
    for t, k in zip(v, lv):
        col = C['red'] if t == 201 else C['indigo']
        y0 = k * (bh + .15)
        poly([(t - bw, y0), (t + bw, y0), (t + bw, y0 + bh), (t - bw, y0 + bh)], fc=col, ec='white', lw=1, zorder=3)
        tx, ty = R(t, y0 + bh / 2)
        ax.text(tx, ty, f'{t:g}', ha='center', va='center', color='white', fontweight='bold', fontsize=8.5,
                rotation=np.degrees(th), rotation_mode='anchor', zorder=5)
    if ghost is not None:
        poly([(ghost - bw, 0), (ghost + bw, 0), (ghost + bw, bh), (ghost - bw, bh)],
             fc='white', ec=C['soft'], lw=1.5, ls='--', zorder=3)
        tx, ty = R(ghost, bh / 2)
        ax.text(tx, ty, f'{ghost:g}', ha='center', va='center', color=C['soft'], fontweight='bold', fontsize=8.5,
                rotation=np.degrees(th), rotation_mode='anchor', zorder=5)
        gx, gy = R(ghost, bh + 1.6)
        ax.text(gx, gy, 'retirado', ha='center', color=C['soft'], fontsize=11)
    ax.add_patch(plt.Polygon([(pivot, -1.3), (pivot - 3.2, -8), (pivot + 3.2, -8)], fc=C['orange'],
                             ec=C['amber'], lw=1.5, zorder=4))
    ax.plot([142, 210], [-8, -8], color=C['soft'], lw=2, zorder=1)
    for t in range(150, 205, 10):
        ax.plot([t, t], [-8, -8.8], color=C['soft'], lw=1)
        ax.text(t, -11, str(t), ha='center', fontsize=10, color=C['soft'])
    txt = br(pivot, 2) if label == 'média' else br(pivot, 1)
    if label == 'média' and pivot == int(pivot):
        txt = br(pivot, 0)
    ax.text(pivot, -14.2, f'apoio na {label} = {txt}', ha='center', color=C['amber'], fontweight='bold')
    if note:
        ax.text(208, 14.5, note, ha='right', va='top', color=C['gray'], fontsize=11.5, fontweight='bold')
    ax.set_xlim(142, 210); ax.set_ylim(-15.5, 15); ax.axis('off')
    save(name)


def pulls(name, v, pivot):
    v = np.asarray(v, float)
    L, Rr = (pivot - v[v < pivot]).sum(), (v[v > pivot] - pivot).sum()
    fig, ax = plt.subplots(figsize=(8, 1.2))
    ax.barh([0], [-L], color=C['sky'], height=.6); ax.barh([0], [Rr], color=C['orange'], height=.6)
    ax.axvline(0, color=C['gray'], lw=2)
    ax.text(-L / 2, 0, f'esquerda: {br(L, 0)} cm', ha='center', va='center', color='white', fontweight='bold')
    ax.text(Rr / 2, 0, f'direita: {br(Rr, 0)} cm', ha='center', va='center', color=C['night'], fontweight='bold')
    ax.set_xlim(-max(L, Rr) * 1.05, max(L, Rr) * 1.05); ax.axis('off'); save(name)


seesaw(x, 'gangorra_a', m, 'média', tilt=False, note='equilibra: puxões iguais')
seesaw(x, 'gangorra_med', med, 'mediana', tilt=True, note='o 201 pesa mais: a prancha cai à direita')
seesaw(x11, 'gangorra_b', x11.mean(), 'média', tilt=False, ghost=201, note='sem o 201: média ≈ mediana')
pulls('puxoes_a', x, m)


# ---------- fileira de "cartas"
def tiles(ax, vals, colors, idx=True):
    for i, (v, c) in enumerate(zip(vals, colors), start=1):
        ax.add_patch(FancyBboxPatch((i - .43, 0), .86, .9, boxstyle='round,pad=0,rounding_size=.12',
                                    fc=c, ec=C['indigo'], lw=1.6))
        ax.text(i, .45, f'{v}', ha='center', va='center', fontweight='bold', fontsize=12.5,
                color='white' if c in (C['indigo'], C['sky'], C['teal']) else C['night'])
        if idx:
            ax.text(i, -.35, str(i), ha='center', va='center', color=C['soft'], fontsize=11)
    ax.set_xlim(.2, len(vals) + .8); ax.axis('off')


# mediana (n par: dois valores centrais)
fig, ax = plt.subplots(figsize=(8, 2.8))
tiles(ax, list(x), [C['mist']] * 5 + [C['orange']] * 2 + [C['mist']] * 5)
ax.set_ylim(-1.0, 2.1)
ax.annotate('', (5.45, 1.35), (.6, 1.35), arrowprops=dict(arrowstyle='<->', color=C['sky'], lw=2))
ax.text(3, 1.55, '5 valores antes', ha='center', color=C['sky'], fontweight='bold', fontsize=12)
ax.annotate('', (12.4, 1.35), (7.55, 1.35), arrowprops=dict(arrowstyle='<->', color=C['sky'], lw=2))
ax.text(10, 1.55, '5 valores depois', ha='center', color=C['sky'], fontweight='bold', fontsize=12)
ax.text(6.5, 1.55, 'centro', ha='center', color=C['amber'], fontweight='bold', fontsize=12)
ax.text(6.5, -.9, 'n = 12 é par: posições 12/2 = 6 e 6 + 1 = 7', ha='center', color=C['amber'], fontweight='bold', fontsize=12)
save('mediana')

# moda: Sexo (categórica) e Altura (numérica)
fig, ax = plt.subplots(1, 2, figsize=(8, 2.9), gridspec_kw=dict(width_ratios=[1, 2.4]))
cs = [(sexo == 'F').sum(), (sexo == 'M').sum()]
ax[0].bar(['F', 'M'], cs, color=[C['orange'], C['line']], edgecolor=C['indigo'], lw=1.5, width=.6)
for i_, c in enumerate(cs):
    ax[0].text(i_, c + .15, f'{c}×', ha='center', fontweight='bold', color=C['indigo'])
ax[0].set_ylim(0, 9.2); ax[0].set_yticks([]); ax[0].spines['left'].set_visible(False)
ax[0].set_title('Sexo: moda = F', fontsize=12.5)
vals, cnt = np.unique(x, return_counts=True)
ax[1].bar(range(len(vals)), cnt, color=[C['orange'] if c == cnt.max() else C['line'] for c in cnt],
          edgecolor=C['indigo'], lw=1.2, width=.7)
for i_, c in enumerate(cnt):
    ax[1].text(i_, c + .05, f'{c}×', ha='center', fontweight='bold', color=C['indigo'], fontsize=10.5)
ax[1].set_xticks(range(len(vals))); ax[1].set_xticklabels([str(v) for v in vals], fontsize=9.5)
ax[1].set_ylim(0, 3); ax[1].set_yticks([]); ax[1].spines['left'].set_visible(False)
ax[1].set_title('Altura: moda = 165 cm', fontsize=12.5)
plt.tight_layout(); save('moda')

# amplitude
fig, ax = plt.subplots(figsize=(8, 2.4))
ys = levels(x, 2.2) + 1
ax.scatter(x, ys, s=170, color=C['indigo'], zorder=3)
ax.scatter([150, 201], [ys[0], ys[-1]], s=170, color=C['orange'], zorder=4)
ax.annotate('', (201, -.1), (150, -.1), arrowprops=dict(arrowstyle='<->', color=C['amber'], lw=2.5))
ax.text(175.5, -.75, 'amplitude = 201 − 150 = 51 cm', ha='center', color=C['amber'], fontweight='bold')
ax.text(150, ys[0] + .7, 'mínimo', ha='center', color=C['amber'], fontweight='bold')
ax.text(201, ys[-1] + .7, 'máximo', ha='center', color=C['amber'], fontweight='bold')
ax.set_xlim(144, 207); ax.set_ylim(-1.3, 4.4); clean_y(ax); ax.set_xlabel(XL)
save('amplitude')


# quartis (n par: duas metades, sem exclusão)
def quartil_tiles(stage, name):
    fig, ax = plt.subplots(figsize=(8, 2.9))
    tiles(ax, list(x), ['#CFEFF7'] * 6 + ['#D5F5EF'] * 6)
    ax.set_ylim(-1.0, 2.5 if stage == 2 else 2.2)
    ax.plot([6.5, 6.5], [-.1, 1.05], color=C['amber'], lw=3, ls='--')
    if stage == 1:
        ax.text(3.5, 1.35, 'metade inferior (6 valores)', ha='center', color=C['sky'], fontweight='bold', fontsize=12)
        ax.text(9.5, 1.35, 'metade superior (6 valores)', ha='center', color=C['teal'], fontweight='bold', fontsize=12)
        ax.text(6.5, -.85, 'n é par: a mediana (162,5) separa as duas metades', ha='center', color=C['soft'], fontsize=11)
    else:
        for xq, lab, col in [(3.5, 'Q₁ = (156 + 158)/2 = 157', C['sky']), (9.5, 'Q₃ = (165 + 171)/2 = 168', C['teal'])]:
            ax.plot([xq, xq], [-.1, 1.05], color=col, lw=3, ls='--')
            ax.text(xq, 1.3, lab, ha='center', color=col, fontweight='bold', fontsize=12)
        ax.annotate('', (9.5, 1.95), (3.5, 1.95), arrowprops=dict(arrowstyle='<->', color=C['amber'], lw=2.5))
        ax.text(6.5, 2.12, 'IQR = 168 − 157 = 11', ha='center', color=C['amber'], fontweight='bold', fontsize=12.5)
    save(name)


quartil_tiles(1, 'quartis1'); quartil_tiles(2, 'quartis2')

# ---------- desvios e quadrados
d = x - m
idx = np.arange(1, n + 1)
fig, ax = plt.subplots(figsize=(8, 3.1))
ax.axhline(m, color=C['orange'], lw=3)
ax.text(n + .45, m, f'x̄ = {br(m, 0)}', color=C['amber'], va='center', fontweight='bold')
for i_, v_, d_ in zip(idx, x, d):
    ax.plot([i_, i_], [m, v_], color=C['sky'] if d_ > 0 else C['teal'], lw=4, solid_capstyle='round')
    if d_ != 0:
        ax.text(i_, v_ + (3 if d_ > 0 else -8), ('+' if d_ > 0 else '') + br(d_, 0), ha='center', fontsize=10.5,
                color=C['sky'] if d_ > 0 else C['teal'], fontweight='bold')
ax.scatter(idx, x, s=130, color=C['indigo'], zorder=3)
ax.set_xlim(.3, n + 1.9); ax.set_ylim(138, 212); ax.set_xticks(idx); ax.set_xlabel('aluno (em ordem crescente de altura)')
ax.set_ylabel('altura (cm)'); ax.set_title('Desvios xᵢ − x̄: sobras e faltas somam 0', fontsize=13)
save('desvios')

fig, ax = plt.subplots(figsize=(8, 3.1))
sq = d ** 2
ax.bar(idx, sq, color=[C['red'] if v_ > 500 else C['orange'] for v_ in sq], width=.65)
for i_, v_ in zip(idx, sq):
    ax.text(i_, v_ + 30, br(v_, 0), ha='center', fontsize=10.5, fontweight='bold', color=C['indigo'])
ax.set_xticks(idx); ax.set_xlabel('aluno (em ordem crescente de altura)'); ax.set_ylabel('(xᵢ − x̄)²')
ax.set_ylim(0, 1500); ax.set_title(f'Quadrados dos desvios: soma = {br(sq.sum(), 0)}', fontsize=13)
save('quadrados')

# ---------- limites
fig, ax = plt.subplots(figsize=(8, 3.1))
ys = levels(x, 2.2) * .55 + .2
ax.scatter(x[:-1], ys[:-1], s=170, color=C['indigo'], zorder=3)
ax.scatter([201], [ys[-1]], s=170, color=C['red'], zorder=3)
ax.add_patch(Rectangle((q1, -1.2), q3 - q1, .9, fc=C['sky'], alpha=.5, ec=C['indigo'], lw=2))
ax.plot([med, med], [-1.2, -.3], color=C['orange'], lw=4)
for f_, t_ in [(lo, f'limite inferior\n{br(lo, 1)}'), (hi, f'limite superior\n{br(hi, 1)}')]:
    ax.axvline(f_, ymin=.02, ymax=.62, color=C['red'], ls=':', lw=2)
    ax.text(f_, 2.0, t_, ha='center', color=C['red'], fontweight='bold', fontsize=11.5)
ax.annotate('201 > 184,5: discrepante', (201, 1.0), (196, 3.0), color=C['red'], fontweight='bold', fontsize=11.5, ha='center',
            arrowprops=dict(arrowstyle='->', color=C['red'], lw=2))
ax.set_xlim(136, 208); ax.set_ylim(-1.6, 3.5); clean_y(ax); ax.set_xlabel(XL)
save('limites')

# ---------- com x sem o 201 (quanto cada medida muda, em cm)
iqr_manual = lambda v: np.median(np.sort(v)[-(len(v) // 2):]) - np.median(np.sort(v)[:len(v) // 2])
labs = ['Média', 'Mediana', 'Desvio padrão', 'IQR']
com = [x.mean(), np.median(x), x.std(ddof=1), iqr_manual(x)]
sem = [x11.mean(), np.median(x11), x11.std(ddof=1), iqr_manual(x11)]
dif = [abs(a_ - b_) for a_, b_ in zip(com, sem)]
fig, ax = plt.subplots(figsize=(8, 3.1))
yy = np.arange(4)[::-1]
ax.barh(yy, dif, color=[C['orange'] if t in ('Média', 'Desvio padrão') else C['sky'] for t in labs], height=.6)
for y_, d_, a_, b_ in zip(yy, dif, com, sem):
    ax.text(d_ + .12, y_, f'{br(d_, 1)} cm   (sem: {br(b_, 1)}  →  com: {br(a_, 1)})', va='center', fontsize=11.5,
            fontweight='bold', color=C['indigo'])
ax.set_yticks(yy); ax.set_yticklabels(labs); ax.tick_params(axis='y', length=0)
ax.set_xlim(0, 13); ax.set_xticks([]); ax.spines['left'].set_visible(False); ax.spines['bottom'].set_visible(False)
ax.set_title('Quanto o valor 201 muda cada medida', fontsize=13)
save('comparacao')


# ---------- histograma passo a passo (faixas de largura 10)
edges = [145, 155, 165, 175, 185, 195, 205]
cnt_h = np.histogram(x, edges)[0]


def hist12(stage, name):
    fig, ax = plt.subplots(figsize=(8, 2.9))
    if stage >= 2:
        for k_, (a, b) in enumerate(zip(edges[:-1], edges[1:])):
            ax.axvspan(a, b, color=C['mist'] if k_ % 2 == 0 else 'white', zorder=0)
        for e in edges:
            ax.axvline(e, color=C['soft'], lw=1, ls='--')
    if stage >= 3:
        for a, c_ in zip(edges[:-1], cnt_h):
            ax.add_patch(Rectangle((a, 0), 10, c_, fc=C['sky'], alpha=.7, ec=C['indigo'], lw=2))
            ax.text(a + 5, c_ + .12, str(c_), ha='center', fontweight='bold', color=C['indigo'])
    if stage == 1:
        ax.scatter(x[:-1], np.full(n - 1, .5), s=260, color=C['indigo'], zorder=3)
        ax.scatter([201], [.5], s=260, color=C['red'], zorder=4)
    else:
        b_ = np.digitize(x, edges[1:-1])
        cn, ys = {}, []
        for k_ in b_:
            cn[k_] = cn.get(k_, 0) + 1; ys.append(cn[k_] - .5)
        ax.scatter(x, ys, s=260, color=C['indigo'] if stage == 2 else 'white', edgecolor=C['indigo'], zorder=3)
    ax.set_xlim(142, 208); ax.set_xticks(edges); ax.set_ylim(0, 6.2); clean_y(ax); ax.set_xlabel(XL)
    save(name)


for k in (1, 2, 3):
    hist12(k, f'hist_{k}')

# ---------- barras (variável qualitativa)
fig, ax = plt.subplots(figsize=(8, 2.9))
cats, vv = ['Feminino (F)', 'Masculino (M)'], [(sexo == 'F').sum(), (sexo == 'M').sum()]
ax.bar(cats, vv, color=[C['orange'], C['sky']], width=.45, edgecolor=C['indigo'], lw=1.5)
for i_, v_ in enumerate(vv):
    ax.text(i_, v_ + .15, str(v_), ha='center', fontweight='bold', color=C['indigo'])
ax.set_ylim(0, 8.6); ax.set_yticks([]); ax.spines['left'].set_visible(False)
ax.set_title('Sexo: uma barra por categoria, com espaço entre elas', fontsize=13)
save('barras')


# ---------- boxplot passo a passo
def boxfig(stage, name):
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ys = levels(x, 2.2) * .55 + .2
    out = x > hi
    ax.scatter(x[~out], ys[~out], s=170, zorder=3, color=C['indigo'])
    ax.scatter(x[out], ys[out], s=170, zorder=3, color=C['red'] if stage >= 5 else C['indigo'])
    if stage >= 2:
        for q, t, col, ha_, yy_ in [(q1, 'Q₁ = 157', C['sky'], 'right', 2.0), (med, 'mediana = 162,5', C['amber'], 'center', 2.6),
                                    (q3, 'Q₃ = 168', C['teal'], 'left', 2.0)]:
            ax.axvline(q, ymin=.1, ymax=.72 if ha_ != 'center' else .85, color=C['soft'], ls='--', lw=1.3)
            ax.text(q + (-.8 if ha_ == 'right' else .8 if ha_ == 'left' else 0), yy_, t, ha=ha_,
                    fontweight='bold', color=col, fontsize=11.5)
    if stage >= 3:
        ax.add_patch(Rectangle((q1, -1.25), q3 - q1, .9, fc=C['sky'], alpha=.55, ec=C['indigo'], lw=2))
        ax.plot([med, med], [-1.25, -.35], color=C['orange'], lw=4)
    if stage >= 4:
        a, b = x[x >= lo].min(), x[x <= hi].max()
        ax.plot([a, q1], [-.8, -.8], color=C['indigo'], lw=2.5); ax.plot([q3, b], [-.8, -.8], color=C['indigo'], lw=2.5)
        for e in (a, b):
            ax.plot([e, e], [-1.05, -.55], color=C['indigo'], lw=2.5)
        for lim, tt in [(lo, 'limite 140,5'), (hi, 'limite 184,5')]:
            ax.axvline(lim, ymin=.05, ymax=.55, color=C['red'], ls=':', lw=1.8)
            ax.text(lim, -1.9, tt, color=C['red'], ha='center', fontsize=11, fontweight='bold')
    if stage >= 5:
        ax.scatter([201], [-.8], color=C['red'], s=110, zorder=5)
        ax.annotate('ponto isolado', (201, -.8), (188, .5), color=C['red'], fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=C['red'], lw=2))
    ax.set_xlim(134, 208); ax.set_ylim(-2.3, 3.2); clean_y(ax); ax.set_xlabel(XL)
    save(name)


for k in range(1, 6):
    boxfig(k, f'box{k}')

# ---------- dispersão: idade (x) × altura (y)
mi, mh = idade.mean(), alt.mean()


def disp(stage, name):
    fig, ax = plt.subplots(figsize=(5.6, 3.5))
    X0, X1, Y0, Y1 = 11.4, 17.6, 143, 207
    if stage == 2:
        for (xa, xb, ya, yb, col) in [(mi, X1, mh, Y1, C['cyan']), (X0, mi, Y0, mh, C['cyan']),
                                      (X0, mi, mh, Y1, C['orange']), (mi, X1, Y0, mh, C['orange'])]:
            ax.add_patch(Rectangle((xa, ya), xb - xa, yb - ya, fc=col, alpha=.18, ec='none'))
        ax.axvline(mi, color=C['soft']); ax.axhline(mh, color=C['soft'])
        for t, p, col in [('+', (16.9, 198), C['teal']), ('+', (11.9, 146.5), C['teal']),
                          ('−', (12.1, 198), C['amber']), ('−', (16.9, 146.5), C['amber'])]:
            ax.text(*p, t, fontsize=26, ha='center', va='center', fontweight='bold', color=col, alpha=.7)
        ax.text(X1 - .05, mh + 2.5, f'ȳ = {br(mh, 0)}', ha='right', color=C['soft'], fontsize=10.5)
        ax.text(mi + .08, Y0 + 2, f'x̄ = {br(mi, 1)}', color=C['soft'], fontsize=10.5)
    if stage == 3:
        ax.axvline(mi, color=C['soft'], lw=1); ax.axhline(mh, color=C['soft'], lw=1)
        sp, sn = 0, 0
        for xi, yi in zip(idade, alt):
            p_ = (xi - mi) * (yi - mh)
            ax.add_patch(Rectangle((min(xi, mi), min(yi, mh)), abs(xi - mi), abs(yi - mh),
                                   fc=C['teal'] if p_ > 0 else C['orange'], alpha=.22, ec='none'))
            sp += max(p_, 0); sn += min(p_, 0)
        ax.text(X0 + .12, Y1 - 3, f'áreas +: {br(sp, 1)}\náreas −: {br(sn, 1)}\nsoma: {br(sp + sn, 0)}', va='top',
                fontsize=11, fontweight='bold', color=C['indigo'])
    ax.scatter(idade, alt, s=90, color=C['indigo'], zorder=3)
    if stage >= 2:
        ax.scatter([17], [201], s=90, color=C['red'], zorder=4)
    ax.set_xlim(X0, X1); ax.set_ylim(Y0, Y1)
    ax.set_xlabel('x: idade (anos)'); ax.set_ylabel('y: altura (cm)')
    ax.set_xticks(range(12, 18))
    save(name)


for k in (1, 2, 3):
    disp(k, f'disp{k}')

# ---------- grade de correlações (ilustrativa)
fig, ax = plt.subplots(1, 5, figsize=(10, 2.3))
for a_, r in zip(ax, [-.9, -.4, 0, .4, .9]):
    z = rng.multivariate_normal([0, 0], [[1, r], [r, 1]], 400)
    a_.scatter(z[:, 0], z[:, 1], s=8, color=C['sky'], alpha=.7); a_.set_xticks([]); a_.set_yticks([])
    a_.set_title(f'r ≈ {r:g}'.replace('.', ',').replace('-', '−'), fontsize=13)
    for s_ in a_.spines.values():
        s_.set_visible(False)
plt.tight_layout(); save('r_grid')

# ---------- limites da correlação
xp = np.array([-2, -1, 0, 1, 2]); yp = xp ** 2
fig, ax = plt.subplots(figsize=(4.2, 3.4))
xs = np.linspace(-2.2, 2.2, 100)
ax.plot(xs, xs ** 2, color=C['line'], lw=2, zorder=1)
ax.scatter(xp, yp, s=110, color=C['indigo'], zorder=3)
ax.set_title(f'y = x²: r = {br(np.corrcoef(xp, yp)[0, 1], 2)}', fontsize=13)
ax.set_xticks(xp); ax.set_yticks([0, 2, 4])
save('trap1')

x2, y2 = rng.normal(0, 1, 50), rng.normal(0, 1, 50)
x2o, y2o = np.append(x2, 8), np.append(y2, 8)
for name, xs_, ys_, hl in [('trap2a', x2, y2, False), ('trap2b', x2o, y2o, True)]:
    fig, ax = plt.subplots(figsize=(4.2, 3.4))
    ax.scatter(xs_, ys_, s=12, color=C['sky'])
    if hl:
        ax.scatter(xs_[-1], ys_[-1], s=90, color=C['red'], zorder=3)
    r_ = np.corrcoef(xs_, ys_)[0, 1]
    ax.set_title(('Com 1 ponto: ' if hl else 'Sem o ponto: ') + f'r = {br(r_, 2)}', fontsize=13)
    ax.set_xticks([]); ax.set_yticks([])
    save(name)


# ---------- Venn: A = sexo feminino (7), B = altura >= 165 (5), A∩B = 2, Ω = 12
def venn(stage, name):
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.add_patch(Rectangle((-2.6, -1.8), 5.2, 3.6, fc='white', ec=C['soft'], lw=1.5))
    cA, cB = Circle((-.55, 0), 1.1), Circle((.55, 0), 1.1)
    if stage == 1:
        for c_, col in ((cA, C['sky']), (cB, C['orange'])):
            c_.set(fc=col, alpha=.28, ec='none'); ax.add_patch(c_)
    elif stage == 2:
        for c_ in (cA, cB):
            c_.set(fc=C['orange'], alpha=.4, ec='none'); ax.add_patch(c_)
    else:
        cA.set(fc=C['sky'], alpha=.35, ec='none'); ax.add_patch(cA)
        inter = Circle((.55, 0), 1.1, fc=C['orange'], alpha=.6, ec='none'); ax.add_patch(inter)
        inter.set_clip_path(Circle((-.55, 0), 1.1, transform=ax.transData))
    ax.add_patch(Circle((-.55, 0), 1.1, fc='none', ec=C['sky'], lw=2.5))
    ax.add_patch(Circle((.55, 0), 1.1, fc='none', ec=C['amber'], lw=2.5))
    for t, p, sz in [('5', (-1.05, 0), 17), ('2', (0, 0), 17), ('3', (1.05, 0), 17), ('2', (2.0, -1.2), 15)]:
        ax.text(*p, t, ha='center', va='center', fontsize=sz, fontweight='bold', color=C['night'])
    ax.text(-1.3, 1.4, 'A: feminino (7)', color=C['sky'], fontweight='bold', ha='center', fontsize=11.5)
    ax.text(1.3, 1.4, 'B: altura ≥ 165 (5)', color=C['amber'], fontweight='bold', ha='center', fontsize=11.5)
    ax.text(-2.5, -1.58, 'Ω (12)', color=C['soft'], fontsize=11, va='center')
    ax.set_xlim(-2.7, 2.7); ax.set_ylim(-1.9, 1.9); ax.set_aspect('equal'); ax.axis('off')
    save(name)


for k in (1, 2, 3):
    venn(k, f'venn{k}')

# ---------- lei dos grandes números (moeda justa, simulação)
fig, ax = plt.subplots(figsize=(8, 3))
N = 3000
for col in (C['sky'], C['teal'], C['indigo']):
    fl = rng.integers(0, 2, N)
    ax.plot(np.arange(1, N + 1), np.cumsum(fl) / np.arange(1, N + 1), color=col, lw=2, alpha=.9)
ax.axhline(.5, color=C['orange'], lw=2.5, ls='--'); ax.text(N * .6, .53, 'P = 0,5', color=C['amber'], fontweight='bold')
ax.set_xscale('log'); ax.set_ylim(0, 1); ax.set_xlabel('número de lançamentos (escala log)')
ax.set_ylabel('proporção de caras'); ax.set_title('Três sequências de lançamentos: a proporção estabiliza', fontsize=13)
save('lln')

# ---------- normal
t = np.linspace(-4.2, 4.2, 400); pdf = stats.norm.pdf
fig, ax = plt.subplots(1, 2, figsize=(8, 2.9), sharey=True)
for mu_, col in zip((-2, 0, 2), (C['sky'], C['orange'], C['teal'])):
    ax[0].plot(t, pdf(t, mu_, 1), color=col, lw=3); ax[0].axvline(mu_, color=col, lw=1, ls=':')
ax[0].set_title('μ desloca o sino', fontsize=13)
for sg, col in zip((.6, 1, 1.7), (C['sky'], C['orange'], C['teal'])):
    ax[1].plot(t, pdf(t, 0, sg), color=col, lw=3)
ax[1].set_title('σ espalha o sino', fontsize=13)
for a_ in ax:
    a_.set_yticks([]); a_.spines['left'].set_visible(False)
plt.tight_layout(); save('normal_mu_sigma')

print('figuras geradas:', len(os.listdir('figuras')))
