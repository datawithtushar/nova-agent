# Creating an analysis tool for basic calculations
from langchain.tools import tool


@tool
def run_analysis(operation: str, values: list[float]):
    """Perform calculations such as percentage, average, total, ratio, growth and prorated values."""

    if operation == "add":
        return values[0] + values[1]

    if operation == "subtract":
        return values[0] - values[1]

    if operation == "multiply":
        return values[0] * values[1]

    if operation == "divide":
        if values[1] == 0:
            return "Cannot divide by zero."

        return values[0] / values[1]

    if operation == "percentage":
        return values[0] * values[1] / 100

    if operation == "percentage_change":
        old_value = values[0]
        new_value = values[1]

        if old_value == 0:
            return "Old value cannot be zero."

        return ((new_value - old_value) / old_value) * 100

    if operation == "average":
        if not values:
            return "No values provided."

        return sum(values) / len(values)

    if operation == "total":
        return sum(values)

    if operation == "minimum":
        if not values:
            return "No values provided."

        return min(values)

    if operation == "maximum":
        if not values:
            return "No values provided."

        return max(values)

    if operation == "ratio":
        if values[1] == 0:
            return "Second value cannot be zero."

        return values[0] / values[1]

    if operation == "prorate":
        value = values[0]
        completed_period = values[1]
        total_period = values[2]

        if total_period == 0:
            return "Total period cannot be zero."

        return value * completed_period / total_period

    return "Unsupported analysis operation."