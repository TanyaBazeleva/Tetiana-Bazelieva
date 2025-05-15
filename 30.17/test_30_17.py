import unittest
from unittest.mock import patch
from T30_17 import get_weather, save_weather
import pandas as pd
import os


class TestWeatherForecast(unittest.TestCase):
    def test_1_mocked_fetch(self):
        mock_html = ""
        for i in range(1, 6):
            mock_html += f"""
            <div id="bd{i}">
                <p class="date">15</p>
                <p class="month">травня</p>
                <div class="min">Мін. -2°C</div>
                <div class="max">Макс. +9°C</div>
            </div>
            """
        with patch("T30_17.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = mock_html
            result = get_weather("київ")
            self.assertEqual(len(result), 5)
            self.assertIn("Дата", result[0])
            self.assertIn("Мінімальна температура", result[0])
            self.assertIn("Максимальна температура", result[0])

    def test_2_error_request(self):
        with patch("T30_17.requests.get") as mock_get:
            mock_get.return_value.status_code = 404
            with self.assertRaises(ValueError):
                get_weather("notfound")

    def test_3_excel_save(self):
        test_data = [
            {"Дата": "15 травня", "Мінімальна температура": "-2°C", "Максимальна температура": "+9°C"}
        ]
        filename = "test_weather.xlsx"
        save_weather(test_data, filename)
        self.assertTrue(os.path.exists(filename))
        df = pd.read_excel(filename)
        self.assertIn("Дата", df.columns)
        os.remove(filename)

if __name__ == "__main__":
    unittest.main(verbosity=2)
