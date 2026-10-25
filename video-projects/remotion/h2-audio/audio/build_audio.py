"""Generate the H2 procedural audio beds and SFX locally or in CI."""
import glob, os, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
extra = sorted(glob.glob(os.path.join(os.path.dirname(D), "packs", "*", "audio.py")))
for f in [os.path.join(D, "synth.py"), os.path.join(D, "music.py")] + extra:
    print(">>", os.path.relpath(f, os.path.dirname(D)), flush=True)
    r = subprocess.run([sys.executable, f], cwd=D)
    if r.returncode:
        raise SystemExit("Audio generation failed at " + f)
print("H2 music/SFX generation complete.")
