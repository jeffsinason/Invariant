from invariant_harness.types import ConversationTurn, Prompt, SessionMemory


def build_session_prompt(
    system_instruction: str,
    turns: list[ConversationTurn],
    memory: list[SessionMemory] | None = None,
) -> Prompt:
    rendered_turns = "\n\n".join(
        f"[{turn.role.upper()}]\n{turn.content}" for turn in turns
    )

    prompt_parts = [f"Conversation transcript:\n{rendered_turns}"]
    if memory:
        rendered_memory = "\n".join(f"- {item.key}: {item.value}" for item in memory)
        prompt_parts.append(f"Session memory:\n{rendered_memory}")

    return Prompt(
        system=system_instruction,
        user="\n\n".join(prompt_parts),
    )
