RELATIVE_METERS: dict[float, tuple[float, float]] = {
    1: (-50.50, -39.00),
    2: (-57.00, -50.50),
    3: (-62.50, -57.00),
    4.5: (-76.50, -62.50),
    6: (-82.50, -76.50),
}


def rssi_to_relative_meters(rssi: float) -> float | None:
    for key, segment in RELATIVE_METERS.items():
        (min, max) = segment
        if rssi > min and rssi <= max:
            return key
    return None


def relative_meters_method(
    ref_points: list[tuple[float, float]], rssi_values: list[int] | list[float]
) -> tuple[float, float] | None:
    # Extract reference point coordinates and RSSI values
    (x1, y1), (x2, y2), (x3, y3) = ref_points
    rssi_1, rssi_2, rssi_3 = rssi_values

    # Calculate distances
    d1 = rssi_to_relative_meters(rssi_1)
    d2 = rssi_to_relative_meters(rssi_2)
    d3 = rssi_to_relative_meters(rssi_3)
    if d1 is None or d2 is None or d3 is None:
        return None

    # Calculate trilateration coefficients
    A = 2 * x2 - 2 * x1
    B = 2 * y2 - 2 * y1
    C = d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2 * x3 - 2 * x2
    E = 2 * y3 - 2 * y2
    F = d2**2 - d3**2 - x2**2 + x3**2 - y2**2 + y3**2

    # Calculate position coordinates
    x = (C * E - F * B) / (A * E - B * D)
    y = (C * D - A * F) / (B * D - A * E)
    return x, y
