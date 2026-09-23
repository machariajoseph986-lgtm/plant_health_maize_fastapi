-- Base plant reference data
-- These records must exist before disease knowledge-base seeds are loaded.

INSERT INTO public.plants
    (plant_id, common_name, genus, family)
VALUES
    ('PLANT_MAIZE', 'Maize', 'Zea', 'Poaceae'),
    ('PLANT_COFFEE', 'Coffee', 'Coffea', 'Rubiaceae'),
    ('PLANT_POTATO', 'Potato', 'Solanum', 'Solanaceae'),
    ('PLANT_TEA', 'Tea', 'Camellia', 'Theaceae')
ON CONFLICT (plant_id) DO NOTHING;
