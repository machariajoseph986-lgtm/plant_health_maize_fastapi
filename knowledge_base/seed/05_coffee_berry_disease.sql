-- Coffee Berry Disease knowledge-base seed
-- Health problem: HP_COFFEE_BERRY_DISEASE

INSERT INTO public.health_problems
    (health_problem_id, plant_id, name, type, description)
VALUES
    (
        'HP_COFFEE_BERRY_DISEASE',
        'PLANT_COFFEE',
        'Coffee Berry Disease',
        'fungal',
        'A fungal disease of Arabica coffee caused by Colletotrichum kahawae, characterized by dark sunken lesions and progressive rotting of coffee berries.'
    )
ON CONFLICT (health_problem_id) DO NOTHING;

INSERT INTO public.pathogens
    (pathogen_id, health_problem_id, scientific_name, type, role)
VALUES
    (
        'PATH_COFFEE_BERRY_DISEASE_C_KAHAWAE',
        'HP_COFFEE_BERRY_DISEASE',
        'Colletotrichum kahawae',
        'fungus',
        'Causal organism of coffee berry disease'
    )
ON CONFLICT (pathogen_id) DO NOTHING;

INSERT INTO public.symptoms
    (symptom_id, health_problem_id, category, description)
VALUES
    (
        'SYM_COFFEE_BERRY_DISEASE_BERRY_EARLY',
        'HP_COFFEE_BERRY_DISEASE',
        'berry',
        'Small water-soaked lesions appear on young expanding coffee berries.'
    ),
    (
        'SYM_COFFEE_BERRY_DISEASE_BERRY_LESION',
        'HP_COFFEE_BERRY_DISEASE',
        'berry',
        'Lesions rapidly become dark, sunken and progressively enlarge.'
    ),
    (
        'SYM_COFFEE_BERRY_DISEASE_BERRY_ROT',
        'HP_COFFEE_BERRY_DISEASE',
        'berry',
        'The affected berry may eventually rot completely.'
    ),
    (
        'SYM_COFFEE_BERRY_DISEASE_SPORULATION',
        'HP_COFFEE_BERRY_DISEASE',
        'sporulation',
        'Pink spore masses may become visible on lesions under humid conditions.'
    ),
    (
        'SYM_COFFEE_BERRY_DISEASE_FRUIT_DROP',
        'HP_COFFEE_BERRY_DISEASE',
        'fruit_drop',
        'Affected berries may drop from the branch early.'
    ),
    (
        'SYM_COFFEE_BERRY_DISEASE_FLOWER',
        'HP_COFFEE_BERRY_DISEASE',
        'flower',
        'Under very wet conditions, flowers may develop brown lesions on the petals.'
    )
ON CONFLICT (symptom_id) DO NOTHING;

INSERT INTO public.transmission
    (transmission_id, health_problem_id, method, description)
VALUES
    (
        'TRANS_COFFEE_BERRY_DISEASE_RAIN_SPLASH',
        'HP_COFFEE_BERRY_DISEASE',
        'rain_splash',
        'Rain splash can spread fungal spores between infected and healthy plant tissues.'
    ),
    (
        'TRANS_COFFEE_BERRY_DISEASE_HUMAN_ACTIVITY',
        'HP_COFFEE_BERRY_DISEASE',
        'human_activity',
        'Human activity can contribute to movement of infected plant material and disease inoculum.'
    ),
    (
        'TRANS_COFFEE_BERRY_DISEASE_PLANT_MATERIAL',
        'HP_COFFEE_BERRY_DISEASE',
        'plant_material',
        'Infected plant material can carry the pathogen and contribute to disease spread.'
    ),
    (
        'TRANS_COFFEE_BERRY_DISEASE_ANIMALS',
        'HP_COFFEE_BERRY_DISEASE',
        'animals',
        'Animals can contribute to movement of infected plant material or fungal inoculum.'
    )
ON CONFLICT (transmission_id) DO NOTHING;

INSERT INTO public.conditions
    (condition_id, health_problem_id, factor, value, description)
VALUES
    (
        'COND_COFFEE_BERRY_DISEASE_HUMIDITY',
        'HP_COFFEE_BERRY_DISEASE',
        'humidity',
        'wet conditions',
        'Wet conditions favour disease development and infection.'
    ),
    (
        'COND_COFFEE_BERRY_DISEASE_TEMPERATURE',
        'HP_COFFEE_BERRY_DISEASE',
        'temperature',
        '15-27.7 C',
        'Temperatures in this range can favour coffee berry disease development.'
    )
ON CONFLICT (condition_id) DO NOTHING;

INSERT INTO public.management
    (management_id, health_problem_id, category, action)
VALUES
    (
        'MGMT_COFFEE_BERRY_DISEASE_VARIETY',
        'HP_COFFEE_BERRY_DISEASE',
        'variety_selection',
        'Use coffee varieties with appropriate resistance or tolerance to coffee berry disease where available.'
    ),
    (
        'MGMT_COFFEE_BERRY_DISEASE_PRUNING',
        'HP_COFFEE_BERRY_DISEASE',
        'pruning',
        'Prune appropriately to improve canopy conditions and reduce prolonged moisture around susceptible tissues.'
    ),
    (
        'MGMT_COFFEE_BERRY_DISEASE_SANITATION',
        'HP_COFFEE_BERRY_DISEASE',
        'sanitation',
        'Remove and manage infected plant material and affected berries to reduce sources of inoculum.'
    ),
    (
        'MGMT_COFFEE_BERRY_DISEASE_CANOPY',
        'HP_COFFEE_BERRY_DISEASE',
        'canopy_management',
        'Maintain suitable canopy management to improve airflow and reduce prolonged wetness.'
    ),
    (
        'MGMT_COFFEE_BERRY_DISEASE_FUNGICIDE',
        'HP_COFFEE_BERRY_DISEASE',
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
        'HP_COFFEE_BERRY_DISEASE',
        'Fungicide',
        'Disease management',
        'Copper oxychloride',
        'Copper-based protectant',
        'Before the rainy season and according to disease risk',
        'Use a registered copper oxychloride formulation according to the product label and local recommendations.',
        'Rotate with fungicides having different modes of action where appropriate.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_COFFEE_BERRY_DISEASE',
        'Fungicide',
        'Disease management',
        'Azoxystrobin + tebuconazole',
        'QoI + DMI',
        'Before disease-favourable wet periods and according to local recommendations',
        'Use a registered combination product according to its product label.',
        'Rotate fungicide modes of action and avoid repeated use of the same mode of action.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_COFFEE_BERRY_DISEASE',
        'Fungicide',
        'Disease management',
        'Chlorothalonil',
        'Multi-site protectant',
        'Before and during disease-favourable wet periods according to local recommendations',
        'Use a registered chlorothalonil formulation according to the product label.',
        'Use integrated disease management and rotate modes of action where appropriate.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_COFFEE_BERRY_DISEASE',
        'Fungicide',
        'Disease management',
        'Pyraclostrobin',
        'QoI',
        'Before and during disease-favourable wet periods according to local recommendations',
        'Use a registered pyraclostrobin formulation according to the product label.',
        'Rotate or combine fungicide modes of action where appropriate to reduce resistance risk.',
        'Follow the registered product label and required protective measures.',
        NULL
    );

INSERT INTO public.sources
    (source_id, health_problem_id, organization, title, url, accessed_date)
VALUES
    (
        'SRC_COFFEE_BERRY_DISEASE_GREENLIFE',
        'HP_COFFEE_BERRY_DISEASE',
        'Greenlife Crop Protection Africa',
        'Understanding Coffee Berry Disease',
        'https://www.greenlife.co.ke/understanding-coffee-berry-disease/',
        NULL
    ),
    (
        'SRC_COFFEE_BERRY_DISEASE_BIOVISION',
        'HP_COFFEE_BERRY_DISEASE',
        'Infonet Biovision',
        'Coffee berry disease',
        'https://infonet-biovision.org/PlantHealth/MinorPests/coffee-berry-disease',
        NULL
    )
ON CONFLICT (source_id) DO NOTHING;
