# FINAL PROJECT

+++ {"part": "abstract"}

This project studies collusion dynamics in procurement auction markets using an
agent-based simulation model. Firms repeatedly interact in auctions, forming co-bidding
networks that reveal patterns of interaction. We analyze the distribution of detected
groups in the coherence–exclusivity feature space and examine how these structural
properties relate to the emergence of collusion.

+++

```{raw} latex
\clearpage
```

The simulation generates repeated auction interactions between firms and issuers. From
these interactions we construct co-bidding networks and detect groups of firms. For each
group we compute two structural measures: **coherence**, which captures the intensity
and balance of interactions within the group, and **exclusivity**, which measures how
isolated the group is from the rest of the market.

Figure :A\` shows the distribution of detected groups across the coherence–exclusivity
space. Figure :B illustrates how the rate of collusion varies across this feature space.

```{figure} ../bld/figures/figure_a.png
---
width: 85%
label: fig:distribution
---
(A) The distribution of groups observed from the resulting co-bidding networks
in the binned coherence-exclusivity feature space.
```

```{figure} ../bld/figures/figure_b.png
---
width: 85%
label: fig:collusion
---
(B) The rate of collusion by groups with given coherence-exclusivity.
The model suggests that high coherence and exclusivity groups are not
common, but that they have significantly higher rates of collusion.
```
