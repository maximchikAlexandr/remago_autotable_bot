# Autotable bot 
## О проекте

Тестовое задание для Remago

## Установка

Склонировать репозиторий с GitHub:

```sh
git clone https://github.com/maximchikAlexandr/remago_autotable_bot.git
```

Перейти в директорию с проектом:

```sh
cd remago_autotable_bot/
```

**Дальнейшая установка требует запущенного Docker**

### Linux

Сделать исполняемым файл со скриптом и запустить его:

```bash
chmod +x install.sh && ./install.sh
```

### Windows

Запустить файл со скриптом:

```powershell
./install.cmd
```

Данные скрипты создают файл **.env** с переменными окружения.
В переменных окружения сохранены тестовые параметры БД, для реальной
работы переменные окружения необходимо изменить.

Также вам необходимо в файле **.env** в переменную 
**TELEGRAM_TOKEN** прописать свой токен для Telegram Bot API

После добавления токена, запустить приложение:

```bash
docker exec -it tg_app python main.py
```

## Токен для Telegram Bot API
Чтобы получить токен, перейдите на [@BotFather](https://t.me/botfather)
, выполните команду **/newbot**. Пройдя все шаги, вы получите токен


Более полное описание процедуры можно помотреть в документации:

https://core.telegram.org/bots/features#creating-a-new-bot

## Уровень логирования SQLAlchemy

Чтобы приложение выводило в консоль SQL запросы, нужно 
изменить переменную окружения в файле **.env**:

```bash
SQLALCHEMY_LOG_LEVEL=INFO
```