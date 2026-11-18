# The Illusion of Transit Equity

**Replication Data and Code Repository**  
This repository contains the spatial econometric workflows, CBG-level output tables, data dictionaries, and replication scripts for the manuscript:  
*"The Illusion of Transit Equity: Evaluating Spatial Poverty Mismatches and Neighboring Transit Supply Across Three U.S. Metropolitan Archetypes"* (Submitted to *Cities*).

## Overview
This study evaluates the local bivariate spatial association between Census Block Group (CBG) poverty rates (`Poverty_Rate`, income-to-poverty ratio < 1.00) and neighboring public transit supply (`TrAccess_Index`) across boundary-stable 2010–2020 subsets ($N = 8,085$ CBGs) of three contrasting U.S. Metropolitan Statistical Areas (MSAs):
- **Chicago-Naperville-Elgin, IL-IN-WI** (Monocentric legacy network): $n = 5,537$ retained of $6,592$ populated 2010 CBGs ($84.0\%$ retention).
- **Atlanta-Sandy Springs-Alpharetta, GA** (Fragmented Sunbelt region): $n = 1,059$ retained of $2,589$ populated 2010 CBGs ($40.9\%$ retention).
- **Houston-The Woodlands-Sugar Land, TX** (Unzoned polycentric system): $n = 1,489$ retained of $3,039$ populated 2010 CBGs ($49.0\%$ retention).

Moving beyond global correlation metrics, the framework executes Lee's (2001) Bivariate Spatial Association ($L_i$) to isolate localized **High-Poverty / Low-Supply (`High-Low`)** spatial outliers (comprising $473$ core focal high-poverty mismatches and $161$ contiguous boundary spillover polygons across the $634$ total `High-Low` units) to support Title VI service-equity screening.

## Data Sources
1. **Socio-Economic Data:** U.S. Census Bureau, 2020–2024 American Community Survey (ACS) 5-Year Estimates ([Table C17002: Ratio of Income to Poverty Level](https://api.census.gov/data/2024/acs/acs5/groups/C17002.html)).
   - Computed as `Poverty_Rate = 100 * (C17002_002E + C17002_003E) / C17002_001E` for populated CBGs (`C17002_001E > 0`).
2. **Transit Supply Data:** U.S. Environmental Protection Agency (EPA) [Smart Location Database (SLD v3.0)](https://www.epa.gov/smartgrowth/smart-location-mapping) (circa-2020 GTFS schedules tabulated on 2010 Census CBG `GEOID10` geometries).
   - Variables used: `D4a` (pedestrian network distance from population-weighted centroid to nearest transit stop), `D4c` (aggregate weekday evening-peak service frequency within 0.25 miles), and `D4d` (aggregate frequency per square mile), min–max normalized across the pooled retained sample and averaged with equal weights ($1/3$ each) into `TrAccess_Index` (geodatabase alias: `AuthorComposite_TransitSupply`).

## Methodology & Software Specification
- **Software Environment:** Python 3.11 / ArcGIS Pro 3.7 (`arcpy.stats.BivariateSpatialAssociation`).
- **Coordinate Reference System:** USA Contiguous Albers Equal Area Conic (`EPSG:5070`).
- **Longitudinal Boundary Filter:** Exact 1:1 `GEOID10`–`GEOID20` matching paired with a polygon area-consistency check (area overlap ratio $\ge 0.99$) to prevent areal interpolation smoothing.
- **Spatial Econometric Statistic:** Bivariate Spatial Association (Lee's $L_i(X,Y) = \tilde{z}_i^X \cdot \tilde{z}_i^Y$), where spatial lags are standardized within each retained MSA subset using population standard deviations ($\text{ddof} = 0$) and include the focal unit within its own smoothing neighborhood.
- **Spatial Weights Matrix ($W$):** Row-standardized (`ROW`) first-order Queen contiguity (`CONTIGUITY_EDGES_CORNERS`) supplemented by nearest-neighbor fallback for isolated boundary-stable polygons (`NUM_NBRS` $\ge 1$).
- **Inference & Permutations:** 999 conditional random permutations (`arcpy.env.randomGenerator = "42 MERSENNE_TWISTER"`). The exported `P_VALUE` column reports the two-sided pseudo-$p$ value (minimum bound $= 0.002$), while `ASSOC_CAT` assigns cluster categories at the ArcGIS Pro one-sided permutation threshold of $p_{\text{one-sided}} \le 0.05$ (corresponding to two-sided `P_VALUE <= 0.100`).

## Data Dictionary (Exported CSV Schema)
Each metropolitan CSV file in `/data` contains $9$ fields indexed by sequential within-subset identifier `SOURCE_ID`:

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `SOURCE_ID` | Integer | Sequential within-subset feature identifier ($1 \dots n$). |
| `Poverty_Rate` | Float | Unsmoothed CBG poverty rate ($\%$, income-to-poverty ratio $< 1.00$, ACS 2020–2024). |
| `TrAccess_Index` | Float | Unsmoothed composite local transit supply score ($[0.000, 1.000]$, EPA SLD v3.0 `D4a`, `D4c`, `D4d`). |
| `LOCAL_L` | Float | Local Bivariate Spatial Association statistic (Lee's $L_i = \tilde{z}_i^X \cdot \tilde{z}_i^Y$). |
| `NWA_VAR1` | Float | Neighbor-weighted average (spatial lag) of `Poverty_Rate
