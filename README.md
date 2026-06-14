# Dynamic Functional Connectivity in Psychedelic-Induced Altered States of Consciousness

Author: Fan Yu-kang  
Institution: National Taiwan University

This project investigates how psychedelic-induced altered states of consciousness influence the temporal organization of resting-state brain networks.

The main goal is to compare **static functional connectivity (FC)** and **dynamic functional connectivity (dFC)** to determine whether dynamic connectivity measures provide additional information beyond traditional static connectivity analyses.

This repository is part of a course project focused on **open neuroscience workflows**, including dataset inspection, reproducible pipelines, and open-source neuroimaging analysis.

---

# Research Questions

This project focuses on three main questions:

- How do psilocybin-induced altered states of consciousness alter resting-state brain connectivity?
- Do brain networks exhibit different **temporal dynamics** under psychedelic conditions?
- Does **dynamic functional connectivity (dFC)** provide complementary information beyond static FC?

---

# Dataset

The analysis uses an open neuroimaging dataset from **OpenNeuro**.

Dataset: PsiConnect  
Accession: ds006110  
Source: https://openneuro.org/datasets/ds006110  

Key features of the dataset:

- ~65 participants
- Two sessions
- Psilocybin administration (19 mg dose)
- Multimodal recordings (MRI and EEG)
- Tasks include resting-state, meditation, music listening, and movie watching

This project focuses on **resting-state fMRI data** to analyze intrinsic brain network dynamics.

The full dataset (~233 GB) is **not included in this repository**.

## Dataset Availability Update

Full fMRIPrep derivatives were verified in the local DataLad file tree. The dataset includes resting-state preprocessed BOLD images and corresponding confound regressors, including MNI152NLin2009cAsym-space outputs:

- `*_task-rest_*space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz`
- `*_task-rest_*desc-confounds_timeseries.tsv`

This confirms that the dataset can support resting-state functional connectivity and dynamic functional connectivity analyses, pending selective download of the required git-annexed files.


---

# Analysis Pipeline

![analysis pipeline](analysispipeline.png)


The analysis pipeline consists of the following steps:

1. Dataset inspection and BIDS structure verification  
2. Selection of resting-state fMRI runs  
3. ROI parcellation using a standard brain atlas (e.g., Schaefer or AAL)  
4. Extraction of ROI time series  
5. Static functional connectivity estimation  
6. Sliding-window dynamic functional connectivity  
7. Extraction of dynamic network features  
8. Comparison between static and dynamic connectivity measures
