# Curiefuel — Claude Code Global Instructions

## THE MOST IMPORTANT RULE
ALWAYS build in the current working directory.
NEVER create a subfolder that wraps the entire project.
Before writing ANY file, run `pwd` and confirm you are in the correct root.
After writing ANY file, run `ls -la` and confirm it appears at root.

If you find yourself about to write `mkdir curiefuel-oss` or 
`mkdir fsp-thermal-model` or ANY top-level project wrapper — STOP.
The current directory IS the project. Build here.

## Pre-flight checklist — run before every session
1. `pwd` — confirm location
2. `ls -la` — confirm existing files
3. `cat .claude/CLAUDE.md` — confirm instructions loaded
4. Only then start writing files

## Project structure — all files go directly here:
- `README.md`
- `setup.py`
- `requirements.txt`
- `LICENSE`
- `.gitignore`
- Source package folder (e.g. `fsp_thermal/`, `lunar_grid/`)
- `examples/`
- `tests/`
- `docs/`

Never create a folder above these. The repo root IS the project root.

## Git rules
Never commit:
- `node_modules/`
- `.next/`
- `__pycache__/`
- `*.pyc`
- `.env`
- `dist/`
- `*.egg-info/`

Always confirm `.gitignore` contains all of the above before first commit.

## Python rules
- Always use `pip install --break-system-packages`
- Python 3.10+ only
- No virtual environments unless explicitly asked
- All imports must be tested by running the example files
- Fix all import errors before reporting done
