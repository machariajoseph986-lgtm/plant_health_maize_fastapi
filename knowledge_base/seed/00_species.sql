-- Base species reference data
-- These records depend on the plant records in 00_plants.sql.

INSERT INTO public.species
    (species_id, plant_id, scientific_name, common_name)
VALUES
    ('SPECIES_COFFEE_ARABICA', 'PLANT_COFFEE', 'Coffea arabica', 'Arabica coffee'),
    ('SPECIES_COFFEE_CANEphora', 'PLANT_COFFEE', 'Coffea canephora', 'Robusta coffee'),
    ('SPECIES_MAIZE', 'PLANT_MAIZE', 'Zea mays', 'Maize'),
    ('SPECIES_POTATO', 'PLANT_POTATO', 'Solanum tuberosum', 'Potato'),
    ('SPECIES_TEA', 'PLANT_TEA', 'Camellia sinensis', 'Tea')
ON CONFLICT (species_id) DO NOTHING;
