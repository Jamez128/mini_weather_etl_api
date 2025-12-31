def convert_temperature(temperature: float, unit: str) -> float:
    if unit == "Degrees Celsius":
        return temperature
    elif unit == "Degrees Fahrenheit":
        temp_c = 5*(temperature -32)/9
        return round(temp_c,1)
    elif unit == "Kelvin":
        temp_c = (temperature - 273.15)
        return round(temp_c,1)
    else:
        raise ValueError
    
def convert_wind_speed(wind_speed: float, wind_speed_unit: str) -> float:
    """Convert wind speed to nromalised meters per second"""
    if wind_speed_unit == "ms":
        return round(wind_speed,1)
    elif wind_speed_unit == "kmh":
        wind_speed_ms = wind_speed/3.6
        return round(wind_speed_ms,1)
    elif wind_speed_unit == "mph":
        wind_speed_ms = wind_speed * 0.44704
        return round(wind_speed_ms,1)
    else:
        raise ValueError

    
def compute_feels_like_c(temp_c: float, humidity: float) -> float:
    """
    Compute the 'feels like' temperature in Celsius using the
    Rothfusz regression (heat index formula).
    Valid for temperatures >=26 deg C and humidity >= 40%.
    """
    # Convert Celsius -> Fahrenheit
    t_f = (temp_c *9/5) + 32

    h = humidity

    hi_f = (
        -42.379
        +2.04901523 * t_f
        +10.14333127 * h
        -0.22475541 * t_f * h
        -6.83783e-3 * (t_f ** 2)
        -5.481717e-2 * (h ** 2)
        +1.22874e-3 * (t_f ** 2) * h
        +8.5282e-4 * t_f * (h ** 2)
        -1.99e-6 * (t_f ** 2) * (h ** 2)
    )

    hi_c = (hi_f -32) * 5/9
    
    return round(hi_c, 1)

def safe_feels_like_c(temp_c: float, humidity: int) -> float:
    if temp_c < 26 or humidity < 40:
        return temp_c # feels like ~ actual
    return compute_feels_like_c(temp_c, humidity)