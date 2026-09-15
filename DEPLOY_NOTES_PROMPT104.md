# Deploy notes — catalog art lockstep (Prompt 104)

Date: 2026-09-14  
Site root: `D:\WS\programs\Phyllux-repos\phyllux-app`

## Local verify

```powershell
cd D:\WS\programs\Phyllux-repos\phyllux-app
python build_site.py
python serve_local.py
```

Check:

- http://127.0.0.1:8788/suite/ — APK honesty cards + suite icon
- http://127.0.0.1:8788/catalog/decision-and-uncertainty/ — icons on matched Android rows
- `assets/catalog/` contains 62 PNGs from Android registry

## Production

```powershell
npx vercel deploy --prod
```

Only when David asks. This ticket prepared the build; it did **not** deploy.

## Provenance

Android art source: `D:\WS\programs\Quantonics-repos\quantonics-android\docs\assets\`  
Gate: `docs/phase7-assets-gate.md` in that repo.
