"""Module đối chiếu Detection (YOLO) <-> Panoptic (COCO) và sinh candidates.json
Tác giả: Vũ (Cross-check Specialist)
"""
from __future__ import annotations
import json
from pathlib import Path
import sys

# Cho phép import pngutil từ thư mục scripts
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import pngutil


def box_iou(b1: list[float], b2: list[float]) -> float:
    # b: [x1, y1, x2, y2]
    ix1, iy1 = max(b1[0], b2[0]), max(b1[1], b2[1])
    ix2, iy2 = min(b1[2], b2[2]), min(b1[3], b2[3])
    inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    if inter == 0.0:
        return 0.0
    a1 = (b1[2] - b1[0]) * (b1[3] - b1[1])
    a2 = (b2[2] - b2[0]) * (b2[3] - b2[1])
    union = a1 + a2 - inter
    return inter / union if union > 0 else 0.0


def generate_candidates(delivery_dir: Path) -> list[dict]:
    d = Path(delivery_dir)
    manifest = json.loads((d / "manifest.json").read_text(encoding="utf-8"))["items"]
    pan = json.loads((d / "panoptic.json").read_text(encoding="utf-8"))

    # Map class index YOLO (0..79) -> class_name
    classes_80 = [ln.split(" ", 1)[1].strip() for ln in (d / "classes.txt").read_text(encoding="utf-8").splitlines()]
    # Map panoptic category_id -> dict
    cat_by_id = {c["id"]: c for c in pan["categories"]}
    # Map panoptic annotation by file_name
    pan_by_stem = {Path(a["file_name"]).stem: a for a in pan["annotations"]}

    candidates = []

    for stem, it in manifest.items():
        img_p = d / it["image"]
        lbl_p = d / it["label"]
        msk_p = d / it["mask"]

        if not (lbl_p.is_file() and msk_p.is_file()):
            continue

        pan_ann = pan_by_stem.get(stem)
        if not pan_ann:
            continue

        # 1. Đọc kích thước ảnh từ mask PNG
        try:
            w_img, h_img, _ = pngutil.read_rgb(msk_p)
        except Exception:
            continue

        # 2. Đọc nhãn YOLO: class_id, x1, y1, x2, y2 (pixel)
        yolo_boxes = []
        for line in lbl_p.read_text(encoding="utf-8").splitlines():
            parts = line.strip().split()
            if len(parts) >= 5:
                cid = int(float(parts[0]))
                xc, yc, w, h = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
                x1 = (xc - w / 2) * w_img
                y1 = (yc - h / 2) * h_img
                x2 = (xc + w / 2) * w_img
                y2 = (yc + h / 2) * h_img
                cname = classes_80[cid] if 0 <= cid < 80 else str(cid)
                yolo_boxes.append({"class_id": cid, "class_name": cname, "bbox": [x1, y1, x2, y2], "area": w * h * w_img * h_img})

        # 3. Lọc danh sách Panoptic segments (chỉ lấy isthing, bỏ iscrowd)
        pan_segments = []
        for seg in pan_ann.get("segments_info", []):
            cat = cat_by_id.get(seg["category_id"])
            if not cat or not cat.get("isthing") or seg.get("iscrowd"):
                continue
            sx, sy, sw, sh = seg["bbox"]
            pan_segments.append({
                "id": seg["id"],
                "category_id": seg["category_id"],
                "class_name": cat["name"],
                "bbox": [sx, sy, sx + sw, sy + sh],
                "area": seg["area"]
            })

        matched_segs = set()
        matched_boxes = set()

        # 4. Đối chiếu cặp Box - Segment
        for bi, b in enumerate(yolo_boxes):
            best_iou = 0.0
            best_si = -1
            for si, s in enumerate(pan_segments):
                iou = box_iou(b["bbox"], s["bbox"])
                if iou > best_iou:
                    best_iou = iou
                    best_si = si

            if best_si >= 0 and best_iou > 0.4:
                s = pan_segments[best_si]
                # Kiểm tra LỆCH LỚP (class_swap hoặc category_swap)
                if b["class_name"] != s["class_name"]:
                    candidates.append({
                        "image": stem,
                        "type": "class_swap",
                        "hint": f"YOLO={b['class_name']} vs Panoptic={s['class_name']} (IoU={best_iou:.2f})"
                    })
                    matched_boxes.add(bi)
                    matched_segs.add(best_si)
                elif best_iou > 0.6:
                    matched_boxes.add(bi)
                    matched_segs.add(best_si)
            elif 0.15 <= best_iou <= 0.4:
                # Kiểm tra BBOX DRIFT (box bị lệch, cùng lớp)
                s = pan_segments[best_si]
                if b["class_name"] == s["class_name"]:
                    candidates.append({
                        "image": stem,
                        "type": "bbox_drift",
                        "hint": f"Box lệch: {b['class_name']} IoU={best_iou:.2f}"
                    })
                    matched_boxes.add(bi)
                    matched_segs.add(best_si)

        # 5. Kiểm tra MISSING BOX (segment panoptic lớn nhưng không có box yolo tương ứng)
        for si, s in enumerate(pan_segments):
            if si not in matched_segs and s["area"] > 2500:
                candidates.append({
                    "image": stem,
                    "type": "missing_box",
                    "hint": f"Panoptic có {s['class_name']} (area={s['area']}) nhưng YOLO thiếu box"
                })

        # 6. Kiểm tra INSTANCE MERGE (1 segment phủ lên 2 box YOLO cùng lớp)
        for si, s in enumerate(pan_segments):
            overlaps = [b for b in yolo_boxes if b["class_name"] == s["class_name"] and box_iou(b["bbox"], s["bbox"]) > 0.35]
            if len(overlaps) >= 2:
                candidates.append({
                    "image": stem,
                    "type": "instance_merge",
                    "hint": f"1 mask {s['class_name']} phủ 2 box YOLO"
                })

    # Khử trùng lặp ảnh trong candidates
    unique_candidates = []
    seen = set()
    for c in candidates:
        key = (c["image"], c["type"])
        if key not in seen:
            seen.add(key)
            unique_candidates.append(c)

    return unique_candidates
