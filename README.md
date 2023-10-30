<h1 align=center>Inter-Exchange Price Comparator</h1>

Этот проект предназначен для поиска аномальной разницы в стоимости актива на разных биржах с целью дальнейшего арбитража.

<h2 align=center>Содержание</h2>

1. [Особенности](#Особенности)
2. [Технологии](#Технологии)
3. [Подготовка к работе](#Подготовка-к-работе)
4. [Использование](#Использование)
5. [ОТКАЗ ОТ ОТВЕТСТВЕННОСТИ](#ОТКАЗ-ОТ-ОТВЕТСТВЕННОСТИ)

## Особенности
Основные особенности этого приложения включают в себя:
  + полная автономность (пользователю необходимо лишь сделать начальные настройки и запустить программу)
  + информирование в телеграм об обнаружении аномальной разница в стоимости актива между различными биржами
  + простота адаптации под другие биржи (в этом примере используется биржа Binance, однако подобный механизм можно реализовать на других биржах)

## Используемые технологии и библиотеки

| Технология / Библиотека | Описание |
| ----------- | ----------- |
| Python    | Язык программирования, на котором реализован проект   |
| MySQL    | Реляционная база данных для хранения истории сделок   |
| SQLAlchemy    | Комплексный набор инструментов для работы с реляционными базами данных в Python   |
| requests    | HTTP-библиотека для Python. Используется для отправки HTTP-запросов и получения ответов   |
| numpy    | Пакет для научных вычислений на Python   |
| pandas    | Инструмент для анализа и обработки данных   |

## Подготовка к работе
1. Установите [Python](https://www.python.org/downloads/)
2. Скачайте исходный код проекта
3. Разверните виртуальное окружение (venv) в папке с проектом. Для этого откройте терминал в папке с проектом и введите команду:  
   `python3 -m venv venv`
4. Активируйте виртуальное окружение командой  
   `source venv/bin/activate`
5. Установите зависимости проекта, которые находятся в файле requirements.txt. Для этого в терминале введите команду:  
   `pip install -r requirements.txt`
6. Внесите изменения в файл `.env.example` и переименуйте его в `.env`

## Использование
1. На Linux нужно запустить файл `run.sh`, после чего запустить файл `processing.sh` командами (в консоли):  
   `./run.sh`
   `./processing.sh`

3. Для других ОС необходимо порядок запуска иной:
   - `python truncate_price.py`
   - `python price_updaters/binance.py`
   - `python price_updaters/gate.py`
   - `python whitelist_generator.py`
   - `python main.py`
   - `python price_comparator_cex.py`
  
_Все команды вводить в папке с проектом после выполнения всех настроек и активации виртуального окружения. Все пути указаны относительно файла main.py._

## ОТКАЗ ОТ ОТВЕТСТВЕННОСТИ
Пользователь этого программного обеспечения подтверждает, что оно предоставляется "как есть", без каких-либо явных или неявных гарантий. 
Разработчик программного обеспечения не несет ответственности за любые прямые или косвенные финансовые потери, возникшие в результате использования данного программного обеспечения. 
Пользователь несет полную ответственность за свои действия и решения, связанные с использованием программного обеспечения.
