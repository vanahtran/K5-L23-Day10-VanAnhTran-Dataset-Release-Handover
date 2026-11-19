"""Công cụ xem ảnh trực quan cho nhóm Day 10 Lab.
Vẽ Bounding Box YOLO (xanh lá) và nhãn lớp lên ảnh để cả nhóm mở xem cực nhanh.
Chạy: python scripts/view_candidates.py --run runs/r7007
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw


def main() -> None:
    ap = argparse.ArgumentParser(description="Vẽ bounding box và nhãn để review nhanh")
    ap.add_argument("--run", required=True, help="Thư mục run, ví dụ runs/r7007 hoặc submission/de_an")
    args = ap.parse_args()

    run_dir = Path(args.run)
    delivery = run_dir / "delivery" if (run_dir / "delivery").is_dir() else run_dir.parent / "delivery"
    if not delivery.is_dir():
        delivery = Path("delivery")

    cand_file = run_dir / "candidates.json"
    if not cand_file.is_file():
        print(f"Chưa có file {cand_file}. Hãy chạy validator --candidates trước!")
        return

    cands = json.loads(cand_file.read_text(encoding="utf-8"))
    out_dir = run_dir / "visualized_candidates"
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_p = delivery / "manifest.json"
    classes_p = delivery / "classes.txt"
    if not (manifest_p.is_file() and classes_p.is_file()):
        print(f"Không tìm thấy manifest.json hoặc classes.txt trong {delivery}")
        return

    manifest = json.loads(manifest_p.read_text(encoding="utf-8"))["items"]
    classes_80 = [ln.split(" ", 1)[1].strip() for ln in classes_p.read_text(encoding="utf-8").splitlines()]

    print(f"Đang vẽ {len(cands)} ảnh ứng viên ra thư mục: {out_dir} ...")

    for item in cands:
        stem = item.get("image") or item.get("target")
        if not stem or stem not in manifest:
            continue

        img_p = delivery / manifest[stem]["image"]
        lbl_p = delivery / manifest[stem]["label"]

        if not img_p.is_file():
            continue

        img = Image.open(img_p).convert("RGB")
        draw = ImageDraw.Draw(img)
        w_img, h_img = img.size

        # Vẽ box YOLO (Màu xanh lá)
        if lbl_p.is_file():
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
                    draw.rectangle([x1, y1, x2, y2], outline="lime", width=3)
                    draw.text((x1 + 3, y1 + 3), f"YOLO: {cname}", fill="lime")

        tag = item.get("type", "candidate")
        out_file = out_dir / f"{stem}_{tag}.jpg"
        img.save(out_file)

    print(f"==> Xong! Toàn bộ ảnh đã được lưu tại: {out_dir}")
    print("5 thành viên có thể mở thư mục này để lướt xem ảnh bằng mắt và chốt verdict!")


if __name__ == "__main__":
    main()
