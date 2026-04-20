from pathlib import Path
import argparse

dirs = [
    "docs",
    "harness/src/invariant_harness/models",
    "harness/src/invariant_harness/runners",
    "harness/src/invariant_harness/cases",
    "harness/results",
    "harness/examples/vulnerable_app",
]

files = [
    "README.md",
    "docs/whitepaper.md",
    "harness/pyproject.toml",
    "harness/requirements.txt",
    "harness/.env.example",
    "harness/run_case.py",
    "harness/src/invariant_harness/__init__.py",
    "harness/src/invariant_harness/config.py",
    "harness/src/invariant_harness/types.py",
    "harness/src/invariant_harness/result_store.py",
    "harness/src/invariant_harness/case_registry.py",
    "harness/src/invariant_harness/models/__init__.py",
    "harness/src/invariant_harness/models/base.py",
    "harness/src/invariant_harness/models/openai_adapter.py",
    "harness/src/invariant_harness/models/mock_adapter.py",
    "harness/src/invariant_harness/runners/__init__.py",
    "harness/src/invariant_harness/runners/simple_runner.py",
    "harness/src/invariant_harness/cases/__init__.py",
    "harness/src/invariant_harness/cases/base.py",
    "harness/src/invariant_harness/cases/direct_override_case.py",
    "harness/src/invariant_harness/cases/prompt_leakage_case.py",
    "harness/results/.gitkeep",
]

def create_structure(base: Path) -> None:
    base = base.resolve()

    for d in dirs:
        (base / d).mkdir(parents=True, exist_ok=True)
        
    print    


    for f in files:
        path = base / f
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        
    print        


    print(f"Structure created under: {base}")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create the invariant harness directory structure in a specified directory."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Base directory where the structure should be created (default: current directory)",
    )
    args = parser.parse_args()

    create_structure(Path(args.target))

if __name__ == "__main__":
    main()