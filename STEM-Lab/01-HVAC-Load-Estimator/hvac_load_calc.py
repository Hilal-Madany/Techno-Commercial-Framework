# ==========================================================
# Project: Mech-Flow HVAC Load Estimator (Verified v1.1)
# Author: Syed Hilaluddin Madany | hilalmadany.com
# ==========================================================

import math

def calculate_hvac_load():
    print("--- 🛠️ Industrial HVAC Load Estimator ---")
    
    try:
        # User Inputs
        area = float(input("Enter Room Area (sq. ft): "))
        occupants = int(input("Number of Occupants: "))
        equipment_wattage = float(input("Total Equipment Wattage (Watts): "))
        
        # Engineering Logic (ASHRAE Base Standards)
        area_load = area * 20
        occupant_load = occupants * 400
        equipment_load = equipment_wattage * 3.41
        
        total_btu = area_load + occupant_load + equipment_load
        tonnage = total_btu / 12000 
        
        # Commercial Selection Logic
        # (Standard AC units come in 0.5 increments: 1.0, 1.5, 2.0...)
        recommended_unit = math.ceil(tonnage * 2) / 2
        
        # Output Formatting
        print("\n" + "═"*40)
        print(f"📊 CALCULATION RESULTS")
        print("═"*40)
        print(f"Total Heat Load  : {total_btu:,.2f} BTU/hr")
        print(f"Calculated TR    : {tonnage:.2f} TR")
        print(f"Commercial Match : {recommended_unit:.1f} Ton Unit")
        print("═"*40)
        print("✅ Verified by: Syed Hilaluddin Madany")

    except ValueError:
        print("❌ Error: Invalid input. Please enter numbers only.")

if __name__ == "__main__":
    calculate_hvac_load()
