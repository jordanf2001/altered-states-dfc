<a href="https://github.com/jordanf2001">
<img src="https://avatars.githubusercontent.com/u/154563255?v=4" width="100px;" alt=""/>
<br /><sub><b>Fan Yu-kang</b></sub>
</a># fan_project

# Dynamic Functional Connectivity in Psychedelic-Induced Altered States of Consciousness

This project investigates how psychedelic-induced altered states of consciousness influence the temporal organization of resting-state brain networks.  
The main goal is to compare **static functional connectivity (FC)** and **dynamic functional connectivity (dFC)** to determine whether dynamic measures provide additional information beyond traditional static connectivity analyses.

This repository is part of a course project focused on **open neuroscience workflows**, including dataset inspection, reproducible pipelines, and open-source neuroimaging analysis.

---

# Research Questions

This project focuses on three main questions:

- Does psilocybin-induced altered states of consciousness change resting-state brain connectivity?
- Do brain networks show different **temporal dynamics** under psychedelic conditions?
- Does **dynamic functional connectivity (dFC)** provide complementary information beyond static FC?

---

# Dataset

The analysis will use an open neuroimaging dataset from **OpenNeuro**.

**Dataset:** PsiConnect  
**Accession:** ds006110  
**Source:** https://openneuro.org/datasets/ds006110  

Key features of the dataset:

- ~65 participants
- Two sessions
- Psilocybin administration (19 mg dose)
- Multimodal recordings (MRI and EEG)
- Tasks include:
  - resting-state
  - meditation
  - music listening
  - movie watching

For this project, the analysis focuses on **resting-state fMRI data** to investigate intrinsic brain network dynamics.

The full dataset (~233 GB) is not included in this repository.

---

# Analysis Overview

The planned analysis pipeline consists of the following steps:

1. Dataset inspection and BIDS structure verification  
2. Selection of resting-state fMRI runs  
3. ROI parcellation using a brain atlas  
4. Extraction of ROI time series  
5. Static functional connectivity estimation  
6. Sliding-window dynamic functional connectivity  
7. Extraction of dynamic network features  
8. Comparison between static and dynamic connectivity measures

---

# Repository Structure

```
project-root
│
├── dataset/           # Dataset description and metadata
├── notebooks/         # Exploratory notebooks and demonstrations
├── src/               # Python scripts for analysis
├── figures/           # Pipeline diagrams and visualizations
└── docs/              # Project documentation
```

Example scripts include:

- static FC computation
- sliding-window dFC estimation
- dataset inspection

Large neuroimaging datasets are excluded from this repository using `.gitignore`.

---

# Tools and Libraries

The analysis will primarily use Python-based neuroimaging tools:

- Python
- Nilearn
- Numpy
- Pandas
- Matplotlib

These tools enable reproducible neuroimaging workflows and open neuroscience research practices.

---

# Project Status

This project is currently in the **pipeline design and dataset inspection stage**.

Current progress:

- Identification of candidate open dataset
- Definition of analysis pipeline
- Repository structure and documentation setup

Future work will include implementation of the full connectivity analysis and visualization of results.

---

# References

OpenNeuro dataset:

PsiConnect. OpenNeuro.  
https://openneuro.org/datasets/ds006110

Relevant literature on brain network dynamics and altered states of consciousness will be added as the project develops.
