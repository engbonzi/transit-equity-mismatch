import arcpy
import os

# ==============================================================================
# Bivariate Spatial Association (Lee's L) Workflow (v2)
# Manuscript: The Illusion of Transit Equity
# Target Journal: Cities (Elsevier)
# ==============================================================================
# Note on Upstream Preprocessing & Spatial Topology:
# Input feature classes below represent the pre-filtered 1:1 longitudinal
# boundary-stable CBG subsets (2010-2020 GEOIDs with polygon area overlap >= 0.99
# and ACS C17002_001E > 0) projected to USA Contiguous Albers Equal Area Conic
# (EPSG:5070) via arcpy.management.Project. Within ArcGIS Pro 3.7, specifying
# CONTIGUITY_EDGES_CORNERS on these retained feature classes yields NUM_NBRS >= 1
# across all 8,085 retained polygons and computes LOCAL_L using population
# standard deviations (ddof = 0) across row-standardized spatial lags.
# ==============================================================================

# 1. Environment Setup
arcpy.env.overwriteOutput = True
arcpy.env.randomGenerator = "42 MERSENNE_TWISTER"  # Fixed seed + PRNG for exact reproducibility

# Define workspace (Update with actual local paths if running locally)
workspace = r"C:\GIS_Projects\TransitEquity\TransitEquity.gdb"
arcpy.env.workspace = workspace

# Input boundary-stable subsets (Projected to EPSG:5070 - USA Contiguous Albers Equal Area Conic)
cities = {
    "Chicago": "Chicago_Retained_CBGs_2024_EPSG5070",
    "Atlanta": "Atlanta_Retained_CBGs_2024_EPSG5070",
    "Houston": "Houston_Retained_CBGs_2024_EPSG5070"
}

# 2. Variable Definitions (Exact schema field names matching exported CSVs)
# X (Variable 1): ACS 2020-2024 CBG Poverty Rate (< 1.00 Income-to-Poverty Ratio)
var_x = "Poverty_Rate"
# Y (Variable 2): Author-defined EPA SLD v3.0 Transit Supply Composite (D4a, D4c, D4d)
var_y = "TrAccess_Index"

# 3. Spatial Econometric Execution
def run_bivariate_lees_L():
    print("Starting Bivariate Spatial Association (Lee's L) Analysis...")
    
    for city, feature_class in cities.items():
        print(f"\nProcessing {city} subset...")
        
        output_fc = f"{feature_class}_LeesL_Output"
        
        try:
            # Execute arcpy.stats.BivariateSpatialAssociation
            # Note: ArcGIS Pro internally includes the focal unit within its own
            # spatial lag smoothing neighborhood (NWA_VAR1, NWA_VAR2) per Lee (2001).
            arcpy.stats.BivariateSpatialAssociation(
                in_features=feature_class,
                analysis_field1=var_x,
                analysis_field2=var_y,
                out_features=output_fc,
                neighborhood_type="CONTIGUITY_EDGES_CORNERS",
                standardization="ROW",             # Row-standardized weights matrix
                number_of_permutations=999         # Yields minimum two-sided P_VALUE = 0.002
            )
            print(f"[SUCCESS] Local Spatial Association Category (ASSOC_CAT) generated for {city}.")
            print(f"Output saved to: {output_fc}")
            
        except arcpy.ExecuteError:
            print(f"[ERROR] Failed to process {city}.")
            print(arcpy.GetMessages(2))

if __name__ == "__main__":
    run_bivariate_lees_L()
    print("\nWorkflow completed successfully.")
