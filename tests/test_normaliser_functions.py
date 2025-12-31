import pytest

from app.services.weather_helpers import (
    convert_wind_speed, 
    safe_feels_like_c, 
    convert_temperature, 
    compute_feels_like_c
    )

# ---------- convert_temperature ----------

@pytest.mark.parametrize(
    "temp, unit, expected",
    [
        (26.0, "Degrees Celsius", 26.0),
        (86.0, "Degrees Fahrenheit", 30.0),
        (299.15, "Kelvin", 26.0),
    ],
)
def test_convert_temperature_valid_units(temp, unit, expected):
    result = convert_temperature(temp, unit)
    assert pytest.approx(result, rel=1e-3) == expected

def test_convert_temperature_unknown_unit_raises():
    with pytest.raises(ValueError):
        convert_temperature(25.0, "Rankine")

# ---------- convert_wind_speed ----------

@pytest.mark.parametrize(
    "speed, unit, expected",
    [
        (35, "ms", 35),
        (65, "kmh", 18.1),
        (81, "mph", 36.2),
    ],
)
def test_convert_wind_speed_valid_units(speed, unit, expected):
    result = convert_wind_speed(speed, unit)
    assert result == expected

def test_convert_wind_unknown_unit_raises():
    with pytest.raises(ValueError):
        convert_wind_speed(24, "Knot")

# ---------- behaviour_check_safe_feels_like ----------

@pytest.mark.parametrize(
    "temp, humidity, feels_like_c",
    [
        (25, 30, 25),
        (27, 30, 27),
        (24, 45, 24),
        (30, 55, 31.9),
        (35, 90, 63.7),
    ],
)
def test_safe_feels_like_c_behaviour(temp, humidity, feels_like_c):
    result = safe_feels_like_c(temp, humidity)
    assert pytest.approx(result, rel=1e-3) == feels_like_c
