import arcpy
import os

# ==============================================================================
# Bivariate Spatial Association (Lee's L) Workflow
# Manuscript: The Illusion of Transit Equity
# Target Journal: Cities (Elsevier)
# ==============================================================================

# 1. Environment Setup
arcpy.env.overwriteOutput = True
arcpy.env.randomGenerator = "42"  # Fixed random seed for exact reproducibility (as stated in manuscript)

# Define workspace (Update with actual local paths if running locally)
workspace = r"C:\GIS_Projects\TransitEquity\TransitEquity.gdb"
arcpy.env.workspace = workspace

# Input boundary-stable subsets (Projected to EPSG:5070 - USA Contiguous Albers Equal Area Conic)
cities = {
    "Chicago": "Chicago_Retained_CBGs_2024_EPSG5070",
    "Atlanta": "Atlanta_Retained_CBGs_2024_EPSG5070",
    "Houston": "Houston_Retained_CBGs_2024_EPSG5070"
}

# 2. Variable Definitions
# X (Focal Variable): Poverty Rate (< 1.00 Ratio)
var_x = "Poverty_Rate_PCT" 

# Y (Lagged Neighboring Variable): Author-defined Transit Supply Composite (D4a, D4c, D4d)
var_y = "AuthorComposite_TransitSupply"

# 3. Spatial Econometric Execution
def run_bivariate_lees_L():
    print("Starting Bivariate Spatial Association (Lee's L) Analysis...")
    
    for city, feature_class in cities.items():
        print(f"\nProcessing {city} subset...")
        
        output_fc = f"{feature_class}_LeesL_Output"
        
        try:
            # Execute arcpy.stats.BivariateSpatialAssociation
            arcpy.stats.BivariateSpatialAssociation(
                in_features=feature_class,
                x_field=var_x,
                y_field=var_y,
                out_features=output_fc,
                conceptualization_of_spatial_relationships="K_NEAREST_NEIGHBORS",
                distance_band=None,
                number_of_neighbors=8,             # k = 8 (Excludes focal CBG internally in ArcGIS Pro)
                standardization="ROW",             # Row-standardized weights matrix
                number_of_permutations=999,        # Yields minimum two-sided p-value = 0.002
                fdr_correction="NONE"              # Nominal alpha = 0.05 without FDR (as stated in methodology)
            )
            print(f"[SUCCESS] Local Spatial Association Category field generated for {city}.")
            print(f"Output saved to: {output_fc}")
            
        except arcpy.ExecuteError:
            print(f"[ERROR] Failed to process {city}.")
            print(arcpy.GetMessages(2))

if __name__ == "__main__":
    run_bivariate_lees_L()
    print("\nWorkflow completed successfully.")