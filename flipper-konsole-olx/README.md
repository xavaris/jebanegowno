# FLIPPER KONSOLE DO GIER OLX

Bot skanuje co ~45 sekund i publikuje okazje niemal natychmiast.

## Co skanuje
- Platforma: OLX
- Kategoria: Konsole do gier
- Start URL: `https://www.olx.pl/elektronika/gry-konsole/konsole/?search%5Border%5D=created_at:desc`

## Funkcje
- continuous scanning w tle (`continuous_scan()` w `app/main.py`)
- bardzo krótki sleep po każdym skanie (`SCAN_INTERVAL_SECONDS=45`)
- losowe opóźnienie 400–1200 ms między żądaniami
- natychmiastowa publikacja na Telegramie po wykryciu nowej oferty
- baseline mediany i score okazji
- filtry anty-oszustwo / anty-akcesoria
- deduplikacja w SQLite
- tłumaczenie opisów
- locki przeciw dublowaniu
- gotowy Dockerfile i `railway.toml`

## Uruchomienie lokalne

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
python -m app.main
```

## Tryb pracy na Hetzner
Ten projekt działa jako **worker publikujący**. Nie uruchamia `start_polling()`.
Używa wspólnego `TELEGRAM_TOKEN` razem z pozostałymi workerami i wysyła wiadomości tylko do swojego `MESSAGE_THREAD_ID`.

## Komendy Telegram
W tym wariancie Hetzner worker nie obsługuje komend Telegram. Służy wyłącznie do skanowania i natychmiastowej publikacji.


## Hetzner
Uruchamiaj 9 workerów równolegle, każdy z tym samym `TELEGRAM_TOKEN`, tym samym `CHANNEL_ID`, ale z innym `MESSAGE_THREAD_ID` i osobną bazą SQLite.
