[ENG](#ENG) || [RUS](#RUS)

# ENG

<h1 align=center>Inter-Exchange Price Comparator</h1>

This project is designed to search for anomalous differences in the value of an asset on different exchanges for the purpose of further arbitrage.

<h2 align=center>Contents</h2>

1. [Features](#Features)
2. [Technologies](#Technologies)
3. [Preparing to work](#Preparing-to-work)
4. [Usage](#Usage)
5. [DISCLAIMER](#DISCLAIMER)

## Features
The main features of this application include:
  + full autonomy (the user only needs to make initial settings and launch the program)
  + informing in Telegram when an abnormal difference in the value of an asset between different exchanges is detected
  + ease of adaptation to other exchanges (in this example, Binance is used, but a similar mechanism can be implemented on other exchanges)

## Technologies

| Technology | Description |
| ----------- | ----------- |
| Python    | Programming language in which the project is implemented   |
| MySQL    | Relational database for storing transaction history   |
| SQLAlchemy    | SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL   |
| requests    | An elegant and simple HTTP library for Python   |
| numpy    | The fundamental package for scientific computing with Python   |
| pandas    | Flexible and easy to use open source data analysis and manipulation tool   |

## Preparing to work
1. Install [Python](https://www.python.org/downloads/)
2. Download the source code of the project
3. Deploy the virtual environment (venv) in the project folder. To do this, open a terminal in the project folder and enter the command:  
   `python3 -m venv venv`
4. Activate the virtual environment with the command  
   `source venv/bin/activate`
5. Install the project dependencies, which are located in the requirements.txt file. To do this, enter the command in the terminal:  
   `pip install -r requirements.txt`
6. Change the values in the file `.env.example` and rename it to `.env`

## Usage
1. On Linux, you need to run the `run.sh` file, then run the `processing.sh` file with the commands (in the console):  
   `./run.sh`
   `./processing.sh`

3. Other operating systems require a different startup order:
   - `python truncate_price.py`
   - `python price_updaters/binance.py`
   - `python price_updaters/gate.py`
   - `python whitelist_generator.py`
   - `python main.py`
   - `python price_comparator_cex.py`
  
_All commands should be entered in the project folder after all settings have been made and the virtual environment has been activated. All paths are specified relative to the main.py file._

## DISCLAIMER
The user of this software acknowledges that it is provided "as is" without any express or implied warranties. 
The software developer is not liable for any direct or indirect financial losses resulting from the use of this software. 
The user is solely responsible for his/her actions and decisions related to the use of the software.

---

# RUS

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

## Технологии

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
