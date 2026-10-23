
import re


def get_variables(expression):
    """
    Find variables used in an expression.
    Function names such as readInput() are not treated as variables.
    """
    identifiers = re.findall(r"\b[A-Za-z_]\w*\b", expression)

    ignored_words = {"True", "False", "None"}
    variables = set()

    for name in identifiers:
        if name in ignored_words:
            continue

        # Ignore a name followed by '(' because it is a function call.
        pattern = rf"\b{re.escape(name)}\b\s*\("
        if re.search(pattern, expression):
            continue

        # Ignore identifiers that are part of quoted strings.
        # String handling will be improved in a later version.
        variables.add(name)

    return variables


def has_function_call(expression):
    """
    Conservatively treat function calls as potentially side-effecting.
    """
    return bool(re.search(r"\b[A-Za-z_]\w*\s*\(", expression))


def eliminate_dead_code(source_code):
    """
    Perform backward dead assignment elimination on simplified,
    straight-line intermediate code.

    Supported examples:
        t1 = 10
        t3 = t1 + t2
        print(t3)

    This is a teaching prototype, not a complete compiler.
    """
    instructions = [
        line.strip()
        for line in source_code.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    live_variables = set()
    optimized_reversed = []
    removed_instructions = []

    # Process instructions backwards.
    for instruction in reversed(instructions):

        # Recognize simple assignments such as x = 10 or x = a + b.
        match = re.fullmatch(
            r"([A-Za-z_]\w*)\s*=\s*(.+)",
            instruction
        )

        if match:
            target = match.group(1)
            expression = match.group(2).strip()

            used_variables = get_variables(expression)
            potentially_has_side_effects = has_function_call(expression)

            # Remove an assignment only if its result is not needed
            # and evaluating the expression has no possible side effects.
            if (
                target not in live_variables
                and not potentially_has_side_effects
            ):
                removed_instructions.append(instruction)
                continue

            # Keep the instruction.
            optimized_reversed.append(instruction)

            # The assignment defines target, replacing its old value.
            live_variables.discard(target)

            # The expression requires these variables.
            live_variables.update(used_variables)

        else:
            # Keep non-assignment statements conservatively.
            optimized_reversed.append(instruction)
            live_variables.update(get_variables(instruction))

    optimized_code = list(reversed(optimized_reversed))
    removed_instructions.reverse()

    return {
        "original_code": instructions,
        "optimized_code": optimized_code,
        "removed_instructions": removed_instructions,
        "original_count": len(instructions),
        "optimized_count": len(optimized_code),
        "removed_count": len(removed_instructions),
    }


if __name__ == "__main__":
    sample_code = """
x = 10
y = 20
print(x)
"""

    result = eliminate_dead_code(sample_code)

    print("===== ORIGINAL CODE =====")
    print("\n".join(result["original_code"]))

    print("\n===== OPTIMIZED CODE =====")
    print("\n".join(result["optimized_code"]))

    print("\n===== REMOVED INSTRUCTIONS =====")
    for instruction in result["removed_instructions"]:
        print(instruction)

    print("\n===== STATISTICS =====")
    print("Original instructions:", result["original_count"])
    print("Optimized instructions:", result["optimized_count"])
    print("Removed instructions:", result["removed_count"])
