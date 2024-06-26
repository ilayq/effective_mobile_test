# Установка и запуск
**!!!ВНИМАНИЕ!!! ДЛЯ ЗАПУСКА ТРЕБУЕТСЯ `Python 3.12` ( используются generic-types ) ИЛИ ЗАПУСК ЧЕРЕЗ `Docker`**

1. ```git clone git@github.com:ilayq/effective_mobile_test.git```
2. ```cd effective_mobile_test```
3. Тесты: 
    ```python3 -m unittest ```
4. Запуск
    ```python3 main.py``` или `docker build -t <tag_name> . && docker run -it <tagname>`

### Комментарии по проекту
##### Архитектура
1. Директория `tests` - тесты 
2. Директория `src` - **исходный код**
    - `src/category.py` - `Enum`класс для категории операции (Доход / Расход)
    - `src/transaction.py` - `dataclass` для операции, определены методы `update` - обновление данных на основе другой транзакции, `__str__` - для приведения в единый формат и записи в файл
    - `src/utils.py` - различные вспомогательные функции, в том числе поиск в коллекции по предикатам, считывание данных с пользовательского ввода ( обработка ошибок, автоматическое приведение к нужному типу )
    - `src/db.py` - абстрактный класс источника данных и его имплементация в виде `FileDataBase` (чтение данных из файла, обновление, добавление, удаление)
    - `src/app.py` - класс приложения `FinanceControllerApp` с несколькими обработчиками пользовательских команд, использует абстрактный класс `DataSource`, описанный в `src/db.py`, то есть предусмотрена расширяемость приложения
##### Функционал приложения
1. Вывод баланса
2. Добавление записи
3. Редактирование записи
4. Поиск по записям (возможен поиск по нескольким параметрам одновременно)
5. Удаление записей
6. Вывод всех записей

Весь пользовательский ввод обрабатывается на предмет ошибок, используется контекстный менеджер ( в классе `FinanceControllerApp` ), который сохраняет автоматически сохраняет все данные в файл. Есть возможность через аргументы коммандной передать название файла, который будет являться базой данных, например `python3 main.py database.db`

Везде есть `type-hints`, и `doc-strings` описывают важные методы и функции. 