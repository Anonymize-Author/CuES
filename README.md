A lightweight, modular pipeline for three-stage agent data generation:
- Stage 1: Triplet generation (environment exploration)
- Stage 2: Task abstraction (derive tasks and queries)
- Stage 3: Trajectory generation (execute tasks and record messages)
- Optional: Query Rewrite (rewrite queries using Stage 3 trajectory context)

## Features
- Pluggable environment managers (AppWorld, BFCL, WebShop via EnvService)
- Persistent storage with per-stage outputs
- Threaded execution for higher throughput
- Deterministic JSON schemas per stage
- Query Rewrite to mirror Stage 3 JSON and diversify training data

## Quickstart

1) Requirements
- Python 3.10+
- Access to Aliyun DashScope API
- EnvService if using external simulated environments (AppWorld/BFCL/WebShop)

2) Installation
- Create and activate a virtual environment
- Install dependencies (adapt to your environment):
  - pip install -r requirements.txt (if provided)
  - or pip install pyyaml requests
- Export your DashScope key:
  - export DASHSCOPE_API_KEY=... (or set in config.yaml)

3) Configuration
See `config/config.yaml` for full options. Key sections:
- api: DashScope model, temperature, max tokens
- environment: type and EnvService endpoint
- stage1/stage2/stage3: knobs per stage
- threading: worker pool settings
- logging: level and file path
- rewrite: Query Rewrite settings

4) Run
- All stages:  python main.py --stage all --config config/config.yaml
- Stage 1:     python main.py --stage stage1
- Stage 2:     python main.py --stage stage2 --input-file ./data/triplets/*.jsonl (latest auto-selected if omitted)
- Stage 3:     python main.py --stage stage3 --input-file ./data/tasks/*.jsonl (latest auto-selected if omitted)
- Enable rewrite after stage 3: add --rewrite (alias: --query-rewrite)

Outputs are written to `./data/`:
- data/triplets/*.jsonl
- data/tasks/*.jsonl
- data/trajectories/trajectory_*.json
- data/trajectories/failed_tasks/*.json
- data/rewrites/trajectories/trajectory_*_rw*.json

## Run with EnvService (AppWorld)

Use the bundled EnvService scripts to bring up the AppWorld environment, then run the pipeline:

1) Prepare environment with conda
- Ensure conda is installed and available in your shell:
  - source $(conda info --base)/etc/profile.d/conda.sh

2) Install AppWorld environment via setup script
- cd env_service/environments/appworld
- bash setup.sh

3) Launch EnvService for AppWorld (in a separate terminal)
- cd env_service/launch_script
- bash appworld.sh

4) Configure Client (optional)
- In `config/config.yaml`, set:
  - environment.type: appworld
  - environment.envservice.server_url: http://127.0.0.1:8080

5) Start synthesis
- From the repo root (CuES/):
  - python main.py --stage all --config config/config.yaml

Notes
- You can override `APPWORLD_ROOT` before launching to point to an existing AppWorld data directory.
- If EnvService runs on another host/port, update `server_url` accordingly.

## CLI
- --config: path to config file (default: config/config.yaml)
- --stage: all | stage1 | stage2 | stage3
- --session-name: label for the run
- --input-file: input for stage2/stage3
- --verbose: verbose logging
- --requirement: exploration requirement for stage1
- --extract: extract concept set from env (optional)
- --rewrite | --query-rewrite: run Query Rewrite after Stage 3

## main() flow
1. Load config and validate API key
2. If AppWorld is selected, probe EnvService
3. Build pipeline and run selected stage(s)
4. Save outputs and stats
5. If rewrite is enabled, run Query Rewrite over Stage 3 outputs

## Query Rewrite
- Purpose: produce multiple semantically equivalent variants for each task query while keeping the exact Stage 3 JSON structure.
- Input: a directory of `trajectory_*.json` or a single file.
- Output: per-file JSONs under `data/rewrites/trajectories/`, named `trajectory_<task_id>_rw<i>.json`.
- Method: summarize `messages` context and prompt the LLM to rewrite the `query` into up to K variants.
- Config:
  - rewrite.batch_size: default 10
  - rewrite.num_variants: default 3
- CLI: pass --rewrite or --query-rewrite with --stage all (after stage 3) or run independently by calling the pipeline API.

## Development notes
- Code layout:
  - agents/: LLM action planner and evaluator
  - core/: API client, memory manager, pipeline
  - data/: pydantic-like models and storage helpers
  - envs/: EnvService managers (AppWorld, BFCL, WebShop)
  - environment/: legacy base abstractions
  - prompts/: all prompt builders and parsers
  - stages/: Stage 1/2/3 implementations
  - utils/: logger and config utilities
- Trajectories store both metadata and `messages` for downstream use.
- Query Rewrite preserves all keys and only changes `query`.

## Troubleshooting
- EnvService import errors: ensure EnvService is available in PYTHONPATH or run from the repo root where EnvService exists.
- Missing API key: set `api.dashscope_api_key` in `config.yaml` or environment variable.
- Empty outputs: check logs in `./logs/agentflow.log` and lower thresholds.
