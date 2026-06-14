from pathlib import Path
import argparse
import pandas as pd
import nibabel as nib


def safe_load_nifti(path):
    """
    Try to load a NIfTI file using nibabel.

    Returns
    -------
    result : dict
        Dictionary containing readability status, shape, number of volumes, TR,
        and error message if loading fails.
    """
    result = {
        "readable": False,
        "shape": "",
        "n_volumes": None,
        "tr": None,
        "error": "",
    }

    try:
        img = nib.load(str(path))
        shape = img.shape
        header = img.header

        result["readable"] = True
        result["shape"] = str(shape)

        if len(shape) == 4:
            result["n_volumes"] = shape[3]
        elif len(shape) == 3:
            result["n_volumes"] = 1
        else:
            result["n_volumes"] = None

        zooms = header.get_zooms()
        if len(zooms) >= 4:
            result["tr"] = float(zooms[3])
        else:
            result["tr"] = None

    except Exception as e:
        result["error"] = str(e)

    return result


def safe_read_confounds(path):
    """
    Try to read a confounds TSV file.

    Returns
    -------
    result : dict
        Dictionary containing readability status, row count, column count,
        framewise displacement summary, and error message if loading fails.
    """
    result = {
        "confounds_readable": False,
        "confounds_n_rows": None,
        "confounds_n_cols": None,
        "fd_mean": None,
        "fd_max": None,
        "confounds_error": "",
    }

    try:
        df = pd.read_csv(path, sep="\t")

        result["confounds_readable"] = True
        result["confounds_n_rows"] = int(df.shape[0])
        result["confounds_n_cols"] = int(df.shape[1])

        if "framewise_displacement" in df.columns:
            fd = pd.to_numeric(df["framewise_displacement"], errors="coerce")
            result["fd_mean"] = float(fd.mean(skipna=True))
            result["fd_max"] = float(fd.max(skipna=True))

    except Exception as e:
        result["confounds_error"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Generate BOLD metadata QC table for resting-state fMRI files."
    )

    parser.add_argument(
        "--file-index",
        type=str,
        default="outputs/file_index/rest_file_index.csv",
        help="Path to resting-state file index CSV."
    )

    parser.add_argument(
        "--output",
        type=str,
        default="outputs/qc/rest_bold_qc.csv",
        help="Output QC CSV path."
    )

    args = parser.parse_args()

    file_index_path = Path(args.file_index)
    output_path = Path(args.output)

    if not file_index_path.exists():
        raise FileNotFoundError(f"File index not found: {file_index_path}")

    index_df = pd.read_csv(file_index_path)

    rows = []

    for _, row in index_df.iterrows():
        bold_path = Path(row["bold_mni_path"])
        confounds_path = Path(row["confounds_path"])
        mask_path = Path(row["brain_mask_path"])

        bold_exists = bold_path.exists()
        confounds_exists = confounds_path.exists()
        mask_exists = mask_path.exists()

        bold_qc = {
            "bold_readable": False,
            "bold_shape": "",
            "bold_n_volumes": None,
            "bold_tr": None,
            "bold_error": "",
        }

        mask_qc = {
            "mask_readable": False,
            "mask_shape": "",
            "mask_error": "",
        }

        confounds_qc = {
            "confounds_readable": False,
            "confounds_n_rows": None,
            "confounds_n_cols": None,
            "fd_mean": None,
            "fd_max": None,
            "confounds_error": "",
        }

        if bold_exists:
            bold_result = safe_load_nifti(bold_path)
            bold_qc["bold_readable"] = bold_result["readable"]
            bold_qc["bold_shape"] = bold_result["shape"]
            bold_qc["bold_n_volumes"] = bold_result["n_volumes"]
            bold_qc["bold_tr"] = bold_result["tr"]
            bold_qc["bold_error"] = bold_result["error"]

        if mask_exists:
            mask_result = safe_load_nifti(mask_path)
            mask_qc["mask_readable"] = mask_result["readable"]
            mask_qc["mask_shape"] = mask_result["shape"]
            mask_qc["mask_error"] = mask_result["error"]

        if confounds_exists:
            confounds_qc = safe_read_confounds(confounds_path)

        bold_confounds_aligned = False
        if (
            bold_qc["bold_n_volumes"] is not None
            and confounds_qc["confounds_n_rows"] is not None
        ):
            bold_confounds_aligned = (
                int(bold_qc["bold_n_volumes"])
                == int(confounds_qc["confounds_n_rows"])
            )

        ready_for_roi_extraction = bool(
            bold_exists
            and confounds_exists
            and mask_exists
            and bold_qc["bold_readable"]
            and confounds_qc["confounds_readable"]
            and mask_qc["mask_readable"]
            and bold_confounds_aligned
        )

        qc_row = {
            "subject": row["subject"],
            "session": row["session"],
            "task": row["task"],
            "run": row["run"],

            "bold_mni_path": row["bold_mni_path"],
            "confounds_path": row["confounds_path"],
            "brain_mask_path": row["brain_mask_path"],

            "bold_mni_relpath": row.get("bold_mni_relpath", ""),
            "confounds_relpath": row.get("confounds_relpath", ""),
            "brain_mask_relpath": row.get("brain_mask_relpath", ""),

            "bold_exists": bold_exists,
            "confounds_exists": confounds_exists,
            "mask_exists": mask_exists,

            "bold_readable": bold_qc["bold_readable"],
            "bold_shape": bold_qc["bold_shape"],
            "bold_n_volumes": bold_qc["bold_n_volumes"],
            "bold_tr": bold_qc["bold_tr"],
            "bold_error": bold_qc["bold_error"],

            "confounds_readable": confounds_qc["confounds_readable"],
            "confounds_n_rows": confounds_qc["confounds_n_rows"],
            "confounds_n_cols": confounds_qc["confounds_n_cols"],
            "fd_mean": confounds_qc["fd_mean"],
            "fd_max": confounds_qc["fd_max"],
            "confounds_error": confounds_qc["confounds_error"],

            "mask_readable": mask_qc["mask_readable"],
            "mask_shape": mask_qc["mask_shape"],
            "mask_error": mask_qc["mask_error"],

            "bold_confounds_aligned": bold_confounds_aligned,
            "ready_for_roi_extraction": ready_for_roi_extraction,
        }

        rows.append(qc_row)

    qc_df = pd.DataFrame(rows)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    qc_df.to_csv(output_path, index=False)

    print("=" * 70)
    print("Resting-state BOLD metadata QC completed")
    print("=" * 70)
    print(f"Input file index: {file_index_path}")
    print(f"Output QC table:  {output_path}")
    print(f"Rows:             {len(qc_df)}")
    print()

    print("File existence summary:")
    print(f"BOLD exists:      {qc_df['bold_exists'].sum()} / {len(qc_df)}")
    print(f"Confounds exists: {qc_df['confounds_exists'].sum()} / {len(qc_df)}")
    print(f"Mask exists:      {qc_df['mask_exists'].sum()} / {len(qc_df)}")
    print()

    print("Readability summary:")
    print(f"BOLD readable:      {qc_df['bold_readable'].sum()} / {len(qc_df)}")
    print(f"Confounds readable: {qc_df['confounds_readable'].sum()} / {len(qc_df)}")
    print(f"Mask readable:      {qc_df['mask_readable'].sum()} / {len(qc_df)}")
    print()

    print("Temporal alignment summary:")
    print(qc_df["bold_confounds_aligned"].value_counts(dropna=False))
    print()

    print("Ready for ROI extraction:")
    print(qc_df["ready_for_roi_extraction"].value_counts(dropna=False))
    print()

    print("Rows ready for ROI extraction:")
    ready_df = qc_df[qc_df["ready_for_roi_extraction"] == True]
    if len(ready_df) > 0:
        cols = [
            "subject",
            "session",
            "task",
            "run",
            "bold_shape",
            "bold_n_volumes",
            "bold_tr",
            "confounds_n_rows",
            "fd_mean",
            "fd_max",
        ]
        print(ready_df[cols].to_string(index=False))
    else:
        print("No rows are currently ready for ROI extraction.")


if __name__ == "__main__":
    main()

