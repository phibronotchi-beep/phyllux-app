# phyllux.app

Apps hub for Phyllux and Quantonics Applications.

## Local

```powershell
cd D:\WS\programs\Phyllux-repos\phyllux-app
python build_site.py
python serve_local.py
```

http://127.0.0.1:8788/

## Live

https://phyllux.app/

Rebuild: `python build_site.py` then `npx vercel deploy --prod`
