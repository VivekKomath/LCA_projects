import numpy as np
import pandas as pd

# Set pandas display options to show all columns and prevent line wrapping
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def biodiesel_raw_materials(required_kg_biodiesel):
    # Molar masses (g/mol)
    M_triolein = 885.44
    M_ethanol = 46.07
    M_biodiesel = 296.50  # Ethyl oleate
    M_glycerol = 92.09

    # Reaction: 1 mol triolein + 3 mol ethanol -> 3 mol biodiesel + 1 mol glycerol
    moles_biodiesel = required_kg_biodiesel * 1000 / M_biodiesel
    moles_triolein = moles_biodiesel / 3
    moles_ethanol = moles_triolein * 3
    moles_glycerol = moles_triolein

    # Masses in kg
    mass_triolein = moles_triolein * M_triolein / 1000
    mass_ethanol = moles_ethanol * M_ethanol / 1000
    mass_glycerol = moles_glycerol * M_glycerol / 1000

    return mass_triolein, mass_ethanol, mass_glycerol


raw_materials_df = pd.read_csv('raw_material_emissions.csv', index_col='Component',encoding='utf-8-sig')
raw_materials_df.insert(0, 'Value', 0)

utilities_df = pd.read_csv('utility_emissions.csv', index_col='Component', encoding='utf-8-sig')
utilities_df.insert(0, 'Value', 0)

products_df = pd.DataFrame(columns=raw_materials_df.columns)



# Functional unit: 1 kg of biodiesel
required_kg_biodiesel = 1
mass_triolein, mass_ethanol, mass_glycerol = biodiesel_raw_materials(required_kg_biodiesel)
raw_materials_df.loc['Triolein', 'Value'] = mass_triolein
raw_materials_df.loc['Bio-ethanol', 'Value'] = mass_ethanol

results_triolein = raw_materials_df.loc['Triolein']* raw_materials_df.loc['Triolein', 'Value']
results_bio_ethanol = raw_materials_df.loc['Bio-ethanol']* raw_materials_df.loc['Bio-ethanol', 'Value']
total_emissions = results_triolein + results_bio_ethanol

mass_allocation_glycerol = mass_glycerol / (mass_glycerol + required_kg_biodiesel)
mass_allocation_biodiesel = required_kg_biodiesel / (mass_glycerol + required_kg_biodiesel)
mass_results_glycerol = total_emissions * mass_allocation_glycerol
mass_results_biodiesel = total_emissions * mass_allocation_biodiesel

# Store the allocated results in the products_df DataFrame
products_df.loc['Biodiesel'] = mass_results_biodiesel
products_df.loc['Glycerol'] = mass_results_glycerol
products_df.at['Biodiesel', 'Value'] = required_kg_biodiesel
products_df.at['Glycerol', 'Value'] = mass_glycerol

products_df.at['Biodiesel', 'Cost (USD)'] = 1.4
products_df.at['Glycerol', 'Cost (USD)'] = 1



print("--- Allocated Emissions for Products ---")
print(products_df)