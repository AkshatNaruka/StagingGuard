#!/bin/sh
set -eu

task_sdk_commit=f4fcd2fe476f0c4dcf800e498530b7042b830f6b
command -v git >/dev/null
command -v uv >/dev/null
mkdir -p .local
if [ ! -d .local/agntid-python/.git ]; then
  git clone --no-checkout --filter=blob:none https://github.com/AGNTID-AI/agntid-python.git .local/agntid-python
  git -C .local/agntid-python checkout "$task_sdk_commit"
fi
if [ "$(git -C .local/agntid-python rev-parse HEAD)" != "$task_sdk_commit" ]; then
  echo 'SDK checkout differs from the reviewed source. Inspect it before changing versions.' >&2
  exit 1
fi
if [ ! -d .local/agntid-venv ]; then
  uv venv --python 3.11 .local/agntid-venv
fi
uv pip install --python .local/agntid-venv/bin/python -e .local/agntid-python
.local/agntid-venv/bin/python -c "import agntid; from importlib.metadata import version; print('AgntID SDK installed:', version('agntid-sdk'))"
