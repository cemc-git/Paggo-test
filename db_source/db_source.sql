CREATE TABLE IF NOT EXISTS data (
    timestamp TIMESTAMP PRIMARY KEY,
    wind_speed FLOAT,
    power FLOAT,
    ambient_temperature FLOAT
);

INSERT INTO data(
    timestamp,
    wind_speed,
    power,
    ambient_temperature
) SELECT
    ts,
    random() * 25,
    random() * 5000,
    10 + random() * 20
FROM generate_series(
    now(),
    now() + interval '10 days',
    interval '1 minute'
) AS ts;