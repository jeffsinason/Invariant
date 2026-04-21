import argparse

from invariant_harness.benchmark import build_benchmark_report
from invariant_harness.case_registry import CASE_REGISTRY
from invariant_harness.models import load_model
from invariant_harness.result_store import save_benchmark_report
from invariant_harness.runners.batch_runner import BatchRunner


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a benchmark matrix across harness cases.")
    parser.add_argument(
        "--provider",
        default=None,
        help="Model provider to use, e.g. mock, openai, or anthropic",
    )
    parser.add_argument(
        "--model",
        dest="model_name",
        default=None,
        help="Model name to use for the benchmark run",
    )
    parser.add_argument(
        "--cases",
        default="all",
        help="Comma-separated case list or 'all'",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Do not save per-case results or the benchmark report",
    )

    args = parser.parse_args()

    if args.cases == "all":
        case_names = list(CASE_REGISTRY.keys())
    else:
        case_names = [name.strip() for name in args.cases.split(",") if name.strip()]

    try:
        model = load_model(provider=args.provider, model_name=args.model_name)
        runner = BatchRunner(model=model)
        results, saved_paths = runner.run(case_names, save=not args.no_save)
    except (RuntimeError, ValueError) as exc:
        parser.exit(status=1, message=f"error: {exc}\n")

    report = build_benchmark_report(
        provider=results[0].provider,
        model_name=results[0].model_name,
        results=results,
    )

    report_path = None
    if not args.no_save:
        report_path = str(
            save_benchmark_report(
                report,
                provider=results[0].provider,
                model_name=results[0].model_name,
            )
        )

    print("\n=== BENCHMARK MATRIX ===")
    print(f"provider:    {report['provider']}")
    print(f"model_name:  {report['model_name']}")
    print(f"total_cases: {report['summary']['total_cases']}")
    print(f"vulnerable:  {report['summary']['vulnerable_cases']}")
    print(f"safe:        {report['summary']['safe_cases']}")
    print(f"cases:       {[item['case_name'] for item in report['results']]}")
    if saved_paths:
        print(f"saved_cases:  {len(saved_paths)}")
    if report_path:
        print(f"saved_to:    {report_path}")


if __name__ == "__main__":
    main()
