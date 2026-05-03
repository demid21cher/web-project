import requests


class OpenWeatherMap:
    def __init__(self, city) -> None:
        self.data = self.__get_data(city)
        # self.get_text()

    def __get_data(self, city):
        data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=e90fab7014064d2c88795d9fd95afa6f"
        )
        d = eval(data.text)
        # print(d)
        return d

    def _get_temp(self):
        temp = round(float(self.data.get("main")["temp"]) - 273.15, 1)
        # answer = f"{self.data.get('name').title()} {temp} °C"
        # print(answer)
        return temp

    def _get_weather(self):
        weather = self.data.get("weather")[0]["main"]
        # answer = f"{self.data.get('name').title()} {weather}"
        # print(answer)
        return weather

    def _get_wind(self):
        wind = self.data.get("wind")["speed"]
        # answer = f"{self.data.get('name').title()} {wind} m/s"
        # print answer
        return wind

    def _get_city(self):
        answer = f"{self.data.get('name').title()}"
        return answer

    def get_text(self):
        for key, value in self.data.items():
            print(f"{key}: {value}")

    def get_any_key(self, *args):
        return [self.data.get(key) for key in args]

    def __str__(self) -> str:
        return f"{self._get_city()} temperature: {self._get_temp()}°C, wind: {self._get_wind()} m/s, weather: {self._get_weather()}."


c = OpenWeatherMap("London")


def test_get_weather():
    # Перевірка отримання назви міста
    assert c._get_city() == "London"
    # Перевірка отримання температури
    assert isinstance(c._get_temp(), float)
    # Перевірка отримання швидкості вітру
    assert isinstance(c._get_wind(), (int, float))
    # Перевірка отримання погодних умов
    assert isinstance(c._get_weather(), str)
