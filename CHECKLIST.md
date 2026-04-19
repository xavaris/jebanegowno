# CHECKLIST

## Zweryfikowane
- [x] 9 workerów ma osobne foldery
- [x] każdy worker ma własny `.env`
- [x] każdy worker ma poprawny `CHANNEL_ID=-1003731348618`
- [x] każdy worker ma poprawny `MESSAGE_THREAD_ID`
- [x] tylko jedna platforma jest aktywna na worker (`ENABLE_*`)
- [x] nieaktywne URL w `.env` są wyczyszczone
- [x] `SCAN_INTERVAL_SECONDS=45`
- [x] workery używają `continuous_scan()` w `while True`
- [x] workery nie uruchamiają Telegram pollingu
- [x] kod kompiluje się (`compileall` OK)
- [x] docker-compose ma 9 osobnych usług i 9 osobnych volume'ów

## Co nadal musisz wpisać ręcznie
- [ ] prawdziwy `TELEGRAM_TOKEN` w 9 plikach `.env`

## Co może się zepsuć w runtime
- strony OLX / Allegro Lokalnie / Vinted mogą zmienić HTML i scraper będzie wymagał poprawki
- platforma może zwrócić captcha / anti-bot / rate limit
- jeśli bot nie ma prawa pisać do danego topiku, Telegram odrzuci wiadomość
- jeśli token bota będzie zły, workery wystartują, ale publish się nie uda
- na świeżej bazie pierwsze minuty mogą iść na budowę baseline median; liczba publikacji może być wtedy mniejsza
