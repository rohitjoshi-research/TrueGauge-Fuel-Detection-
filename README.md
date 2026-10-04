# TrueGauge

**A retrofit-viable, sensorless-first energy integrity indicator for fuel adulteration and EV charging.**

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22674618-blue)](https://doi.org/10.5281/zenodo.22674618)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0007--4201--7862-a6ce39)](https://orcid.org/0009-0007-4201-7862)
![Status](https://img.shields.io/badge/status-design%20%26%20protocol-orange)

---

## Status: read this first

This repository holds a **design, a simulation prototype, and a validation protocol**. It does **not** hold a working product.

- No prototype, trained model, or labeled real-world dataset exists yet.
- Everything in the notebooks is **synthetic or simulated**. It checks the pipeline and the design logic. It never supports an accuracy claim.
- App screens in `demo/` are mock-ups. The news cards on the news screen are real, dated headlines, shown with their sources.

The paper states exactly which evidence is still missing (Table X) and the minimum bar for completing the study (Section VIII).

## The idea in four lines

1. The pump shows price and litres. The vehicle reports nothing about fuel quality or charging integrity.
2. TrueGauge reads signals the vehicle already produces (OBD-II, battery management system) and returns one score per energy type: Good, Caution, or Poor.
3. Scores are judged against the **legal standard of the jurisdiction** (BIS, SABS, EU), not one fixed threshold.
4. A reading stays **provisional** until it is confirmed; public station flags need N independent reports.

## What is in this repository

```
paper/
  TrueGauge-EII-IEEE-format.pdf      the paper (IEEE two-column format, 18 pages)
  source/                            LaTeX source, figures, and the scripts that regenerate them
notebooks/
  TrueGauge_EII_notebook.ipynb       formal model (Eq. 1-7) and Algorithm 1 on SYNTHETIC data
  TrueGauge_report_and_statistics.ipynb   index of every real statistic the paper cites
  TrueGauge_simulation.ipynb         fuel-side simulator: how adulterants and faults move fuel trims
simulation/
  sim_core.py                        simulator core (mixture physics, closed-loop ECU model)
data/
  scene_catalog.csv                  the 17-scene validation catalog (12 fuel, 5 EV)
  scene_dimensions.csv               13 scene dimensions and their levels
  sim_steady_state.csv               idealised steady-state trim shift by adulterant
demo/
  truegauge-phone-final.html         phone app mock-up (7 screens), open in any browser
  truegauge-final-full-recording.html  phone screens plus 16 use cases in two themes
  truegauge-hmi-before-after.html    before/after dashboard concept
  truegauge-full-coverage.svg        all 16 use cases on one page
  videos/                            two short walkthrough videos
docs/
  overview-simple.md                 plain-language overview
  paper-summary.md                   plain-language summary of the paper
```

## Quick start

**Read the paper:** open `paper/TrueGauge-EII-IEEE-format.pdf`.

**Run a notebook:** open any file in `notebooks/` in [Google Colab](https://colab.research.google.com) and choose *Runtime → Run all*. No GPU is needed.

**Rebuild the paper:**

```bash
cd paper/source
pdflatex truegauge.tex && pdflatex truegauge.tex && pdflatex truegauge.tex
```

This needs a LaTeX installation with the `IEEEtran` class, TikZ, and the `algorithms` package.

**Regenerate the figures and tables:**

```bash
pip install -r requirements.txt
cd paper/source
python build_assets.py        # evidence pies, cost chart, scene coverage matrix, scene tables
python build_overview.py      # page-1 graphical abstract
python build_sim_assets.py    # simulation figure and steady-state table
```

## Main contributions of the paper

- A unified Energy Integrity Index (Fuel Quality Index and Charging Integrity Index) with a provisional/confirmed state policy and region-calibrated scoring.
- A patent-landscape review that delimits the design space, most closely against Volkswagen's DE102024134018A1.
- A dual-track design: sensorless first, optional hardware second.
- A 17-scene validation catalog with independent reference methods, plus a simulation-based pre-validation plan.
- A critical review from six perspectives, an adopter analysis, and an itemised list of the evidence still missing.

## Findings worth knowing (all simulated, assumed fuel properties)

- Adulterants that change stoichiometry (ethanol, methanol, ketones, water) shift fuel trims by several percent at 10-20 % concentration.
- Kerosene and paraffin shift trims by under 1 % at 10 %, so trims alone are unlikely to identify them.
- A +3.3 % shift fits about 9 % ethanol, 10 % acetone, or 6 % methanol, so trim magnitude cannot name the adulterant.
- Confounders are as large as the effects of interest: a 30 °C warmer fuel is about +3 %, and a 4 % sensor gain error is about -3.8 %.

## How to cite

```
Joshi, R. (2026). TrueGauge: A Retrofit-Viable, Sensorless-First Vehicle Energy
Integrity Indicator for Fuel Adulteration and EV Charging Integrity. Zenodo.
https://doi.org/10.5281/zenodo.22674618
```

GitHub also reads `CITATION.cff` to offer a "Cite this repository" button.

## Third-party content

The video `demo/videos/truegauge-phone-demo-v3.mp4` includes screenshots of news pages shown for illustration. Their sources are credited in the video's end card, and all rights remain with the publishers.

## Disclosures

- **Funding:** none. This is independent research.
- **Conflict of interest:** the author works in the automotive HMI and visualization domain at a Tier 1 supplier. This is an independent research concept and does not represent the position, product roadmap, or intellectual property of that employer or of any company named in the patent review.

## License

To be added. Until a license is chosen, all rights are reserved.
