# Attributions

**QSO-Graph exists because of the services, data, and standards built by these organizations and individuals. We are grateful for their work.**

---

## Standards

### ADIF Specification (adif-mcp)

The [Amateur Data Interchange Format](https://adif.org.uk/) is the foundation of amateur radio logging interoperability. adif-mcp bundles the complete ADIF 3.1.6 specification — 186 fields, 26 enumerations, and 28 data types.

- **Author**: Joe Turley, G3ZOD (R.G. Turley OBE)
- **Website**: [adif.org.uk](https://adif.org.uk/)
- **Test corpus**: [CreateADIFTestFiles](https://github.com/g3zod/CreateADIFTestFiles) by G3ZOD — 6,191 records exercising every enumeration value

---

## Logbook Services

### eQSL.cc (eqsl-mcp)

Electronic QSL card exchange and confirmation service. eqsl-mcp wraps the eQSL inbox, QSO verification, Authenticity Guaranteed (AG) member list, and last upload status.

- **Operator**: Dave Morris, N5UP
- **Website**: [eqsl.cc](https://www.eqsl.cc/)

### QRZ.com (qrz-mcp)

The world's largest callsign database. qrz-mcp uses both the XML API (callsign lookup, DXCC resolution) and the Logbook API (QSO fetch, logbook status).

- **Operator**: Fred Lloyd, AA7BQ
- **Website**: [qrz.com](https://www.qrz.com/)
- **XML API**: [xmldata.qrz.com](https://xmldata.qrz.com/xml/current/)
- **Logbook API**: [logbook.qrz.com](https://logbook.qrz.com/api)

### Logbook of The World (lotw-mcp)

ARRL's authoritative QSO confirmation system for award credit (DXCC, WAS, VUCC, WAZ). lotw-mcp queries confirmations, QSOs, DXCC credits, and user activity.

- **Operator**: American Radio Relay League (ARRL)
- **Website**: [lotw.arrl.org](https://lotw.arrl.org/)
- **Public data**: [LoTW User Activity CSV](https://lotw.arrl.org/lotw-user-activity.csv)

### HamQTH.com (hamqth-mcp)

Free callsign lookup, DXCC resolution, biography, recent activity, DX cluster spots, Reverse Beacon Network data, and QSO verification. A generous free-tier service for the amateur radio community.

- **Author**: Petr Hlinak, OK2CQR
- **Website**: [hamqth.com](https://www.hamqth.com/)

---

## Activation Programmes

### Parks on the Air (pota-mcp)

Portable amateur radio operations from parks and protected areas worldwide. pota-mcp queries live activator spots, park information, activator/hunter statistics, and scheduled activations.

- **Organisation**: Parks on the Air, Inc.
- **Website**: [pota.app](https://pota.app/)
- **API**: [api.pota.app](https://api.pota.app/)

### Summits on the Air (sota-mcp)

Portable amateur radio activations from mountain summits. sota-mcp queries the official SOTA API for live spots, activation alerts, summit information, and nearby summit search.

- **Organisation**: Summits on the Air (SOTA)
- **Website**: [sota.org.uk](https://www.sota.org.uk/)
- **SOTA API**: [api2.sota.org.uk](https://api2.sota.org.uk/) — spots, alerts, summit data, region listings

### Islands on the Air (iota-mcp)

Amateur radio operations from islands worldwide, administered by IOTA Ltd in partnership with the RSGB. iota-mcp provides group lookup, island search, DXCC mapping, nearby groups, and programme statistics.

- **Organisation**: IOTA Ltd / Radio Society of Great Britain (RSGB)
- **Website**: [iota-world.org](https://www.iota-world.org/)

---

## Propagation & Space Weather

### NOAA Space Weather Prediction Center (solar-mcp, ionis-mcp)

The authoritative source for space weather data. solar-mcp and ionis-mcp query solar flux index (SFI), planetary K-index (Kp), DSCOVR solar wind, X-ray flux, space weather alerts, 27-day forecasts, and HF band condition outlook.

- **Organisation**: National Oceanic and Atmospheric Administration (NOAA), Space Weather Prediction Center (SWPC)
- **Website**: [swpc.noaa.gov](https://www.swpc.noaa.gov/)
- **API**: [services.swpc.noaa.gov](https://services.swpc.noaa.gov/)
- **Note**: US government public data — no authentication, no usage restrictions

### wspr.live (wspr-mcp)

A volunteer-run public mirror of all WSPRnet data in a ClickHouse database. wspr-mcp queries this service for live spots, band activity, top beacons/spotters, propagation paths, grid activity, longest paths, and SNR trends.

- **Operator**: Arne Batelaan — a volunteer who is not a licensed amateur, maintaining this service for the community
- **Website**: [wspr.live](https://wspr.live/)
- **Database**: ~2.7 billion WSPR spots (2008-present)
- **Note**: wspr-mcp implements rate limiting (20 req/min) and a circuit breaker to respect this volunteer-run service

### WSPRnet (wspr-mcp)

The original Weak Signal Propagation Reporter network. WSPR beacons transmit 2-minute encoded signals at low power (typically 200 mW to 5 W), providing continuous automated propagation monitoring worldwide.

- **Creator**: Joe Taylor, K1JT — Nobel laureate (Physics, 1993) and creator of WSJT-X, FT8, FT4, and WSPR
- **Website**: [wsprnet.org](https://www.wsprnet.org/)

---

## Datasets (ionis-mcp)

### IONIS Propagation Datasets

ionis-mcp wraps pre-computed propagation signature datasets distributed via SourceForge. These contain 175M+ signatures derived from WSPR, RBN, Contest, and PSK Reporter observations.

- **Author**: Greg Beam, KI7MT
- **Distribution**: [sourceforge.net/projects/ionis-ai](https://sourceforge.net/projects/ionis-ai/)

---

## Tools & Frameworks

### Model Context Protocol (MCP)

The protocol that makes all of this possible — connecting AI assistants to external tools and data sources through a standardised interface.

- **Creator**: Anthropic
- **Website**: [modelcontextprotocol.io](https://modelcontextprotocol.io/)

### FastMCP

The Python framework used by all QSO-Graph servers. Clean, typed MCP server development.

- **Creator**: Jeremiah Lowin
- **Website**: [github.com/jlowin/fastmcp](https://github.com/jlowin/fastmcp)

---

## Good Neighbour Policy

QSO-Graph servers **wrap** external APIs — we don't replicate them. Every server implements rate limiting, response caching, and graceful degradation to be respectful consumers of these services. If a service goes down, we back off. We never retry in tight loops.

These services are run by volunteers, non-profits, and small organisations who serve the amateur radio community. We are guests in their house.

---

## Thank You

To every operator who uploads a QSO, every beacon that transmits, every skimmer that decodes, and every volunteer who keeps these services running — thank you. QSO-Graph is a thin layer on top of decades of community effort.

73 de KI7MT
