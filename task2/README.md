# Задание 2

В SQL базе данных есть продукты и категории. Одному продукту может соответствовать много категорий, в одной категории может быть много продуктов.

Напишите HTTP API через которое можно получить:

список всех продуктов с их категориями,
список категорий с продуктами,
список всех пар «Имя продукта – Имя категории».
Если у продукта нет категорий, то он все равно должен выводиться.

Если у категории нет продуктов, то она все равно должна выводиться.

Проект должен содержать docker-compose.yml файл, через который можно запустить сервис и проверить его работу.

Дополнительно оценим покрытие кода юнит-тестами.


## Запуск решения

Для запска вне контейнера и подключения к БД PostgreSQL необходимо указать конфигурацию в файле:
```bash
.env
```

Для запска docker-контейнера исполнить:
```bash
docker-compose up
```

## В программе реализованы запросы:
- список всех продуктов с их категориями
- список категорий с продуктами
- список всех пар «Имя продукта – Имя категории»
- запрос на инициализацию БД и заполнение её тестовыми данными
