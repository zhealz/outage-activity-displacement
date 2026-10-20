"""Makes the five figures of the research summary from the result tables in results/.

Run from the repository root: python scripts/make_summary_figures.py
"""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
INK, MUTED, GRID, SURFACE, FAINT = "#0b0b0b", "#52514e", "#e6e5e1", "#ffffff", "#b9b8b2"
C_DARK, C_MID, C_LIGHT, C_GREY = "#104281", "#2a78d6", "#86b6ef", "#7a7974"
plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False, "axes.axisbelow": True,
    "text.color": INK, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
    "font.size": 9.5, "legend.frameon": False, "savefig.dpi": 220, "savefig.bbox": "tight"})

# Figure 1: dose-response
m = pd.read_csv("results/step2b/step2b_main_coefficients.csv")
bands = ["6–24 h", "24–72 h", "72–120 h", "120+ h"]
fig, ax = plt.subplots(figsize=(7, 3.1))
x = np.arange(len(bands))
for s, color, off, label in [("S1", C_LIGHT, -0.11, "Outages only"), ("S3", C_DARK, 0.11, "Wind and rain controlled")]:
    c = m[m["spec"] == s].set_index("band").reindex(bands)
    ax.errorbar(x + off, c["coef"], yerr=[c["coef"] - c["lo"], c["hi"] - c["coef"]], fmt="o", color=color, ms=5.5, elinewidth=1.5, capsize=0, label=label)
    if s == "S3":
        for xi, v in zip(x + off, c["coef"]):
            if v < -15:
                ax.text(xi + 0.09, v, f"{v:+.0f} ({(np.exp(v / 100) - 1) * 100:.0f}%)".replace("-", "−"), va="center", ha="left", fontsize=8.5, color=INK)
n = m[m["spec"] == "S3"].set_index("band").reindex(bands)["n_band"]
ax.set_xticks(x)
ax.set_xticklabels([f"{b}\n{int(v)} county-weeks" for b, v in zip(bands, n)])
ax.axhline(0, color=FAINT, lw=1)
ax.set_xlim(-0.5, 3.75)
ax.set_xlabel("Hours without power per customer in the week")
ax.set_ylabel("Visits to places in the county,\nlog points vs under 6 h")
ax.legend(loc="lower left", fontsize=8.5)
fig.savefig("figures/fig1_dose_response.png")

# Figure 2: outflow decomposition
dst = pd.read_csv("results/step3/step3_destinations.csv")
LAB = {"home": "Home county", "d0": "Other counties 0–50 km", "d1": "50–150 km", "d2": "150–400 km", "d3": "400+ km",
       "p_none": "Had power (< 6 h)", "p_some": "Partial outage (6–72 h)", "p_long": "Also without power (72+ h)", "p_out": "Outside the study states"}
fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.9), sharex=True)
for ax, (split, order, title) in zip(axes, [("distance", ["home", "d0", "d1", "d2", "d3"], "Residents' visits, by distance"),
                                            ("power", ["p_none", "p_some", "p_long", "p_out"], "Visits elsewhere, by destination's power")]):
    t = dst[dst["split"] == split].set_index("code").reindex(order)
    y = np.arange(len(t))[::-1]
    colors = [C_GREY if c == "home" else (C_DARK if v >= 0 else C_LIGHT) for c, v in zip(t.index, t["pct"])]
    ax.barh(y, t["pct"], color=colors, height=0.62)
    for yi, v in zip(y, t["pct"]):
        inside = v < -15
        ax.text(v + (1.2 if v >= 0 else (1.5 if inside else -1.2)), yi, f"{v:+.0f}%".replace("-", "−"), va="center",
                ha="left" if (v >= 0 or inside) else "right", fontsize=8.5, color=SURFACE if inside else INK)
    ax.set_yticks(y)
    ax.set_yticklabels([LAB[c] for c in t.index])
    ax.axvline(0, color=FAINT, lw=1)
    ax.grid(axis="y", visible=False)
    ax.set_title(title, fontsize=9.5, loc="left", fontweight="bold")
axes[0].set_xlim(-60, 45)
fig.supxlabel("Change against the counterfactual, % of the visits residents would have made at home", fontsize=8.5, color=MUTED, y=-0.02)
fig.tight_layout()
fig.savefig("figures/fig2_outflow.png")

# Figure 3: the Step 3 map of Ida, week 1, without its title strip
Image.open("results/step3/step3_fig4_map.png").convert("RGB").crop((0, 80, 2579, 1139)).save("figures/fig3_ida_map.png")

# Figure 4: prediction by held-out storm
p = pd.read_csv("results/step4/step4_performance.csv")
names = {"isaias2020": "Isaias", "derecho2020": "Iowa derecho", "laura2020": "Laura", "delta2020": "Delta", "okice2020": "Oklahoma ice storm",
         "zeta2020": "Zeta", "ida2021": "Ida", "pooled": "All 7, pooled", "uri2021": "Winter Storm Uri (transfer)"}
order = ["isaias2020", "derecho2020", "laura2020", "delta2020", "okice2020", "zeta2020", "ida2021", "pooled", "uri2021"]
fig, ax = plt.subplots(figsize=(7, 4.3))
ys = np.arange(len(order))[::-1].astype(float)
ys[order.index("pooled")] -= 0.6; ys[order.index("uri2021")] -= 1.2     # gaps before the pooled and transfer rows
STY = [("p_linear", C_GREY, "s", "Linear, outage duration only", 0.2), ("p_local", C_LIGHT, "o", "Boosted trees, local features", 0.0),
       ("p_net", C_DARK, "o", "Boosted trees, all features", -0.2)]
for col, color, mk, label, off in STY:
    v = p[p["model"] == col].set_index("event").reindex(order)["ap"]
    ax.scatter(v, ys + off, color=color, marker=mk, s=30, zorder=3, label=label)
base = p[p["model"] == "p_net"].set_index("event").reindex(order)["base"]
ax.scatter(base, ys, marker="|", s=140, color=INK, zorder=2, label="Chance level")
ax.axhline((ys[order.index("ida2021")] + ys[order.index("pooled")]) / 2, color=FAINT, lw=1)
ax.axhline((ys[order.index("pooled")] + ys[order.index("uri2021")]) / 2, color=FAINT, lw=1, ls=":")
ax.set_yticks(ys)
ax.set_yticklabels([names[k] for k in order])
ax.set_xlim(0, 0.85)
ax.set_xlabel("Average precision for large drops (held-out storm, weeks 0–2)")
ax.grid(axis="y", visible=False)
ax.legend(loc="lower center", bbox_to_anchor=(0.42, -0.36), ncol=2, fontsize=8.5)
fig.savefig("figures/fig4_prediction.png")

# Figure 5: on whom the loss falls
led = pd.read_csv("results/step5/step5_ledger.csv").set_index("outcome")
GROUPS = [("In the hit county", [("visits_in_chg", "Visits to places"), ("revenue_lp", "Small-business revenue"),
                                 ("merchants_lp", "Small businesses open"), ("emp_lp", "Employees paid")], C_DARK),
          ("The county's residents, wherever they are", [("visits_res_chg", "Residents' visits"), ("spend_lp", "Residents' card spending")], C_MID)]
fig, ax = plt.subplots(figsize=(7, 3.6))
pos, ticks, labs, heads = 0.0, [], [], []
for head, rows, color in GROUPS:
    heads.append((pos, head))
    pos -= 1
    for key, label in rows:
        r = led.loc[key]
        ax.errorbar(r["coef"], pos, xerr=[[r["coef"] - r["lo"]], [r["hi"] - r["coef"]]], fmt="o", color=color, ms=5.5, elinewidth=1.5, capsize=0)
        pct = (np.exp(r["coef"] / 100) - 1) * 100
        ax.text(r["hi"] + 1.5, pos, f"{r['coef']:+.0f} ({pct:+.0f}%)".replace("-", "−"), va="center", ha="left", fontsize=8.5, color=INK, bbox=dict(facecolor=SURFACE, edgecolor="none", pad=0.6))
        ticks.append(pos)
        labs.append(f"{label} ({int(r['counties_72plus'])} counties)")
        pos -= 1
    pos -= 0.3
ax.set_yticks(ticks)
ax.set_yticklabels(labs)
for yh, head in heads:
    ax.text(0.0, yh, head, transform=ax.get_yaxis_transform(), ha="left", va="center", fontsize=9, fontweight="bold", color=INK)
ax.set_ylim(pos + 0.5, 0.6)
ax.set_xlim(-70, 35)
ax.axvline(0, color=FAINT, lw=1)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Log points vs counties with under 6 h, same storm and week (95% interval)")
fig.savefig("figures/fig5_who_bears.png")
