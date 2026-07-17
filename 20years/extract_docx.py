#!/usr/bin/env python3
"""Extract text paragraphs and images from the two 20-year retrospective docx files,
preserving their original order, and save images to 20years/img_cn/ and 20years/img_en/."""
import os
import json
from docx import Document
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

ROOT = "/Users/mellen/Desktop/nanosynthesis.github.io"
JOBS = [
    ("zh", "20years/建组20年回顾-中文版.docx", "20years/img_cn"),
    ("en", "20years/建组20年回顾-英文版.docx", "20years/img_en"),
]


def extract(lang, docx_path, img_dir):
    doc = Document(docx_path)
    body = doc.element.body
    os.makedirs(os.path.join(ROOT, img_dir), exist_ok=True)

    # Map rId -> image part
    rels = doc.part.related_parts

    items = []
    img_idx = 0
    para_idx = 0
    for child in body.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag != "p":
            continue
        # Collect text
        text_parts = []
        for t in child.iter(qn("w:t")):
            text_parts.append(t.text or "")
        text = "".join(text_parts)
        # Detect drawings (inline images)
        drawings = child.findall(".//" + qn("w:drawing"))
        picts = child.findall(".//" + qn("w:pict"))
        # Paragraph-level properties (alignment, indent)
        pPr = child.find(qn("w:pPr"))
        align = None
        first_line = None
        left_indent = None
        if pPr is not None:
            jc = pPr.find(qn("w:jc"))
            if jc is not None:
                align = jc.get(qn("w:val"))
            indEl = pPr.find(qn("w:ind"))
            if indEl is not None:
                first_line = indEl.get(qn("w:firstLine"))
                left_indent = indEl.get(qn("w:left"))

        if drawings or picts:
            # Find blip with rId
            blips = child.findall(".//" + qn("a:blip"))
            for blip in blips:
                rId = blip.get(qn("r:embed"))
                if not rId:
                    continue
                part = rels.get(rId)
                if part is None:
                    continue
                img_idx += 1
                ext = part.partname.ext.lower() if hasattr(part.partname, "ext") else ".png"
                if not ext.startswith("."):
                    ext = "." + ext
                # Normalize extension
                if ext not in (".png", ".jpg", ".jpeg", ".gif", ".bmp"):
                    ext = ".png"
                fname = f"{img_idx:02d}{ext}"
                out_path = os.path.join(ROOT, img_dir, fname)
                with open(out_path, "wb") as f:
                    f.write(part.blob)
                # Get extent (cx, cy in EMU)
                extent = child.find(".//" + qn("wp:extent"))
                width_in = height_in = None
                if extent is not None:
                    cx = int(extent.get("cx", 0))
                    cy = int(extent.get("cy", 0))
                    width_in = round(cx / 914400, 2)
                    height_in = round(cy / 914400, 2)
                items.append({
                    "type": "img",
                    "idx": img_idx,
                    "src": f"{img_dir}/{fname}",
                    "width_in": width_in,
                    "height_in": height_in,
                })
            # If the same paragraph also has text (rare), append it as a separate paragraph item
            if text.strip():
                para_idx += 1
                items.append({
                    "type": "para",
                    "idx": para_idx,
                    "text": text.strip(),
                    "align": align,
                    "first_line": first_line,
                    "left_indent": left_indent,
                })
        else:
            if text.strip():
                para_idx += 1
                items.append({
                    "type": "para",
                    "idx": para_idx,
                    "text": text.strip(),
                    "align": align,
                    "first_line": first_line,
                    "left_indent": left_indent,
                })
    return items


def main():
    summary = {}
    for lang, docx_rel, img_dir_rel in JOBS:
        docx_path = os.path.join(ROOT, docx_rel)
        print(f"Extracting {docx_path} -> {img_dir_rel}")
        items = extract(lang, docx_path, img_dir_rel)
        summary[lang] = items
        # Save JSON for downstream HTML generation
        out_json = os.path.join(ROOT, f"20years/extract_{lang}.json")
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        n_para = sum(1 for it in items if it["type"] == "para")
        n_img = sum(1 for it in items if it["type"] == "img")
        print(f"  paragraphs: {n_para}, images: {n_img}, total items: {len(items)}")
        print(f"  saved json: {out_json}")
    print("Done.")


if __name__ == "__main__":
    main()
