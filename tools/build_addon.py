#!/usr/bin/env python3
"""
One-command build for the Greek Temple Decorations Bedrock addon.

Steps:
  1. Generates all marble texture PNGs (calls generate_textures).
  2. Zips the behavior pack and resource pack together into a single
     distributable .mcaddon file.

Usage:  python tools/build_addon.py
(Windows users may also double-click tools/build_mcaddon.bat)
"""
import os
import shutil
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BP = os.path.join(ROOT, "GreekTemple_BP")
RP = os.path.join(ROOT, "GreekTemple_RP")
OUT_DIR = os.path.join(ROOT, "build")
ADDON = os.path.join(OUT_DIR, "GreekTemple.mcaddon")


def generate_textures():
    script = os.path.join(ROOT, "tools", "generate_textures.py")
    print("== Generating marble textures ==")
    subprocess.run([sys.executable, script], check=True)


def zipdir(src, zf, arcname):
    for root, _dirs, files in os.walk(src):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, os.path.dirname(src))
            zf.write(full, os.path.join(arcname, rel))


def build():
    os.makedirs(OUT_DIR, exist_ok=True)

    # Create the two .mcpack files, then combine into .mcaddon
    bp_pack = os.path.join(OUT_DIR, "GreekTemple_BP.mcpack")
    rp_pack = os.path.join(OUT_DIR, "GreekTemple_RP.mcpack")
    for pack, target in ((BP, bp_pack), (RP, rp_pack)):
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
            zipdir(pack, zf, "")
        print("packed", target)

    with zipfile.ZipFile(ADDON, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(bp_pack, "GreekTemple_BP.mcpack")
        zf.write(rp_pack, "GreekTemple_RP.mcpack")
    print("addon written to", ADDON)
    print("Import GreekTemple.mcaddon into Minecraft Bedrock.")


if __name__ == "__main__":
    generate_textures()
    build()
