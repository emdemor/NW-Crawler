# NW Crawler

1. Configure seu arquivo `.env`:
```
LOGURU_LEVEL=DEBUG
ENV=dev
```
2. Para acessar o sandbox, execute:
```
make start-jupyter
```

3. Para fazer o scraping de todos os artigos, execute:
```
make scrape
```

Se quiser fazer até um número limitado de páginas (por exemplo, até 3), rode:
```
make scrape last=3
```
