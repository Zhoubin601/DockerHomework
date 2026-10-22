"""Read-only independent OOXML/provenance audit; writes only a JSON in docs/v5-work."""
from pathlib import Path
from collections import Counter
from lxml import etree as ET
import hashlib
import json
import posixpath
import sys
from urllib.parse import unquote
from zipfile import ZipFile

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
N = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    path = Path(sys.argv[1]).resolve()
    source_dirs = [
        ROOT / "docs/docker-evidence",
        ROOT / "docs/v3-evidence",
        ROOT / "docs/local-test-20261022/docker-roundtrip",
    ]
    source_map = {}
    for directory in source_dirs:
        for image in directory.glob("*.png"):
            source_map.setdefault(sha(image.read_bytes()), []).append(str(image.relative_to(ROOT)))

    with ZipFile(ROOT / "output/v4/20261021-docker-lab-report-v4.docx") as old:
        old_media = Counter(sha(old.read(x)) for x in old.namelist() if x.startswith("word/media/"))

    with ZipFile(path) as z:
        names = set(z.namelist())
        report = {"path": str(path), "sha256": sha(path.read_bytes()), "crcError": z.testzip()}
        xml_errors = []
        rel_errors = []
        for name in names:
            if not name.endswith((".xml", ".rels")):
                continue
            try:
                part = ET.fromstring(z.read(name))
            except Exception as exc:
                xml_errors.append({"part": name, "error": str(exc)})
                continue
            if name.endswith(".rels"):
                base = posixpath.dirname(posixpath.dirname(name)) if "/_rels/" in name else ""
                for relationship in part:
                    if relationship.get("TargetMode") == "External":
                        continue
                    target = unquote(relationship.get("Target", "").split("#", 1)[0])
                    target = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join(base, target))
                    if target and target not in names:
                        rel_errors.append({"part": name, "target": target})
        report["xmlErrors"] = xml_errors
        report["missingRelationshipTargets"] = rel_errors

        media = {name: sha(z.read(name)) for name in names if name.startswith("word/media/")}
        retained = Counter(media.values())
        report["historicalMediaMissing"] = list((old_media - retained).elements())
        report["media"] = [{"part": name, "sha256": digest, "source": source_map.get(digest, [])} for name, digest in sorted(media.items())]
        doc = ET.fromstring(z.read("word/document.xml"))
        report["inlineImageCount"] = len(doc.xpath(".//a:blip", namespaces=N))
        report["tableCount"] = len(doc.xpath("./w:body/w:tbl", namespaces=N))
        report["bodyFields"] = doc.xpath(".//w:instrText/text()", namespaces=N)
        report["headerFooterFields"] = {
            name: ET.fromstring(z.read(name)).xpath(".//w:instrText/text()", namespaces=N)
            for name in names if name.startswith(("word/header", "word/footer")) and name.endswith(".xml")
        }
        report["revisionCount"] = len(doc.xpath(".//w:ins | .//w:del | .//w:moveFrom | .//w:moveTo", namespaces=N))
        report["crops"] = [dict(x.attrib) for x in doc.xpath(".//a:srcRect", namespaces=N)]
        text = "\n".join("".join(p.xpath(".//w:t/text()", namespaces=N)) for p in doc.xpath(".//w:p", namespaces=N))
        keys = ["6085", "localtest-20261022", "18087", "15086", "9271", "91b23f11f6da", "cdb872c45267", "1333c043c6b02570c3df12afaa82559359e459bcdd58a69e30ec88a01da2ac38"]
        report["expectedLocalEvidenceKeys"] = {key: key in text for key in keys}
        report["unresolvedMarkerLines"] = [line for line in text.splitlines() if any(marker in line for marker in ["待确认：", "TODO", "TBD", "lorem ipsum", "{{"])]

    output = ROOT / "docs/v5-work/independent-docx-audit.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "media"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
