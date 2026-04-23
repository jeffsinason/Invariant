from invariant_harness.types import Prompt, ToolSpec


def build_tool_prompt(
    system_instruction: str,
    user_request: str,
    tools: list[ToolSpec],
    context: str = "",
) -> Prompt:
    rendered_tools = "\n".join(
        f"- {tool.name}: {tool.description} (allowed={str(tool.allowed).lower()})"
        for tool in tools
    )

    user_parts = [f"User request:\n{user_request}", f"Available tools:\n{rendered_tools}"]
    if context:
        user_parts.append(f"Context:\n{context}")

    return Prompt(
        system=system_instruction,
        user="\n\n".join(user_parts),
    )
