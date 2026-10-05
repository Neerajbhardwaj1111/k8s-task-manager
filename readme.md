                         Internet / Browser
                                │
                                ▼
                       ┌──────────────────┐
                       │ frontend-service │
                          Internet / Browser
                                │
                                ▼
                       ┌──────────────────┐
                       │ frontend-service │
                       │     NodePort     │
                       └────────┬─────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
             Frontend Pod             Frontend Pod
                    │
                    │ /api
                    ▼
             ┌─────────────────┐
             │ backend-service │
             │    ClusterIP    │
             └────────┬────────┘
                      │
             ┌────────┴────────┐
             ▼                 ▼
       Backend Pod        Backend Pod
             │                 │
             ├─────────────────┤
             │
       ┌─────┴──────┐
       ▼            ▼
postgres-service  redis-service
       │            │
       ▼            ▼
 PostgreSQL        Redis
       │
       ▼
 Persistent
   Storage                      │     NodePort     │
                       └────────┬─────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
             Frontend Pod             Frontend Pod
                    │
                    │ /api
                    ▼
             ┌─────────────────┐
             │ backend-service │
             │    ClusterIP    │
             └────────┬────────┘
                      │
             ┌────────┴────────┐
             ▼                 ▼
       Backend Pod        Backend Pod
             │                 │
             ├─────────────────┤
             │
       ┌─────┴──────┐
       ▼            ▼
postgres-service  redis-service
       │            │
       ▼            ▼
 PostgreSQL        Redis
       │
       ▼
 Persistent
   Storage