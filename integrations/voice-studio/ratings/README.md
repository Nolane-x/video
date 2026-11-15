# Human voice ratings

This folder is the optional hand-off location for listener ratings exported by
`voice-audition-all-scripts.html` from a completed GitHub Actions artifact.

## Workflow

1. Download/open the benchmark artifact from the completed
   **Voice Studio Actions CPU lab** run.
2. Open `voice-audition-all-scripts.html`, listen to every full sample under
   each anonymous candidate, enter only ratings you personally reviewed, and
   export `voice-human-ratings-all-scripts.json`.
3. Review the JSON before committing it here. The Actions shortlist workflow
   expects the exported JSON schema and candidate labels without renaming them.
4. Open **Actions → Voice Studio Actions human shortlist**. Supply the source
   benchmark run ID, exact artifact name (for example
   `nolane-voice-actions-lab-12`), and path
   `integrations/voice-studio/ratings/voice-human-ratings-all-scripts.json`.
5. Download the generated JSON/Markdown shortlist artifact from that Actions
   run. The workflow joins listener ratings to the voice identity map from the
   original benchmark artifact.

## Privacy and evidence

This repository is public. Any ratings file committed here, including its
written listener notes, should be treated as public. Keep notes factual and
non-identifying. Do not add a person's private details, raw/reference audio,
voice-cloning consent documents, model weights, API keys or other credentials.

Do not invent ratings or pre-fill scores to make a candidate rank higher. Leave
unheard or unreviewed dimensions empty. The shortlist only reports human
preferences and technical eligibility for these scripts and model revisions;
it is not an objective naturalness score or an ElevenLabs-equivalence claim.
