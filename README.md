# FLIPPER BOTS — Hetzner, 1 bot + 9 workerów

Ten pakiet jest gotowy pod wariant:
- 1 wspólny bot Telegram (`TELEGRAM_TOKEN` ten sam we wszystkich workerach)
- 9 niezależnych workerów
- 0 pollingów Telegrama w workerach
- każdy worker skanuje tylko 1 platformę + 1 kategorię
- publikacja jest natychmiast po wykryciu nowego ogłoszenia

## Co już jest ustawione
We wszystkich plikach `.env` i `.env.example` są już wpisane:
- właściwy `CHANNEL_ID`: `-1003731348618`
- właściwy `MESSAGE_THREAD_ID` dla każdego workera
- tylko jedna aktywna platforma na worker
- tylko właściwy URL dla danej platformy; pozostałe URL są puste

Musisz już tylko wpisać poprawny `TELEGRAM_TOKEN`.

## Topic map
- `flipper-iphone-olx` → topic `1974`
- `flipper-iphone-allegro-lokalnie` → topic `1973`
- `flipper-iphone-vinted` → topic `1972`
- `flipper-konsole-olx` → topic `1984`
- `flipper-konsole-allegro-lokalnie` → topic `1983`
- `flipper-konsole-vinted` → topic `1985`
- `flipper-macbook-olx` → topic `1842`
- `flipper-macbook-allegro-lokalnie` → topic `1989`
- `flipper-macbook-vinted` → topic `1988`

## Jak to działa
Każdy worker:
- robi `continuous_scan()` w pętli `while True`
- skanuje mniej więcej co `45` sekund (`SCAN_INTERVAL_SECONDS=45`)
- ma losowy delay `400–1200 ms` między requestami
- publikuje ofertę od razu po wykryciu
- ma własną bazę SQLite i własny volume Dockera

## Start na Hetzner
```bash
docker compose up -d --build
docker compose logs -f --tail=100
```

## Co sprawdzić po starcie
1. Uzupełnij `TELEGRAM_TOKEN` w każdym `.env`.
2. Odpal `docker compose up -d --build`.
3. Sprawdź logi jednego workera, np.:
   ```bash
   docker compose logs -f flipper-iphone-olx
   ```
4. W logach powinieneś zobaczyć:
   - `Start workera...`
   - `CHAT_ID=-1003731348618 THREAD_ID=...`
   - `=== START SCAN ===`
   - potem ewentualne wpisy o wykrytych ofertach / publish

## Najważniejsze poprawki
- usunięty konflikt z wieloma pollingami Telegrama
- poprawione `.env` dla wszystkich 9 workerów
- poprawiona pętla `continuous_scan()`, żeby nie robiła dwóch skanów pod rząd zaraz po starcie
