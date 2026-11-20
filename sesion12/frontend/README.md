# Lab 11 – Comunicación entre componentes en ReactJS

## Árbol de componentes y dato que vive en cada nivel

```
App                      [estado: query, favoriteIds]  (usa useDebounce)
├── Header               ← favoritesCount (solo el número)
├── PremieresSection     [estado: simulateError]  (usa usePremieres, useWindowSize)
│   ├── SkeletonCard ×N  (estado: cargando)
│   └── PremiereCarousel [estado: start]  ← premieres  (usa useWindowSize)
├── Banner               ← activeFilter, resultsCount, onClearFilter
├── SearchBar            ← value, onChange, isSearching
├── MovieList            ← movies, favoriteIds, onToggleFavorite  (usa useWindowSize)
│   └── MovieCard ×N     ← movie, isFavorite, onToggleFavorite
└── Toaster              (react-hot-toast)
```

`[ ]` = estado propio · `←` = props que recibe

## Hooks propios

| Hook | Qué lógica extrae | Componentes que lo usan |
|---|---|---|
| `useDebounce` | Retrasa un valor hasta que deja de cambiar (400 ms) | App (buscador) |
| `useWindowSize` | Escucha el `resize` de la ventana y limpia el listener | MovieList, PremiereCarousel, PremieresSection |
| `usePremieres` | Petición simulada con 3 estados: cargando, datos y error | PremieresSection |

## Utilidades

- `movieAdapter.js`: patrón adaptador. Convierte los datos de la API (`original_title`, `vote_average`) al modelo de la app (`title`, `rating`). Lo usan la cartelera y `usePremieres`.
- `getColumns.js`: regla compartida de columnas según el ancho.

## ¿Por qué el contador de favoritas no puede vivir en Header?

El contador no puede vivir en Header porque MovieList también lo necesita para marcar los corazones, y como son hermanos no pueden compartir datos directamente; por eso vive en App, su padre común, que le pasa a Header solo el número.

## Comunicación entre hermanos

- **Banner → SearchBar / MovieList:** el botón "Limpiar filtro" llama a `onClearFilter`, `App` vacía `query` y los dos hermanos se actualizan solos.
- **MovieCard → Toaster:** la tarjeta solo llama a `onToggleFavorite`. `App` decide mostrar el aviso, así que la tarjeta no sabe cómo se muestra.