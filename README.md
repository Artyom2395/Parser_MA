# Parser_MA
##Для файла metro_parser.py##
Этот репозиторий содержит Python-скрипт для скрапинга информации о продуктах с веб-сайта Metro. Скрипт позволяет извлекать данные о продуктах, такие как наименование, цены, ссылки и бренд, и сохранять их в формате CSV.

Содержание
Инструкции по установке
Как использовать скрипт
Как работает скрипт
Примечания
Лицензия
Инструкции по установке
Для работы с этим скриптом необходим Python версии 3.x и установленные библиотеки, указанные в файле requirements.txt.

Вы можете установить необходимые библиотеки с помощью pip следующим образом:

bash
pip install -r requirements.txt
Как использовать скрипт
Запустите скрипт metro_scraper.py, предварительно настроив параметры:

city_id - идентификатор города на веб-сайте Metro.
city_name - название города (для создания имени CSV-файла).
Скрипт создаст файл products_city.csv (где city - это название города), в который будут сохранены данные о продуктах.

Запустите скрипт из командной строки:

bash
python metro_parser.py
Скрипт начнет скрапинг данных с веб-сайта Metro и сохранит результаты в указанный CSV-файл.

Как работает скрипт
Скрипт инициализирует сеанс с веб-сайтом Metro для указанного города.

Создается CSV-файл для сохранения данных о продуктах.

Скрипт начинает скрапинг данных с веб-сайта, перебирая страницы с товарами и извлекая информацию о каждом продукте.

Данные о продуктах (название, цены, ссылка и бренд) сохраняются в CSV-файл.

Процесс повторяется для всех доступных страниц с товарами.

По завершении скрапинга, CSV-файл закрывается, и скрипт сообщает о завершении работы.

Примечания
Для использования скрипта необходимо знать city_id для вашего города на веб-сайте Metro. Этот идентификатор можно найти, просмотрев сетевые запросы браузера при переходе на соответствующую страницу на сайте Metro (в куках).

##Для файла metro_async_parser.py##
Установка зависимостей
Перед использованием парсера, вам необходимо установить несколько зависимостей:

Убедитесь, что у вас установлен Python 3.7 или более новая версия.

Установите библиотеку aiohttp с помощью pip:

bash
pip install aiohttp
Установите библиотеку beautifulsoup4:
bash
pip install beautifulsoup4
Как использовать
Загрузите исходный код парсера в свой проект.

Создайте асинхронную функцию для сбора данных. Пример использования парсера для Москвы:

# Создание файла для Москвы moscow_csv_file, moscow_writer = await create_csv_file("moscow") await scrape_data_for_city(10, "Moscow", moscow_writer) moscow_csv_file.close()
Запустите асинхронную функцию:

loop = asyncio.get_event_loop() loop.run_until_complete(main())
Функции парсера
create_csv_file(city): Эта функция создает CSV-файл для записи данных о продуктах. Он принимает имя города и возвращает объекты CSV-файла и писателя.

make_request(session, url, headers, cookies): Эта функция выполняет асинхронный HTTP-запрос с использованием библиотеки aiohttp и возвращает содержимое страницы.

scrape_data_for_city(city_id, city_name, writer): Эта функция выполняет парсинг данных для заданного города. Она принимает идентификатор города, название города и объект писателя CSV. Далее она выполняет запросы к сайту Metro-CC, извлекает информацию о продуктах и записывает их в CSV.

Запуск
После настройки и использования функций парсера, вы можете запустить асинхронную функцию main(), как показано в примере выше. Это запустит процесс сбора данных для указанного города.