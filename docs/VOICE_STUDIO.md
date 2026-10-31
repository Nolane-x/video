# Voice Studio integration

The video repo consumes the pinned user fork of VoiceStudio as an independent
application submodule. The adapter contract, optional provider integrations,
voice casting manifests and H2 handoff live in
[integrations/voice-studio/README.md](../integrations/voice-studio/README.md).

Do not add model weights, reference recordings, API keys, cloned human voices,
or generated audio to Git. Use the external VoiceStudio model cache and local
secret stores. Asset-library acquisition remains a separate completed workstream.
