# aiogram_selenium_redis
Это телеграм-бот созданный для практики парсинга. Здесь реализован парсинг 3-мя способами: обычным http запросами (habr, ria-новости), при помощи API (VK), при помощи Selenium (WB).
Так же было реализовано кэширование новостей, с использованием Redis.

Возможные доработки: сам бот весьма сырой и не несет в себе особой бизнеслогики, но его запросто можно раскрутить до чего-то большего: можно углубиться в парсинг Wb, для поиска нужных товаров или постоянной слежкой за ценами.
Можно добавить листание новостей, чтобы пользователь мог "поскролить" ленту, и тд.
