College Notification Bot
========================

A Telegram bot that automates the process of scraping college website notifications and sending them directly to a Telegram channel or user. This tool ensures you never miss an important update by monitoring the target website and maintaining a local database to prevent duplicate alerts.

Project Structure
-----------------

*   main.py: The entry point of the bot. It initializes the bot and triggers the scraping/notification loop.
    
*   scraper.py: Contains the logic for fetching and parsing data from the college website.
    
*   database.py: Handles SQLite database connections to store sent notifications and avoid duplicates.
    
*   notifications.db: The SQLite database file (generated automatically).
    
*   test\_bot.py: A script for testing bot functionality in isolation.
    
*   .env: Configuration file for storing sensitive credentials like the Bot Token.
    

Features
--------

*   **Automated Scraping**: Periodically checks the college website for new notices.
    
*   **Duplicate Detection**: Uses a local SQLite database to ensure the same notice is not sent twice.
    
*   **Telegram Integration**: Instantly pushes new updates to a specified Telegram chat or channel.
    
*   **Environment Configuration**: Uses .env for secure credential management.
    

Prerequisites
-------------

*   Python 3.8+
    
*   A Telegram Bot Token (obtained from [@BotFather](https://t.me/BotFather))
    

Installation
------------

1.  Bashgit clone https://github.com/Bipul20000/college\_noti\_bot.gitcd college\_noti\_bot
    
2.  Bashpip install requests beautifulsoup4 python-telegram-bot python-dotenv_(Note: If the code uses telebot, install pyTelegramBotAPI instead of python-telegram-bot.)_
    
3.  Code snippetBOT\_TOKEN=your\_telegram\_bot\_token\_hereCHAT\_ID=your\_target\_chat\_id
    

Usage
-----

1.  Bashpython main.py
    
2.  Bashpython test\_bot.py
    

Customization
-------------

To change the target website or the HTML parsing logic, modify the scraper.py file. Ensure that the scraper function returns a list of data compatible with the structure expected in main.py.

License
-------

This project is open-source. Feel free to modify and distribute it as needed.
