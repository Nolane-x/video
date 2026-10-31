# HyperFrames proof lane

This lane demonstrates that the pinned HyperFrames CLI can scaffold, lint, render and snapshot a small HTML video on a CPU-only GitHub Actions runner. It uses the built-in \`warm-grain\` example so it does not pull from the separately managed asset/audio library.

Run \`.github/workflows/video-toolchain-hyperframes-proof.yml\` manually. The generated project and final MP4 are runner-local; only the proof MP4, lint JSON, ffprobe metadata and key-frame snapshots are uploaded as a short-lived Actions artifact.

For a real film, create the composition in the project folder dedicated to that film, define exact shot and caption timing, then use the same CLI commands after the visual proof is reviewed.
