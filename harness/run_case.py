import argparse

from invariant_harness.models import DEFAULT_MODEL_NAMES, load_model
from invariant_harness.result_store import save_error_result
from invariant_harness.runners.simple_runner import SimpleRunner


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a prompt injection test case.")
    parser.add_argument("case_name", help="Case to run, e.g. direct_override")
    parser.add_argument(
        "--provider",
        default=None,
        help="Model provider to use, e.g. mock or openai",
    )
    parser.add_argument(
        "--model",
        dest="model_name",
        default=None,
        help="Model name to use, e.g. mock-v1 or gpt-4.1-mini",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Do not save the result JSON to harness/results",
    )

    args = parser.parse_args()

    try:
        model = load_model(provider=args.provider, model_name=args.model_name)
        runner = SimpleRunner(model=model)
        result, saved_path = runner.run(args.case_name, save=not args.no_save)
    except (RuntimeError, ValueError) as exc:
        if not args.no_save:
            selected_provider = args.provider or "mock"
            selected_model_name = (
                args.model_name or DEFAULT_MODEL_NAMES.get(selected_provider, "unknown-model")
            )
            error_path = save_error_result(
                case_name=args.case_name,
                provider=selected_provider,
                model_name=selected_model_name,
                error_type=type(exc).__name__,
                error_message=str(exc),
            )
            parser.exit(
                status=1,
                message=f"error: {exc}\nsaved_to:    {error_path}\n",
            )

        parser.exit(status=1, message=f"error: {exc}\n")

    print("\n=== RESULT ===")
    print(f"case_name:   {result.case_name}")
    print(f"provider:    {result.provider}")
    print(f"model_name:  {result.model_name}")
    print(f"vulnerable:  {result.vulnerable}")
    print(f"response:    {result.response_text}")
    print(f"notes:       {result.notes}")
    if result.request_id:
        print(f"request_id:  {result.request_id}")
    if result.stop_reason:
        print(f"stop_reason: {result.stop_reason}")
    if result.usage:
        print(f"usage:       {result.usage}")
    if result.tool_calls:
        print(f"tool_calls:  {result.tool_calls}")
    print(f"timestamp:   {result.timestamp_utc}")
    if saved_path:
        print(f"saved_to:    {saved_path}")


if __name__ == "__main__":
    main()
