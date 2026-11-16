# Lab 11 extra – Los hooks del agente

## 1. Conteo de pruebas

### Mis hooks · `npm test`

| Paso | Fallidas | Pasan |
|---|---|---|
| Inicio | 40 | 17 / 57 |
| Tras useDebounce | 34 | 23 / 57 |
| Tras usePlans | 18 | 39 / 57 |
| Tras useAgentRun | 0 | 57 / 57 |

### Hooks de la IA · `npm run test:ai`

| Paso | Fallidas | Pasan |
|---|---|---|
| Original | 20 | 37 / 57 |
| Tras arreglar useDebounce | 15 | 42 / 57 |
| Tras arreglar usePlans | 9 | 48 / 57 |
| Tras arreglar useAgentRun | 0 | 57 / 57 |

## 2. Los 6 fallos de la IA

| # | Hook | Fallo | Arreglo |
|---|---|---|---|
| 1 | useDebounce | No borraba el temporizador anterior | Limpiar con `clearTimeout` en el efecto |
| 2 | usePlans | Si fallaba, se quedaba cargando | Pasar al estado de error |
| 3 | usePlans | Una respuesta vieja pisaba a la nueva | Ignorarla con `cancelled` |
| 4 | useAgentRun | Un `return` antes de los hooks | Poner todos los hooks arriba |
| 5 | useAgentRun | Un plan R2 se aplicaba sin confirmar | Esperar a `approve()` |
| 6 | useAgentRun | No cancelaba al cerrar el componente | Llamar a `abort()` al desmontar |

## 3. Preguntas 

### useDebounce
1. **¿Hooks en orden y arriba?** 

- Sí.

2. **¿Limpia los efectos?**

 - No, dejaba temporizadores vivos. Ya está arreglado.

3. **¿Tres estados?** 

- No aplica, porque no pide datos.

4. **¿El dato está en el lugar correcto?**

 - Sí, en `Inbox`, que es quien lo usa.


### usePlans

1. **¿Hooks en orden y arriba?**
 - Sí.

2. **¿Limpia los efectos?**

 - No, no ignoraba respuestas viejas. Ya está arreglado.

3. **¿Tres estados?** 

- No, el error no se mostraba. Ya está 
arreglado.

4. **¿El dato está en el lugar correcto?**

 - Sí, en `App`, porque lo usan `Header` e `Inbox`.

### useAgentRun

1. **¿Hooks en orden y arriba?**

 - No, había un `return` antes. Ya está arreglado.

2. **¿Limpia los efectos?** 

- No, no cancelaba al cerrar. Ya está arreglado.

3. **¿Tres estados?** 

- Sí, pero el R2 se saltaba la confirmación. Ya está arreglado.

4. **¿El dato está en el lugar correcto?**

 - Sí, en `RunPanel`, que es quien lo usa.

## 4. Árbol de componentes

```
App  [plans, decisions, failing]
├── Header ← pendingCount
├── PlansSkeleton   (cargando)
├── ErrorBanner ← error, onRetry   (error)
└── Inbox ← plans, decisions, onDecide
    │   [query] · useDebounce
    ├── PlanCard ← plan, onDecide
    └── RunPanel ← approvedPlans
          [ejecución] · useAgentRun
```

`[ ]` = dato propio · `←` = lo recibe del padre

**¿Por qué el contador vive en App?**

 Porque lo usan dos hermanos, `Header` e `Inbox`, y solo su padre común puede compartirlo.

## 5. ¿Por qué la interfaz no es la frontera de seguridad?

Porque cualquiera puede saltarse los botones desde el navegador o llamando directo a la API. La pantalla solo ayuda a decidir bien; el que de verdad debe bloquear un plan peligroso es el servidor.
