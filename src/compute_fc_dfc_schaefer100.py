from pathlib import Path
import argparse
import numpy as np
import pandas as pd

# ... (corr_matrix, fisher_z, vectorize_upper_triangle 函式保持不變) ...

def main():
    parser = argparse.ArgumentParser(description="Compute static FC and sliding-window DFC from ROI time series.")
    parser.add_argument("--timeseries-summary", type=str, default="outputs/roi_timeseries/roi_timeseries_summary.csv")
    # 修改輸出目錄預設值
    parser.add_argument("--output-dir", type=str, default="outputs/fc_dfc_schaefer100")
    parser.add_argument("--window-size", type=int, default=60)
    parser.add_argument("--step-size", type=int, default=10)
    args = parser.parse_args()

    summary_path = Path(args.timeseries_summary)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not summary_path.exists():
        raise FileNotFoundError(f"Time series summary not found: {summary_path}")

    summary_df = pd.read_csv(summary_path)
    all_summary_rows = []

    for _, row in summary_df.iterrows():
        subject = row["subject"]
        session = row["session"]
        task = row["task"]
        run = row["run"]
        ts_path = Path(row["timeseries_z_path"])

        base = f"{subject}_{session}_{task}_{run}"

        print("=" * 70)
        print(f"Processing FC/DFC: {base}")
        print(f"Time series: {ts_path}")

        ts_df = pd.read_csv(ts_path)
        ts = ts_df.values
        roi_names = list(ts_df.columns)

        n_t, n_rois = ts.shape
        print(f"Timepoints: {n_t}")
        print(f"ROIs:       {n_rois}")

        # Static FC
        fc = corr_matrix(ts)
        fc_z = fisher_z(fc)

        fc_out = output_dir / f"{base}_static_fc.csv"
        fc_z_out = output_dir / f"{base}_static_fc_fisher_z.csv"

        pd.DataFrame(fc, index=roi_names, columns=roi_names).to_csv(fc_out)
        pd.DataFrame(fc_z, index=roi_names, columns=roi_names).to_csv(fc_z_out)

        # Sliding-window DFC
        window_size = args.window_size
        step_size = args.step_size

        if n_t < window_size:
            raise ValueError(f"Time series length {n_t} is shorter than window size {window_size}")

        window_rows = []
        window_fc_vectors = []

        win_id = 0
        for start in range(0, n_t - window_size + 1, step_size):
            end = start + window_size
            ts_win = ts[start:end, :]

            fc_win = corr_matrix(ts_win)
            fc_win_z = fisher_z(fc_win)

            win_fc_out = output_dir / f"{base}_window-{win_id:03d}_fc_fisher_z.csv"
            pd.DataFrame(fc_win_z, index=roi_names, columns=roi_names).to_csv(win_fc_out)

            fc_vec = vectorize_upper_triangle(fc_win_z)
            window_fc_vectors.append(fc_vec)

            window_rows.append(
                {
                    "subject": subject,
                    "session": session,
                    "task": task,
                    "run": run,
                    "window_id": win_id,
                    "start_index": start,
                    "end_index": end,
                    "window_size": window_size,
                    "step_size": step_size,
                    "fc_matrix_path": str(win_fc_out),
                    "mean_fc_z": float(np.nanmean(fc_vec)),
                    "std_fc_z": float(np.nanstd(fc_vec)),
                }
            )

            win_id += 1

        window_df = pd.DataFrame(window_rows)
        window_summary_out = output_dir / f"{base}_window_summary.csv"
        window_df.to_csv(window_summary_out, index=False)

        window_fc_vectors = np.array(window_fc_vectors)

        # DFC variability: standard deviation across windows for each edge
        edge_std = np.nanstd(window_fc_vectors, axis=0)
        edge_mean = np.nanmean(window_fc_vectors, axis=0)

        edge_summary_out = output_dir / f"{base}_edge_dfc_summary.csv"
        edge_df = pd.DataFrame(
            {
                "edge_index": np.arange(len(edge_mean)),
                "mean_fc_z_across_windows": edge_mean,
                "std_fc_z_across_windows": edge_std,
            }
        )
        edge_df.to_csv(edge_summary_out, index=False)

        all_summary_rows.append(
            {
                "subject": subject,
                "session": session,
                "task": task,
                "run": run,
                "n_timepoints": n_t,
                "n_rois": n_rois,
                "window_size": window_size,
                "step_size": step_size,
                "n_windows": len(window_df),
                "static_fc_path": str(fc_out),
                "static_fc_z_path": str(fc_z_out),
                "window_summary_path": str(window_summary_out),
                "edge_dfc_summary_path": str(edge_summary_out),
                "mean_edge_variability": float(np.nanmean(edge_std)),
                "max_edge_variability": float(np.nanmax(edge_std)),
            }
        )

        print(f"Saved static FC:       {fc_out}")
        print(f"Saved static FC z:     {fc_z_out}")
        print(f"Saved window summary:  {window_summary_out}")
        print(f"Saved edge DFC table:  {edge_summary_out}")
        print(f"Number of windows:     {len(window_df)}")
        print(f"Mean edge variability: {np.nanmean(edge_std):.6f}")

    all_summary_df = pd.DataFrame(all_summary_rows)
    all_summary_out = output_dir / "fc_dfc_summary.csv"
    all_summary_df.to_csv(all_summary_out, index=False)

    print("=" * 70)
    print("FC/DFC computation completed")
    print(f"Summary saved to: {all_summary_out}")
    print(all_summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
