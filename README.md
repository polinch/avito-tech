# JSON API для сайта объявлений

## Дизайн сервиса

Язык - Python, с использованием фреймворка Flask.    
СУБД - PostgreSQL

### Методы
|Метод HTTP|URL|Действие|
|---|---|---|
|GET|/ads?page=page_number|Получить список объявлений|
|GET|/ads/id?parameter=fields|Получить конкретное объявление|
|POST|/ads|Создать объявление|

Параметр page в методе для получения списка объявлений является обязательным.

Для сортировки по дате и цене в запрос следует передать параметры sort_date и sort_price. 

|Значение параметра|Сортировка|
|---|---|
|0|По возрастанию|
|1|По убыванию|

Для валидации полей при создании объявления используется JSON Schema.

Файл avito_test_ad.sql - для создания БД.

### Примеры запросов
Добавить объявление
```
curl -i -H "Content-Type: application/json" -X POST "localhost:5000/ads" -d '{"name": "Тестовое объявление", "photo1": "url1", "photo2": "url2", "photo3": "url3", "price": 405600, "description": "Описание тестового объявления."}'
```
Просмотр объявлений
```
curl -i -X GET "localhost:5000/ads?page=1"
curl -i -X GET "localhost:5000/ads?page=2&sort_date=0"
curl -i -X GET "localhost:5000/ads?page=1&sort_date=1&sort_price=0"
```
Просмотр одного объявления
```
curl -i -X GET "localhost:5000/ads/4"
curl -i -X GET "localhost:5000/ads/4?parameter=fields"
```



