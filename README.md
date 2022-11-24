# weather_api

### building
```
docker build -t weather:latest .
```

### Running
```
docker run -p 8000:8000 -e WEATHER_API="apikey"  weather
```

### Api Key
https://openweathermap.org/appid