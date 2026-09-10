# ChipWise architecture

```mermaid
flowchart LR
    A[OoC experiment records] --> B[Schema validation]
    E[Public study provenance] --> F[Evidence catalog]
    B --> C[Gaussian Process model]
    C --> D[Mean + uncertainty]
    D --> G[Active-learning acquisition]
    G --> H[Ranked next experiment]
    H --> A
    F --> I[Human review + context]
    D --> I
    H --> I
```

The evidence catalog and the synthetic quantitative model are deliberately separated. Public-study metadata grounds the use case and provenance; synthetic values demonstrate the closed-loop planner without misrepresenting literature measurements.
