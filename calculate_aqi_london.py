def calculate_aqi(row):
    """
    Calculate the Air Quality Index (AQI) for both roadside and background measurements and returns both AQI values.

    Args:
    row: A dictionary-like object that represents the pollutant concentrations.

    Returns:
    Two AQI values (for roadside and background) as a tuple.
    """
    # Define the breakpoints for pollutants and AQI
    breakpoints = {
        "PM2.5": [(0, 35), (36, 75), (76, 115), (116, 150), (151, 250), (251, 350), (351, 500)],
        "PM10": [(0, 50), (51, 150), (151, 250), (251, 350), (351, 420), (421, 500), (501, 600)],
        "NO2": [(0, 40), (41, 80), (81, 180), (181, 280), (281, 565), (566, 750), (751, 940)],
        "O3": [(0, 80), (81, 100), (101, 120), (121, 140), (141, 160), (161, 180), (181, 220)],
        "SO2": [(0, 50), (51, 150), (151, 475), (476, 800), (801, 1600), (1601, 2100), (2101, 2620)]
    }

    aqi = [(0, 50), (51, 100), (101, 150), (151, 200), (201, 300), (301, 400), (401, 500)]

    pollutants = ["PM2.5", "PM10", "NO2", "O3", "SO2"]

    max_aqi_R = 0
    max_aqi_B = 0

    for pollutant in pollutants:
        if pollutant + "_R" not in row or pollutant + "_B" not in row:
            raise ValueError(f"Expected {pollutant}_R and {pollutant}_B in input row")

        concentration_R = row[pollutant + "_R"]
        concentration_B = row[pollutant + "_B"]

        for i, (low, high) in enumerate(breakpoints[pollutant]):
            # Roadside
            if low <= concentration_R <= high:
                low_aqi, high_aqi = aqi[i]
                aqi_value_R = ((high_aqi - low_aqi) / (high - low)) * (concentration_R - low) + low_aqi
                max_aqi_R = max(max_aqi_R, round(aqi_value_R))

            # Background
            if low <= concentration_B <= high:
                low_aqi, high_aqi = aqi[i]
                aqi_value_B = ((high_aqi - low_aqi) / (high - low)) * (concentration_B - low) + low_aqi
                max_aqi_B = max(max_aqi_B, round(aqi_value_B))

    return max_aqi_R, max_aqi_B
