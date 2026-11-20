#!/usr/bin/env python3
"""Tự động truy vết ticket của team AI ra trace.json cho Day 10 Lab.

Sử dụng:
  python scripts/trace_query.py --delivery delivery --out submission/de_an/trace.json
  hoặc:
  python scripts/trace_query.py --delivery runs/r7007/delivery --out runs/r7007/trace.json
"""
from __future__ import annotations
import argparse
import csv
import json
import re
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="Tự động sinh trace.json từ delivery")
    ap.add_argument("--delivery", default="delivery", help="Đường dẫn thư mục delivery")
    ap.add_argument("--out", required=True, help="Đường dẫn file trace.json ghi ra")
    args = ap.parse_args()

    delivery = Path(args.delivery)
    if not delivery.is_dir():
        raise SystemExit(f"Không tìm thấy thư mục delivery tại {delivery}")

    ticket_file = delivery / "incoming" / "ticket.md"
    changelog_file = delivery / "guideline" / "changelog.md"
    classes_file = delivery / "classes.txt"
    jobs_file = delivery / "jobs.csv"
    meta_file = delivery / "metadata.json"

    if not ticket_file.is_file():
        raise SystemExit(f"Thiếu file: {ticket_file}")

    # 1. Đọc ticket lấy các cảnh được báo
    ticket_txt = ticket_file.read_text(encoding="utf-8")
    reported_scenes = set(re.findall(r"scene_\d+", ticket_txt))

    # 2. Đọc classes.txt
    all_classes = {}
    for line in classes_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            parts = line.split(" ", 1)
            all_classes[parts[1].strip()] = int(parts[0])

    # 3. Đọc changelog để tìm lớp bị đổi quy tắc và guideline cũ
    cl_txt = changelog_file.read_text(encoding="utf-8")
    target_class = None
    for c in all_classes:
        if f"`{c}`" in cl_txt or f" {c} " in cl_txt or f" {c}:" in cl_txt or f"'{c}'" in cl_txt:
            target_class = c
            break

    if not target_class:
        # Tìm theo từ trong ticket nếu changelog không match
        for c in all_classes:
            if f"`{c}`" in ticket_txt or f" {c} " in ticket_txt:
                target_class = c
                break

    versions = re.findall(r"##\s*(v\d+\.\d+)", cl_txt)
    old_guideline = versions[-1] if len(versions) >= 2 else "v1.2"

    print(f"[*] Truy vết: Lớp bị đổi quy tắc = '{target_class}', Guideline cũ = '{old_guideline}'")
    print(f"[*] Cảnh báo trong ticket: {sorted(reported_scenes)}")

    # 4. Đọc jobs.csv để lấy danh sách job dùng guideline cũ
    with open(jobs_file, encoding="utf-8", newline="") as f:
        jobs = list(csv.DictReader(f))

    old_jobs = {j["job_id"]: j for j in jobs if j.get("guideline") == old_guideline}

    # 5. Đọc metadata.json
    meta_raw = json.loads(meta_file.read_text(encoding="utf-8"))["items"]
    meta = {it["image"]: it for it in meta_raw} if isinstance(meta_raw, list) else meta_raw

    # 6. Quét labels để tìm tier_a và tier_b
    cls_id = all_classes.get(target_class)
    tier_a = []
    tier_b = []
    notify_jobs = set()

    for stem, info in meta.items():
        job_id = info.get("job_id")
        if job_id not in old_jobs:
            continue
        lbl_file = delivery / "labels" / f"{stem}.txt"
        if not lbl_file.is_file():
            continue
        has_class = False
        for line in lbl_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and int(line.split()[0]) == cls_id:
                has_class = True
                break
        if has_class:
            notify_jobs.add(job_id)
            if info.get("scene_id") in reported_scenes:
                tier_a.append(stem)
            else:
                tier_b.append(stem)

    notify = sorted({old_jobs[j]["annotator"] for j in notify_jobs} | {old_jobs[j]["reviewer"] for j in notify_jobs})
    tier_a.sort()
    tier_b.sort()

    res = {
        "tier_a": tier_a,
        "tier_b": tier_b,
        "notify": notify,
    }

    out_p = Path(args.out)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
    print(f"[+] Đã ghi trace.json ra: {out_p}")
    print(f"    - Tier A: {len(tier_a)} ảnh")
    print(f"    - Tier B: {len(tier_b)} ảnh")
    print(f"    - Notify: {len(notify)} nhân sự ({', '.join(notify)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
