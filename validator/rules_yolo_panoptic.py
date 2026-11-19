"""Module kiểm tra lỗi luật YOLO và Panoptic cho Lab 10.
Phụ trách: Minh (Detection & Panoptic Rule Specialist)

Chỉ dùng thư viện chuẩn Python (chuẩn quy định RULES.md).
Được import scripts/pngutil.py để đọc mask PNG.
"""

from __future__ import annotations

import math
from pathlib import Path
import sys

# Hỗ trợ import pngutil từ thư mục scripts
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

try:
    import pngutil
except ImportError:
    pngutil = None


def check_yolo_label(
    label_path: Path,
    image_name: str,
    img_w: int = 640,
    img_h: int = 480,
) -> list[tuple[str, str]]:
    """Kiểm tra nhãn detection YOLO của một ảnh.
    
    Bắt 3 lỗi luật:
      1. invalid_class: class_id nằm ngoài khoảng 0-79
      2. bbox_out_of_bounds: tọa độ bounding box tràn viền ảnh
      3. duplicate_box: 2 box cùng class, cùng kích thước, chỉ lệch 1-2 pixel
    """
    errors: list[tuple[str, str]] = []
    if not label_path.is_file():
        return errors

    lines = [ln.strip() for ln in label_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        return errors

    boxes = []
    has_invalid_class = False
    has_oob = False

    for ln in lines:
        parts = ln.split()
        if len(parts) < 5:
            continue
        try:
            c = int(float(parts[0]))
            x, y, w, h = map(float, parts[1:5])
        except ValueError:
            continue

        # 1. Luật invalid_class: 80 lớp COCO có ID từ 0 đến 79
        if not (0 <= c < 80):
            if not has_invalid_class:
                errors.append(("invalid_class", image_name))
                has_invalid_class = True

        # 2. Luật bbox_out_of_bounds: tràn mép ngoài ảnh
        # YOLO: x, y là tâm; w, h là bề rộng, bề cao (chuẩn hóa 0-1)
        x_min = x - w / 2.0
        y_min = y - h / 2.0
        x_max = x + w / 2.0
        y_max = y + h / 2.0

        # Cho phép sai số số thực nhỏ (0.005), tràn mép thật trong đề thường >= 0.02
        if x_min < -0.005 or y_min < -0.005 or x_max > 1.005 or y_max > 1.005:
            if not has_oob:
                errors.append(("bbox_out_of_bounds", image_name))
                has_oob = True

        boxes.append((c, x, y, w, h))

    # 3. Luật duplicate_box: cặp box cùng lớp, cùng kích thước, chỉ lệch 1-2 pixel
    has_dup = False
    n = len(boxes)
    for i in range(n):
        if has_dup:
            break
        c1, x1, y1, w1, h1 = boxes[i]
        for j in range(i + 1, n):
            c2, x2, y2, w2, h2 = boxes[j]
            if c1 != c2:
                continue

            # Kích thước phải giống hệt nhau (hoặc sai số < 1e-4)
            if abs(w1 - w2) > 1e-4 or abs(h1 - h2) > 1e-4:
                continue

            # Độ lệch tâm tính theo pixel
            dx_px = abs(x1 - x2) * img_w
            dy_px = abs(y1 - y2) * img_h

            # Lệch 1-2 pixel (cho biên độ tới 3.5 pixel để bao trọn) và không phải trùng hoàn toàn
            if 0 < max(dx_px, dy_px) <= 3.5:
                errors.append(("duplicate_box", image_name))
                has_dup = True
                break

    return errors


def check_panoptic_ann(
    mask_path: Path,
    image_name: str,
    ann: dict,
    valid_category_ids: set[int],
) -> list[tuple[str, str]]:
    """Kiểm tra nhãn Panoptic của một ảnh.
    
    Bắt 2 lỗi luật:
      1. invalid_category_id: category_id không có trong categories của panoptic.json
      2. thing_overlap: area khai báo nhiều hơn số pixel thực tế của segment trong mask PNG
    """
    errors: list[tuple[str, str]] = []
    segments = ann.get("segments_info", [])
    if not segments:
        return errors

    # 1. Luật invalid_category_id
    has_invalid_cat = False
    for seg in segments:
        cat_id = seg.get("category_id")
        if cat_id not in valid_category_ids:
            if not has_invalid_cat:
                errors.append(("invalid_category_id", image_name))
                has_invalid_cat = True
                break

    # 2. Luật thing_overlap (bị segment khác đè lên)
    if mask_path.is_file() and pngutil is not None:
        try:
            width, height, pixels = pngutil.read_rgb(mask_path)
            # Đếm số pixel của từng segment ID
            # Segment ID = R + G * 256 + B * 65536
            actual_counts: dict[int, int] = {}
            for i in range(0, len(pixels), 3):
                sid = pngutil.segment_id(pixels, i)
                if sid != 0:  # Bỏ qua id 0 (nền)
                    actual_counts[sid] = actual_counts.get(sid, 0) + 1

            for seg in segments:
                # Chỉ kiểm tra các segment không phải crowd
                if seg.get("iscrowd"):
                    continue
                sid = seg["id"]
                declared_area = seg.get("area", 0)
                actual_px = actual_counts.get(sid, 0)

                # Khi bị thing_overlap, kẻ cắp lấy 15%-30% pixel, nhưng declared_area của donor không đổi
                # Do đó declared_area > actual_px đáng kể
                diff = declared_area - actual_px
                if diff >= 5 and (diff / max(declared_area, 1)) >= 0.10:
                    errors.append(("thing_overlap", image_name))
                    break
        except Exception:
            pass

    return errors
