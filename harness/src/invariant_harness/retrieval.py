from invariant_harness.types import Prompt, RetrievedContent


def build_retrieval_prompt(
    system_instruction: str,
    user_request: str,
    retrieved_items: list[RetrievedContent],
) -> Prompt:
    rendered_items = "\n\n".join(
        (
            f"[Source: {item.source}]"
            f"\n[Trust: {item.trust_level}]"
            f"\n{item.content}"
        )
        for item in retrieved_items
    )

    user_text = (
        f"User request:\n{user_request}\n\n"
        "Retrieved content:\n"
        f"{rendered_items}"
    )

    return Prompt(system=system_instruction, user=user_text)
