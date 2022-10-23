MAX_STEP = 30
EPSILON = 0.001


def perform_gradient_descent(
    fct_to_descent,
    last_position,
    last_position_value,
    step_size,
    step_iteration,
    seen_positions,
    seen_values,
):

    left = last_position - step_size
    left_value = fct_to_descent(left)
    right = last_position + step_size
    right_value = fct_to_descent(right)
    if last_position_value is not None:
        if (
            last_position_value < left
            and last_position_value < right
            or last_position_value - min(left_value, right_value) < EPSILON
            or step_iteration > MAX_STEP
        ):
            return seen_positions, seen_values

    if left_value == right_value:
        perform_gradient_descent(
            fct_to_descent,
            last_position,
            last_position_value,
            step_size / 4,
            step_iteration + 1,
            seen_positions,
            seen_values,
        )

    if left_value < right_value:
        seen_values.append(left_value)
        seen_positions.append(left)

        return perform_gradient_descent(
            fct_to_descent,
            left,
            left_value,
            step_size / 2,
            step_iteration + 1,
            seen_positions,
            seen_values,
        )

    if right_value < left_value:
        seen_values.append(right_value)
        seen_positions.append(right)

        return perform_gradient_descent(
            fct_to_descent,
            right,
            right_value,
            step_size / 2,
            step_iteration + 1,
            seen_positions,
            seen_values,
        )


def wrapper(fct_to_descent):
    starting_pos = 0
    step_size = 20
    iteration = 0

    return perform_gradient_descent(
        fct_to_descent,
        starting_pos,
        None,
        step_size,
        iteration,
        [starting_pos],
        [fct_to_descent(starting_pos)],
    )
