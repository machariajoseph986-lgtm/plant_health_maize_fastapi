-- Tea Blister Blight knowledge-base seed
-- Health problem: HP_TEA_BLISTER_BLIGHT

INSERT INTO public.health_problems
    (health_problem_id, plant_id, name, type, description)
VALUES
    (
        'HP_TEA_BLISTER_BLIGHT',
        'PLANT_TEA',
        'Tea Blister Blight',
        'fungal',
        'A serious foliar disease of tea caused by the obligate biotrophic fungus Exobasidium vexans, mainly affecting young succulent leaves and shoots.'
    )
ON CONFLICT (health_problem_id) DO NOTHING;

INSERT INTO public.pathogens
    (pathogen_id, health_problem_id, scientific_name, type, role)
VALUES
    (
        'PATH_TEA_BLISTER_BLIGHT_E_VEXANS',
        'HP_TEA_BLISTER_BLIGHT',
        'Exobasidium vexans',
        'fungus',
        'Causal organism of tea blister blight'
    )
ON CONFLICT (pathogen_id) DO NOTHING;

INSERT INTO public.symptoms
    (symptom_id, health_problem_id, category, description)
VALUES
    (
        'SYM_TEA_BLISTER_BLIGHT_EARLY',
        'HP_TEA_BLISTER_BLIGHT',
        'early',
        'Small pinhole-sized spots appear on young leaves.'
    ),
    (
        'SYM_TEA_BLISTER_BLIGHT_LEAF',
        'HP_TEA_BLISTER_BLIGHT',
        'leaf',
        'Spots enlarge and become transparent, light brown or pinkish translucent areas.'
    ),
    (
        'SYM_TEA_BLISTER_BLIGHT_BLISTER',
        'HP_TEA_BLISTER_BLIGHT',
        'leaf',
        'White and velvety blister-like lesions develop on the lower leaf surface.'
    ),
    (
        'SYM_TEA_BLISTER_BLIGHT_ADVANCED',
        'HP_TEA_BLISTER_BLIGHT',
        'advanced',
        'Blister lesions become brown and infected leaf tissue may become necrotic.'
    ),
    (
        'SYM_TEA_BLISTER_BLIGHT_SHOOT',
        'HP_TEA_BLISTER_BLIGHT',
        'shoot',
        'Young infected stems may become bent, distorted, break off or die.'
    )
ON CONFLICT (symptom_id) DO NOTHING;

INSERT INTO public.transmission
    (transmission_id, health_problem_id, method, description)
VALUES
    (
        'TRANS_TEA_BLISTER_BLIGHT_WIND',
        'HP_TEA_BLISTER_BLIGHT',
        'wind',
        'Wind can disperse fungal spores between infected and healthy tea tissues.'
    ),
    (
        'TRANS_TEA_BLISTER_BLIGHT_WATER',
        'HP_TEA_BLISTER_BLIGHT',
        'water',
        'Water and prolonged wetness can contribute to disease spread and infection.'
    )
ON CONFLICT (transmission_id) DO NOTHING;

INSERT INTO public.conditions
    (condition_id, health_problem_id, factor, value, description)
VALUES
    (
        'COND_TEA_BLISTER_BLIGHT_HUMIDITY',
        'HP_TEA_BLISTER_BLIGHT',
        'relative_humidity',
        '>80%',
        'High relative humidity favours blister blight development.'
    ),
    (
        'COND_TEA_BLISTER_BLIGHT_TEMPERATURE',
        'HP_TEA_BLISTER_BLIGHT',
        'temperature',
        '20-25 C',
        'Temperatures around 20-25 C can favour disease development.'
    ),
    (
        'COND_TEA_BLISTER_BLIGHT_WETNESS',
        'HP_TEA_BLISTER_BLIGHT',
        'leaf_wetness',
        'prolonged moisture',
        'Prolonged leaf moisture favours infection and disease development.'
    )
ON CONFLICT (condition_id) DO NOTHING;

INSERT INTO public.management
    (management_id, health_problem_id, category, action)
VALUES
    (
        'MGMT_TEA_BLISTER_BLIGHT_PRUNING',
        'HP_TEA_BLISTER_BLIGHT',
        'pruning',
        'Use appropriate pruning and canopy management to improve airflow and reduce prolonged leaf wetness.'
    ),
    (
        'MGMT_TEA_BLISTER_BLIGHT_FUNGICIDE',
        'HP_TEA_BLISTER_BLIGHT',
        'fungicide',
        'Use registered fungicides according to local recommendations and product labels when chemical protection is appropriate.'
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
        'HP_TEA_BLISTER_BLIGHT',
        'Fungicide',
        'Protectant',
        'Copper oxychloride',
        'Copper-based protectant',
        'During disease-favourable wet periods according to local recommendations',
        'Use a registered copper oxychloride formulation according to the product label and local recommendations.',
        'Rotate with fungicides having different modes of action where appropriate.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_TEA_BLISTER_BLIGHT',
        'Fungicide',
        'Protectant',
        'Copper hydroxide',
        'Copper-based protectant',
        'During disease-favourable wet periods according to local recommendations',
        'Use a registered copper hydroxide formulation according to the product label and local recommendations.',
        'Rotate with fungicides having different modes of action where appropriate.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_TEA_BLISTER_BLIGHT',
        'Fungicide',
        'Protectant',
        'Copper oxide',
        'Copper-based protectant',
        'During disease-favourable wet periods according to local recommendations',
        'Use a registered copper oxide formulation according to the product label and local recommendations.',
        'Rotate with fungicides having different modes of action where appropriate.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_TEA_BLISTER_BLIGHT',
        'Fungicide',
        'Systemic',
        'Hexaconazole',
        'Systemic fungicide',
        'During disease-favourable periods according to local recommendations',
        'Use a registered hexaconazole formulation according to the product label and local recommendations.',
        'Alternate systemic fungicides with protectant fungicides where appropriate to reduce resistance risk.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_TEA_BLISTER_BLIGHT',
        'Fungicide',
        'Systemic',
        'Propiconazole',
        'Triazole (DMI)',
        'During disease-favourable periods according to local recommendations',
        'Use a registered propiconazole formulation according to the product label and local recommendations.',
        'Alternate systemic fungicides with protectant fungicides where appropriate to reduce resistance risk.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_TEA_BLISTER_BLIGHT',
        'Fungicide',
        'Systemic',
        'Bitertanol',
        'Triazole (DMI)',
        'During disease-favourable periods according to local recommendations',
        'Use a registered bitertanol formulation according to the product label and local recommendations.',
        'Alternate systemic fungicides with protectant fungicides where appropriate to reduce resistance risk.',
        'Follow the registered product label and required protective measures.',
        NULL
    )
ON CONFLICT (chemical_management_id) DO NOTHING;

INSERT INTO public.sources
    (source_id, health_problem_id, organization, title, url, accessed_date)
VALUES
    (
        'SRC_TEA_BLISTER_BLIGHT_TNAU',
        'HP_TEA_BLISTER_BLIGHT',
        'Tamil Nadu Agricultural University',
        'Tea - Blister blight',
        'https://agritech.tnau.ac.in/crop_protection/tea_diseases_3.html',
        NULL
    ),
    (
        'SRC_TEA_BLISTER_BLIGHT_INTECHOPEN',
        'HP_TEA_BLISTER_BLIGHT',
        'IntechOpen',
        'Blister Blight Disease of Tea: An Enigma',
        'https://www.intechopen.com/chapters/74600',
        NULL
    )
ON CONFLICT (source_id) DO NOTHING;
