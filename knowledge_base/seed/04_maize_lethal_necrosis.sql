-- Maize Lethal Necrosis (MLN) knowledge-base seed
-- Health problem: HP_MAIZE_MLN

INSERT INTO public.health_problems
    (health_problem_id, plant_id, name, type, description)
VALUES
    (
        'HP_MAIZE_MLN',
        'PLANT_MAIZE',
        'Maize Lethal Necrosis',
        'viral',
        'A serious viral disease of maize associated with co-infection by maize chlorotic mottle virus and a virus from the Potyviridae family.'
    )
ON CONFLICT (health_problem_id) DO NOTHING;

INSERT INTO public.pathogens
    (pathogen_id, health_problem_id, scientific_name, type, role)
VALUES
    (
        'PATH_MAIZE_MLN_MCMV',
        'HP_MAIZE_MLN',
        'Maize chlorotic mottle virus',
        'virus',
        'Co-infecting virus associated with MLN'
    ),
    (
        'PATH_MAIZE_MLN_MDMV',
        'HP_MAIZE_MLN',
        'Maize dwarf mosaic virus',
        'virus',
        'Potyvirus that can occur as a cereal-virus component of MLN'
    ),
    (
        'PATH_MAIZE_MLN_SCMV',
        'HP_MAIZE_MLN',
        'Sugarcane mosaic virus',
        'virus',
        'Potyvirus that can co-infect maize with MCMV and contribute to MLN'
    )
ON CONFLICT (pathogen_id) DO NOTHING;

INSERT INTO public.symptoms
    (symptom_id, health_problem_id, category, description)
VALUES
    (
        'SYM_MAIZE_MLN_EARLY',
        'HP_MAIZE_MLN',
        'early',
        'Long yellow stripes appear on maize leaves.'
    ),
    (
        'SYM_MAIZE_MLN_PROGRESSION',
        'HP_MAIZE_MLN',
        'progression',
        'Leaves become yellow and dry from the outer edges toward the midrib.'
    ),
    (
        'SYM_MAIZE_MLN_PLANT',
        'HP_MAIZE_MLN',
        'plant',
        'Plants may become dwarfed and show premature aging.'
    ),
    (
        'SYM_MAIZE_MLN_ADVANCED',
        'HP_MAIZE_MLN',
        'advanced',
        'The entire plant may dry out and die.'
    ),
    (
        'SYM_MAIZE_MLN_REPRODUCTIVE',
        'HP_MAIZE_MLN',
        'reproductive',
        'Late-infected plants may fail to tassel and produce poorly filled cobs.'
    )
ON CONFLICT (symptom_id) DO NOTHING;

INSERT INTO public.transmission
    (transmission_id, health_problem_id, method, description)
VALUES
    (
        'TRANS_MAIZE_MLN_VECTORS',
        'HP_MAIZE_MLN',
        'insect_vectors',
        'Disease-causing viruses can be transmitted by insect vectors including thrips, aphids, leafhoppers and beetles.'
    ),
    (
        'TRANS_MAIZE_MLN_SEED',
        'HP_MAIZE_MLN',
        'seed',
        'Seed can contribute to transmission, particularly for maize chlorotic mottle virus.'
    )
ON CONFLICT (transmission_id) DO NOTHING;

INSERT INTO public.conditions
    (condition_id, health_problem_id, factor, value, description)
VALUES
    (
        'COND_MAIZE_MLN_CONTINUOUS',
        'HP_MAIZE_MLN',
        'cropping_pattern',
        'continuous maize',
        'Continuous maize production can contribute to disease pressure.'
    ),
    (
        'COND_MAIZE_MLN_VECTOR_MOVEMENT',
        'HP_MAIZE_MLN',
        'vector_movement',
        'wind',
        'Wind can contribute to movement of insect vectors between maize plants and fields.'
    )
ON CONFLICT (condition_id) DO NOTHING;

INSERT INTO public.management
    (management_id, health_problem_id, category, action)
VALUES
    (
        'MGMT_MAIZE_MLN_ROTATION',
        'HP_MAIZE_MLN',
        'crop_rotation',
        'Use crop rotation to reduce disease pressure and interrupt conditions that favour continued virus transmission.'
    ),
    (
        'MGMT_MAIZE_MLN_DIVERSIFICATION',
        'HP_MAIZE_MLN',
        'crop_diversification',
        'Use crop diversification where appropriate to reduce reliance on continuous maize production.'
    ),
    (
        'MGMT_MAIZE_MLN_FIELD_SELECTION',
        'HP_MAIZE_MLN',
        'field_selection',
        'Select fields with appropriate drainage and avoid sites with a known history of severe MLN pressure where practical.'
    ),
    (
        'MGMT_MAIZE_MLN_HYGIENE',
        'HP_MAIZE_MLN',
        'field_hygiene',
        'Maintain field hygiene and remove or manage infected plants according to local MLN management guidance.'
    ),
    (
        'MGMT_MAIZE_MLN_VARIETY',
        'HP_MAIZE_MLN',
        'variety_selection',
        'Use maize varieties with appropriate resistance or tolerance to MLN where available.'
    )
ON CONFLICT (management_id) DO NOTHING;

INSERT INTO public.chemical_management
    (
        health_problem_id,
        treatment_type,
        chemical_role,
        active_ingredient,
        chemical_class,
        application_timing,
        application_guidance,
        resistance_management,
        safety_notes,
        source_id
    )
VALUES
    (
        'HP_MAIZE_MLN',
        'No chemical cure',
        'Disease management',
        NULL,
        NULL,
        'Not applicable',
        'There is no chemical treatment that cures MLN because it is a viral disease.',
        NULL,
        'Do not treat vector-control insecticides as a cure for MLN. Follow registered product labels for any insecticide use.',
        NULL
    ),
    (
        'HP_MAIZE_MLN',
        'Seed treatment',
        'Vector management',
        'Imidacloprid',
        'Neonicotinoid',
        'Before planting',
        'Use only a registered seed-treatment formulation according to its product label.',
        'Use integrated vector management and rotate insecticide modes of action where appropriate.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_MAIZE_MLN',
        'Seed treatment',
        'Vector management',
        'Thiamethoxam',
        'Neonicotinoid',
        'Before planting',
        'Use only a registered seed-treatment formulation according to its product label.',
        'Use integrated vector management and rotate insecticide modes of action where appropriate.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_MAIZE_MLN',
        'Foliar insecticide',
        'Vector management',
        'Lambda-cyhalothrin',
        'Pyrethroid',
        'When vector pressure warrants treatment',
        'Use a registered formulation according to the product label and local recommendations.',
        'Rotate insecticide modes of action where appropriate to reduce resistance risk.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_MAIZE_MLN',
        'Foliar insecticide',
        'Vector management',
        'Diazinon',
        'Organophosphate',
        'When vector pressure warrants treatment',
        'Use a registered formulation according to the product label and local recommendations.',
        'Rotate insecticide modes of action where appropriate to reduce resistance risk.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_MAIZE_MLN',
        'Foliar insecticide',
        'Vector management',
        'Malathion',
        'Organophosphate',
        'When vector pressure warrants treatment',
        'Use a registered formulation according to the product label and local recommendations.',
        'Rotate insecticide modes of action where appropriate to reduce resistance risk.',
        'Follow the registered product label and required protective measures.',
        NULL
    );

INSERT INTO public.sources
    (source_id, health_problem_id, organization, title, url, accessed_date)
VALUES
    (
        'SRC_MAIZE_MLN_PLANTWISE',
        'HP_MAIZE_MLN',
        'Plantwise Plus Knowledge Bank',
        'Prevention and detection of Maize Lethal Necrosis Disease',
        'https://plantwiseplusknowledgebank.org/doi/full/10.1079/pwkb.20157800329',
        NULL
    ),
    (
        'SRC_MAIZE_MLN_BIOVISION',
        'HP_MAIZE_MLN',
        'Infonet Biovision',
        'Maize lethal necrosis (MLN)',
        'https://infonet-biovision.org/PlantHealth/MinorPests/maize-lethal-necrosis-mln',
        NULL
    )
ON CONFLICT (source_id) DO NOTHING;
