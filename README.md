# Spondylus: prototyp nowej strony

Statyczny prototyp strony spondylus.pl: strona główna i przykładowe podstrony (podologia, kadra, profil specjalisty, kontakt).

## Uruchomienie

```
python3 build.py
python3 -m http.server 8765
```

Następnie otwórz http://localhost:8765/index.html. Na macOS wystarczy dwukrotnie kliknąć `Otwórz prototyp.command`.
Kalendarz rejestracji (ProAssist) działa tylko przez serwer http, nie z pliku.

## Struktura

- `src/pages/` treść podstron, z której `build.py` składa gotowe pliki HTML (nagłówek, stopka, panel dostępności)
- `assets/css/style.css`, `assets/js/main.js` style i skrypty
- `assets/img/` zdjęcia i ilustracje w formacie WebP
- `narzedzia/` skrypty pomocnicze: jednolite portrety zespołu i koło „Zespół wokół pacjenta”

Przełącznik „Uzasadnienie zmian” na stronie pokazuje przy każdej sekcji, co zmienia się względem obecnej strony i dlaczego.
