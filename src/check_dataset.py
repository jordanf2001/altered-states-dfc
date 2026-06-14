from pathlib import Path
import argparse


def count_files(root, pattern):
    return sorted(root.glob(pattern))


def main():
    parser = argparse.ArgumentParser(
        description="Check availability of fMRIPrep resting-state derivatives."
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        required=True,
        help="Path to the local ds006110 dataset directory."
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    fmriprep_dir = data_dir / "derivatives" / "fmriprep-22.0.2"

    if not fmriprep_dir.exists():
        raise FileNotFoundError(f"fMRIPrep directory not found: {fmriprep_dir}")

    patterns = {
        "rest_mni_preproc_bold": "**/*task-rest*space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz",
        "rest_confounds": "**/*task-rest*desc-confounds_timeseries.tsv",
        "rest_mni_brain_masks": "**/*task-rest*space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz",
        "rest_all_derivatives": "**/*task-rest*",
        "ses01_rest_mni_bold": "**/*ses-01*task-rest*space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz",
        "ses02_rest_mni_bold": "**/*ses-02*task-rest*space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz",
        "ses01_rest_confounds": "**/*ses-01*task-rest*desc-confounds_timeseries.tsv",
        "ses02_rest_confounds": "**/*ses-02*task-rest*desc-confounds_timeseries.tsv",
        "ses01_rest_mni_masks": "**/*ses-01*task-rest*space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz",
        "ses02_rest_mni_masks": "**/*ses-02*task-rest*space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz",
    }

    print("=" * 70)
    print("PsiConnect / ds006110 fMRIPrep Resting-State Dataset Check")
    print("=" * 70)
    print(f"Dataset directory: {data_dir}")
    print(f"fMRIPrep directory: {fmriprep_dir}")
    print()

    results = {}

    for label, pattern in patterns.items():
        files = count_files(fmriprep_dir, pattern)
        results[label] = files
        print(f"{label}: {len(files)}")

    print()
    print("=" * 70)
    print("Example MNI-space resting-state BOLD files")
    print("=" * 70)

    for file in results["rest_mni_preproc_bold"][:10]:
        print(file)

    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)

    n_bold = len(results["rest_mni_preproc_bold"])
    n_confounds = len(results["rest_confounds"])
    n_masks = len(results["rest_mni_brain_masks"])

    print(f"Rest MNI preprocessed BOLD files: {n_bold}")
    print(f"Rest confounds TSV files:        {n_confounds}")
    print(f"Rest MNI brain mask files:       {n_masks}")

    if n_bold == n_confounds:
        print("BOLD/confounds count match:      YES")
    else:
        print("BOLD/confounds count match:      NO")

    if n_bold == n_masks:
        print("BOLD/mask count match:           YES")
    else:
        print("BOLD/mask count match:           NO")

    if n_bold > 0 and n_bold == n_confounds == n_masks:
        print("FC/dFC pipeline feasibility:     YES")
    else:
        print("FC/dFC pipeline feasibility:     NEEDS REVIEW")

    print()
    print("=" * 70)
    print("Session-level Summary")
    print("=" * 70)

    print(f"ses-01 rest MNI BOLD files:      {len(results['ses01_rest_mni_bold'])}")
    print(f"ses-02 rest MNI BOLD files:      {len(results['ses02_rest_mni_bold'])}")
    print(f"ses-01 rest confounds files:     {len(results['ses01_rest_confounds'])}")
    print(f"ses-02 rest confounds files:     {len(results['ses02_rest_confounds'])}")
    print(f"ses-01 rest MNI mask files:      {len(results['ses01_rest_mni_masks'])}")
    print(f"ses-02 rest MNI mask files:      {len(results['ses02_rest_mni_masks'])}")


if __name__ == "__main__":
    main()
