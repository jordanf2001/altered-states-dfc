# Computationally Reproducible FC/dFC Workflow for Psychedelic Resting-State fMRI

#### Author: Yu-kan Fan (范育康)
#### Institution: National Taiwan University

---

## 1. Motivation: Consciousness Is Dynamic

Conscious states — whether resting, psychedelic, or sensory-deprived — fluctuate over time.

Traditional **static functional connectivity (sFC)** averages the entire scan into a single matrix, which erases these temporal dynamics. The figure below shows that brain-wide connectivity patterns are **not constant**: different time windows form distinct similarity blocks.

<div align="center">
  <p><b>Why Dynamics Matter: Window-to-Window FC Similarity</b></p>
  <img src="sch100_window_to_window_fc_similarity.png" alt="Window-to-window FC similarity" width="48%">
</div>

If we only ran static analysis, this temporal structure would be **completely averaged away**. This is the core motivation for building a **dynamic functional connectivity (dFC)** pipeline.

---

## 2. The Solution: A Reproducible Pipeline

This repository develops a **computationally reproducible workflow** for static and dynamic FC analysis of resting-state fMRI from the PsiConnect dataset (OpenNeuro `ds006110`).

**Reproducible** here means computational reproducibility:

```text
same derivatives + same code + same parameters → same outputs
```

At this stage the project focuses on **workflow construction and pilot-run validation**.

The **pipeline** runs from dataset inspection and QC, through ROI extraction, to sliding-window dFC feature extraction:

<div align="center">
  <img src="analysispipeline.png" alt="analysis pipeline" width="30%">
</div>



**Dataset status:** 127 resting-state runs with matched BOLD / confounds / mask files were verified (ses-01: 65, ses-02: 62). The pipeline feasibility check passed.

---

## 3. Pipeline 1 — Validation with a Preliminary Grid Atlas

To prove the pipeline runs end-to-end, I first applied it to one pilot run using a **preliminary grid atlas (67 ROIs)**.

```text
sub-PC001 / ses-01 / task-rest / run-1
```

> This atlas is purely geometric. Its goal is **code validation**, not neurobiological interpretation.

| Output | Result |
|---|---:|
| ROI time-series matrix | 504 × 67 |
| Static FC matrix | 67 × 67 |
| Unique FC edges | 2211 |
| Sliding-window FC matrices | 45 |
| Mean edge dFC variability | 0.361 |

<div align="center">
  <p><b>Grid Atlas — Static FC Matrix</b></p>
  <img src="figures/pilot_grid67_static_fc_matrix.png" alt="Grid static FC" width="62%">
</div>

**Result:** The pipeline successfully produced ROI time series, static FC, and 45 dynamic FC windows. The code works.

---

## 4. Pipeline 2 — System Upgrade with Schaefer 100 ⭐

A grid atlas only cuts the brain by geometry. To make results **biologically meaningful**, I upgraded the same pipeline to the **Schaefer 100 atlas**, which is defined from real functional brain networks (e.g. the Default Mode Network).

> **Why Schaefer 100, not 400?** Finer parcellation (400) demands much heavier noise regression. Schaefer 100 is the best balance between **capturing network dynamics** and **controlling noise** at the pilot stage.

| Metric | Grid atlas | Schaefer 100 |
|---|---:|---:|
| ROIs | 67 | 100 |
| Unique edges | 2211 | 4950 |
| Static mean FC | 0.496 | 0.488 |
| Static FC SD | 0.334 | 0.257 |
| Mean dFC variability | 0.361 | 0.355 |
| Max dFC variability | 0.653 | 0.689 |

### 4.1 ROI Time Series

<div align="center">
  <p><b>Schaefer 100 — ROI Time-Series Heatmap</b></p>
  <img src="figures/pilot_schaefer100_roi_timeseries_heatmap.png" alt="Schaefer ROI heatmap" width="55%">
</div>

**Note the vertical bands:** many ROIs fluctuate at the *same* time points. In fMRI this typically reflects **global signal, head motion, or physiological noise**. I treat this heatmap as a **quality-control signal**, not as neural evidence — it tells me denoising must be strengthened next.

### 4.2 Static FC — Grid vs Schaefer 100

<div align="center">
  <p><b>Schaefer 100 — Static FC Matrix</b></p>
  <img src="figures/pilot_schaefer100_static_fc_matrix.png" alt="Schaefer static FC" width="70%">
</div>

Compared with the grid atlas, the Schaefer 100 matrix shows a **more structured, network-organized layout** and a **narrower FC distribution** (SD 0.334 → 0.257). Because ROIs are now functionally coherent, connectivity estimates are more stable and interpretable.

<div align="center">
  <p><b>Schaefer 100 — Static FC Descriptive Checks</b></p>
  <img src="figures/pilot_schaefer100_static_fc_descriptive_checks.png" alt="Schaefer FC checks" width="68%">
</div>

### 4.3 Dynamic FC

<div align="center">
  <p><b>Schaefer 100 — dFC Mean Connectivity Trajectory</b></p>
  <img src="figures/pilot_schaefer100_dfc_mean_connectivity_trajectory.png" alt="Schaefer dFC trajectory" width="68%">
</div>

Mean connectivity is **not flat** across windows — confirming there is temporal structure for dFC to capture.

<div align="center">
  <p><b>Schaefer 100 — dFC Variability Matrix</b></p>
  <img src="figures/pilot_schaefer100_dfc_variability_matrix.png" alt="Schaefer dFC variability" width="48%">
</div>

Brighter edges fluctuate more over time. With Schaefer 100, these variable edges can later be **mapped onto large-scale networks** — something the grid atlas could not support.

---

## 5. Summary: One Framework, Two Depths

| | Pipeline 1 (Grid) | Pipeline 2 (Schaefer 100) |
|---|---|---|
| Purpose | Code / data validation | Feature extraction |
| Atlas | Geometric grid | Functional networks |
| Interpretability | Low | Network-level |
| Status | ✅ Validated | ✅ Validated |

- **Pipeline 1** proves the workflow runs correctly from data to sFC/dFC.
- **Pipeline 2** introduces preliminary denoising and Schaefer 100 to extract **neurobiologically meaningful** dynamic features.

This open, plug-and-play toolkit is ready to scale to the remaining 127 PsiConnect runs, and can lower the technical barrier for newcomers to dFC analysis — including my own future **sensory-deprivation research**.

---

## 6. Limitations & Next Steps

**Limitations**
- Only one pilot run processed; no group-level inference yet.
- Vertical bands suggest residual global signal / motion; denoising not finalized.
- The meaning of `ses-01` vs `ses-02` still needs confirmation from dataset documentation.

**Next Steps**
- Add motion QC (framewise displacement) and global-signal checks.
- Scale to all 127 matched runs.
- Map Schaefer 100 ROIs onto 7 large-scale networks for within/between-network dFC.
- Link runs to session/condition metadata, then compare FC/dFC features.

---

## 7. Usage

```bash
python src/check_dataset.py --data-dir /path/to/ds006110
python src/build_file_index.py --data-dir /path/to/ds006110
```

Figures are reproduced via `pilot_schaefer100_generation.ipynb` (upload the Schaefer 100-derived CSVs and `fc_dfc_schaefer100.zip` when prompted).

---

## License

Released under the MIT License. The license applies only to the code and documentation in this repository; the original PsiConnect dataset follows its own OpenNeuro terms.
