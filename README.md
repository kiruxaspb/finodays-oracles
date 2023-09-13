dev: python 3.10.10; pip 22.2.1

general req: wheel, setuptools

СХЕМЫ, ОПИСАНИЕ, А ТАКЖЕ УЛУЧШЕНИЯ В ОРАКУЛАХ: https://docs.google.com/document/d/1MYcTv0Htifq1JQQHPAD0byunHPGIIL5l_AwtYZf9BUw

В данном репозитории расположен исходный код оракулов для обновления цены на бирженвые ресурсы для формирования стоимости для конвертации

Такой оракул будет расположен вместе с нодой на стороне страны-участницы

Оракул будет обновлять стоимость ресурсов для конвертации в указанный интервал времени


выполнение функции `update_prices()` занимает ~ 0.6 секунды

оптимальное время блока для консенсуса proof of service - 5 секунд

поэтому можно обновлять рейт каждые 5 секунд

Создайте файл `secret.py` в папке `/src` рядом с сервером по примеру в файле `secret.example.py` 

1. Создать виртуальное окружение:
Windows:
`python -m venv venv`
Linux:
`python3 -m venv venv`

2. Активировать виртуальное окружение:
Windows:
`.\venv\Scripts\activate`
Linux:
`source venv/bin/activate`

3. Установить зависимости:
Windows/Linux:
`pip install -r requirements.txt`

4. Билд контейнера с оракулом
`docker build -t conversion-oracle .`

5. Запуск контейнера с оракулом
`docker run -p 5000:5000 conversion-oracle`



