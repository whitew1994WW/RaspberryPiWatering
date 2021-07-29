settings = {
    'trigger_saturation': 20,  # Water saturation level at which watering the plant starts
    'pump_output_pin': 16,
    'soil_moisture_sensor_pin': 18,

    # Rain options
    'rain_time': 60,  # minutes
    'rain_amount': 200,  # ml
    'check_frequency': 40,  # In seconds

    # Script options
    'water_when_low': True,
    'calibrate': True,
    'table_name': "example_bucket_whitew1994",
    'database_name': "test",
    'output_location': "s3://athena-output-auto-water/"}