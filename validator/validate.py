#!/usr/bin/env python3
"""Validator của nhóm 07 cho Lab 10.

Giao diện CLI chuẩn:
  python validator/validate.py <thư_mục_delivery> --out <errors.json> [--candidates <candidates.json>]

Phân công module:
  - Khung CLI & Rule File/Metadata: Văn (Team Lead)
  - Rule YOLO & Panoptic: Minh (rules_yolo_panoptic.py)
  - Cross-check Candidates: Vũ
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

# Import module kiểm tra lỗi YOLO & Panoptic của Minh
try:
    from validator.rules_yolo_panoptic import check_yolo_label, check_panoptic_ann
except ImportError:
    from rules_yolo_panoptic import check_yolo_label, check_panoptic_ann

# Import module đối chiếu nhãn và sinh ứng viên của Vũ
try:
    from validator.cross_check import generate_candidates
except ImportError:
    from cross_check import generate_candidates

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

try:
    import pngutil
except ImportError:
    pngutil = None


def sha256_file(path: Path) -> str:
    """Tính mã băm SHA256 trên bytes thực tế của file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def check_file_and_metadata_rules(delivery_dir: Path) -> list[tuple[str, str]]:
    """Kiểm tra các lỗi luật mức File và Metadata (Phụ trách: Văn).
    
    1. missing_image: manifest có nhưng thiếu file ảnh
    2. wrong_hash: sha256 thật khác sha256 trong manifest
    3. scene_leak: cùng 1 cảnh nhưng có ảnh ở cả train và val
    4. guideline_mismatch: guideline của ảnh khác guideline của job trong jobs.csv
    """
    errors: list[tuple[str, str]] = []
    
    manifest_path = delivery_dir / "manifest.json"
    metadata_path = delivery_dir / "metadata.json"
    jobs_path = delivery_dir / "jobs.csv"

    if not manifest_path.is_file() or not metadata_path.is_file() or not jobs_path.is_file():
        return errors

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))["items"]
    metadata = {m["image"]: m for m in json.loads(metadata_path.read_text(encoding="utf-8"))["items"]}
    jobs = {row["job_id"]: row for row in read_csv(jobs_path)}

    scene_splits: dict[str, set[str]] = {}

    for stem, it in manifest.items():
        m = metadata.get(stem, {})
        scene_id = m.get("scene_id")
        split = m.get("split")
        job_id = m.get("job_id")
        img_guideline = m.get("guideline_version")

        # Gom split theo scene để kiểm tra scene_leak
        if scene_id and split:
            scene_splits.setdefault(scene_id, set()).add(split)

        # 1. missing_image
        img_file = delivery_dir / it["image"]
        if not img_file.is_file():
            errors.append(("missing_image", stem))
            continue

        # 2. wrong_hash (đọc chế độ byte 'rb')
        if sha256_file(img_file) != it["image_sha256"]:
            errors.append(("wrong_hash", stem))
            continue

        # 4. guideline_mismatch (so với guideline ghi ở job trong jobs.csv)
        job = jobs.get(job_id)
        if job and img_guideline != job.get("guideline"):
            errors.append(("guideline_mismatch", stem))

    # 3. scene_leak (target là scene_id, ví dụ 'scene_557')
    for scene_id, splits in scene_splits.items():
        if len(splits) > 1:
            errors.append(("scene_leak", scene_id))

    return errors


# generate_candidates duoc import tu validator.cross_check (Phu trach: Vu)


def main():
    parser = argparse.ArgumentParser(description="Day 10 Lab Validator — Nhóm 07")
    parser.add_argument("delivery", type=str, help="Đường dẫn thư mục delivery cần kiểm tra")
    parser.add_argument("--out", type=str, required=True, help="Đường dẫn file errors.json xuất ra")
    parser.add_argument("--candidates", type=str, default=None, help="Đường dẫn file candidates.json xuất ra (tùy chọn)")
    args = parser.parse_args()

    delivery_dir = Path(args.delivery).resolve()
    if not delivery_dir.is_dir():
        print(f"Lỗi: Thư mục {delivery_dir} không tồn tại!", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Bắt đầu kiểm tra dữ liệu tại: {delivery_dir.name}")
    all_errors: list[dict] = []
    seen_errors: set[tuple[str, str]] = set()

    def add_err(etype: str, target: str):
        if (etype, target) not in seen_errors:
            seen_errors.add((etype, target))
            all_errors.append({"type": etype, "target": target})

    # --- 1. Luật File & Metadata (Văn) ---
    file_errors = check_file_and_metadata_rules(delivery_dir)
    for etype, target in file_errors:
        add_err(etype, target)

    # --- 2. Luật YOLO & Panoptic (Minh) ---
    manifest_path = delivery_dir / "manifest.json"
    panoptic_path = delivery_dir / "panoptic.json"

    if manifest_path.is_file() and panoptic_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))["items"]
        pan = json.loads(panoptic_path.read_text(encoding="utf-8"))
        valid_cats = {c["id"] for c in pan.get("categories", [])}
        anns = {a["image_id"]: a for a in pan.get("annotations", [])}
        imgs = {im["file_name"]: im for im in pan.get("images", [])}

        for stem, it in manifest.items():
            im_file_name = it["image"].split("/")[-1]
            im_info = imgs.get(im_file_name)
            w, h = (im_info["width"], im_info["height"]) if im_info else (640, 480)

            # Kiểm tra YOLO label
            lbl_path = delivery_dir / it["label"]
            yolo_errs = check_yolo_label(lbl_path, stem, w, h)
            for etype, target in yolo_errs:
                add_err(etype, target)

            # Kiểm tra Panoptic mask & annotations
            if im_info and im_info["id"] in anns:
                mask_path = delivery_dir / it["mask"]
                pan_errs = check_panoptic_ann(mask_path, stem, anns[im_info["id"]], valid_cats)
                for etype, target in pan_errs:
                    add_err(etype, target)

    # Xuất errors.json
    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_data = {"errors": all_errors}
    out_path.write_text(json.dumps(out_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[+] Đã phát hiện {len(all_errors)} lỗi luật. Ghi vào: {out_path}")

    # --- 3. Sinh Candidates (Vũ) nếu được yêu cầu ---
    if args.candidates:
        cand_path = Path(args.candidates).resolve()
        cand_path.parent.mkdir(parents=True, exist_ok=True)
        candidates = generate_candidates(delivery_dir)
        cand_path.write_text(json.dumps(candidates, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[+] Đã sinh {len(candidates)} ứng viên đối chiếu. Ghi vào: {cand_path}")


if __name__ == "__main__":
    main()
