# How QSO Graph Works

!!! note "Specification version"
    This page documents **QSO-GRAPH-SPEC v1.0**. The specification itself is authoritative:
    [qso-graph-spec at v1.0](https://github.com/qso-graph/qso-graph-spec/tree/v1.0). Where this
    summary and the specification differ, the specification wins.

QSO Graph follows the model of W1HKJ's fldigi suite: small, focused programs that each do one thing, share conventions, and keep going as contributors come and go. **Every tool stands alone. Together they compose.**

The rules are the eight pillars in [PILLARS.md](https://github.com/qso-graph/qso-graph-spec/blob/v1.0/PILLARS.md). Each one comes with a test a reviewer can apply to a change.

| Pillar | The rule | The test |
|:-------|:---------|:---------|
| **P1** | We don't break the NCS mid-net | Can this change interrupt, stall or steal focus from an operator running a net? |
| **P2** | No private definition of anything ADIF defines | Does this add a rule for something ADIF already specifies? Could an operator move to another logger and keep everything that matters? |
| **P3** | Adding a club must not require touching the engine | Does supporting a new club need a code change? |
| **P4** | Delete every wrapper and the build still works | Does the build succeed from plain CMake alone? |
| **P5** | Nothing ships that we cannot build from source ourselves | For each dependency: who built it, can we verify it, could we rebuild it? |
| **P6** | Every tool stands alone | Installed with none of the others, is it fully useful? |
| **P7** | Design for the median maintainer | Could someone with no prior context get from a clean machine to a working build by following what is written? |
| **P8** | Published facts only; no characterisation | Does this sentence state something measurable, or pass judgement on someone? |

To cite a rule, give the version and the pillar, for example *QSO-GRAPH-SPEC v1.0, PILLARS.md P2*.

## ADIF is the anchor

[ADIF](https://adif.org/) is the data model for everything here. Where ADIF defines a field, ADIF's definition is the one that ships. QSO Graph's own fields are extensions that only add to ADIF and never stand in for a field ADIF already defines (P2).

## Contracts, not shared code

The products run on different stacks (a Qt desktop app, Python services, the MCP servers), because they do different jobs. What they share is the contract: ADIF, published interfaces, and shared reference data. Nothing requires another product to be installed (P6).

## Governance

The specification changes through its own [process](https://github.com/qso-graph/qso-graph-spec/tree/v1.0/governance).
