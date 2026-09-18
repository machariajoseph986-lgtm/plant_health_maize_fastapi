-- Potato Bacterial Wilt knowledge-base seed
-- Health problem: HP_POTATO_BACTERIAL_WILT

INSERT INTO public.health_problems
    (health_problem_id, plant_id, name, type, description)
VALUES
    (
        'HP_POTATO_BACTERIAL_WILT',
        'PLANT_POTATO',
        'Potato Bacterial Wilt',
        'bacterial',
        'A serious soil-borne bacterial disease of potato caused by Ralstonia solanacearum and associated with wilting, yellowing and tuber symptoms.'
    )
ON CONFLICT (health_problem_id) DO NOTHING;

INSERT INTO public.pathogens
    (pathogen_id, health_problem_id, scientific_name, type, role)
VALUES
    (
        'PATH_POTATO_BACTERIAL_WILT_R_SOLANACEARUM',
        'HP_POTATO_BACTERIAL_WILT',
        'Ralstonia solanacearum',
        'bacterium',
        'Soil-borne bacterium responsible for bacterial wilt of potato'
    )
ON CONFLICT (pathogen_id) DO NOTHING;

INSERT INTO public.symptoms
    (symptom_id, health_problem_id, category, description)
VALUES
    (
        'SYM_POTATO_BACTERIAL_WILT_PLANT',
        'HP_POTATO_BACTERIAL_WILT',
        'plant',
        'Wilting may begin with drooping of the tips of lower leaves.'
    ),
    (
        'SYM_POTATO_BACTERIAL_WILT_LEAF',
        'HP_POTATO_BACTERIAL_WILT',
        'leaf',
        'Leaves may yellow and roll upward and inward from the margins.'
    ),
    (
        'SYM_POTATO_BACTERIAL_WILT_STUNT',
        'HP_POTATO_BACTERIAL_WILT',
        'plant',
        'Plants may become stunted and experience die-back.'
    ),
    (
        'SYM_POTATO_BACTERIAL_WILT_TUBER_EXTERNAL',
        'HP_POTATO_BACTERIAL_WILT',
        'tuber',
        'Brownish-grey areas may appear on the outside of infected tubers, especially near stolon attachment.'
    ),
    (
        'SYM_POTATO_BACTERIAL_WILT_TUBER_OOZE',
        'HP_POTATO_BACTERIAL_WILT',
        'tuber',
        'Bacterial ooze may emerge through the eyes of infected tubers.'
    ),
    (
        'SYM_POTATO_BACTERIAL_WILT_VASCULAR',
        'HP_POTATO_BACTERIAL_WILT',
        'vascular',
        'Cut infected tubers may show browning of vascular tissue and bacterial discharge.'
    )
ON CONFLICT (symptom_id) DO NOTHING;

INSERT INTO public.transmission
    (transmission_id, health_problem_id, method, description)
VALUES
    (
        'TRANS_POTATO_BACTERIAL_WILT_WATER',
        'HP_POTATO_BACTERIAL_WILT',
        'water',
        'Water can move the soil-borne pathogen between infected and healthy areas.'
    ),
    (
        'TRANS_POTATO_BACTERIAL_WILT_SOIL',
        'HP_POTATO_BACTERIAL_WILT',
        'soil',
        'Contaminated soil can carry the pathogen between fields and planting sites.'
    ),
    (
        'TRANS_POTATO_BACTERIAL_WILT_EQUIPMENT',
        'HP_POTATO_BACTERIAL_WILT',
        'equipment',
        'Contaminated farm equipment can transfer infected soil and pathogen material.'
    ),
    (
        'TRANS_POTATO_BACTERIAL_WILT_SEED',
        'HP_POTATO_BACTERIAL_WILT',
        'seed',
        'Infected or contaminated seed tubers can introduce the pathogen into new fields.'
    )
ON CONFLICT (transmission_id) DO NOTHING;

INSERT INTO public.conditions
    (condition_id, health_problem_id, factor, value, description)
VALUES
    (
        'COND_POTATO_BACTERIAL_WILT_TEMPERATURE',
        'HP_POTATO_BACTERIAL_WILT',
        'temperature',
        '25-37 C',
        'Warm temperatures can favour bacterial wilt development.'
    ),
    (
        'COND_POTATO_BACTERIAL_WILT_SOIL_MOISTURE',
        'HP_POTATO_BACTERIAL_WILT',
        'soil_moisture',
        'wet soil',
        'Wet soil conditions can favour bacterial wilt development and pathogen movement.'
    ),
    (
        'COND_POTATO_BACTERIAL_WILT_SOIL_TEMPERATURE',
        'HP_POTATO_BACTERIAL_WILT',
        'soil_temperature',
        'below 15 C',
        'Lower soil temperatures are associated with fewer bacterial wilt problems.'
    )
ON CONFLICT (condition_id) DO NOTHING;

INSERT INTO public.management
    (management_id, health_problem_id, category, action)
VALUES
    (
        'MGMT_POTATO_BACTERIAL_WILT_ROTATION',
        'HP_POTATO_BACTERIAL_WILT',
        'crop_rotation',
        'Rotate with pastures, cereals and other non-solanaceous crops for more than five years where appropriate.'
    ),
    (
        'MGMT_POTATO_BACTERIAL_WILT_SEED',
        'HP_POTATO_BACTERIAL_WILT',
        'seed',
        'Use certified seed from reliable sources.'
    ),
    (
        'MGMT_POTATO_BACTERIAL_WILT_FIELD',
        'HP_POTATO_BACTERIAL_WILT',
        'field_selection',
        'Select planting fields with a low risk of bacterial wilt and avoid known contaminated sites where practical.'
    ),
    (
        'MGMT_POTATO_BACTERIAL_WILT_WEEDS',
        'HP_POTATO_BACTERIAL_WILT',
        'weed_control',
        'Control weeds that may help maintain or spread the pathogen in affected production areas.'
    ),
    (
        'MGMT_POTATO_BACTERIAL_WILT_WATER',
        'HP_POTATO_BACTERIAL_WILT',
        'water_management',
        'Manage irrigation and drainage to reduce movement of contaminated water through the production area.'
    ),
    (
        'MGMT_POTATO_BACTERIAL_WILT_SANITATION',
        'HP_POTATO_BACTERIAL_WILT',
        'sanitation',
        'Remove and manage infected plant material and maintain good field sanitation.'
    ),
    (
        'MGMT_POTATO_BACTERIAL_WILT_EQUIPMENT',
        'HP_POTATO_BACTERIAL_WILT',
        'equipment_hygiene',
        'Clean equipment and tools to reduce transfer of contaminated soil between fields.'
    ),
    (
        'MGMT_POTATO_BACTERIAL_WILT_SEED_HYGIENE',
        'HP_POTATO_BACTERIAL_WILT',
        'seed_hygiene',
        'Maintain seed hygiene and use clean planting material from reliable sources.'
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
        'HP_POTATO_BACTERIAL_WILT',
        'No reliable chemical cure',
        'Disease management',
        NULL,
        NULL,
        'Not applicable',
        'There is no reliable chemical cure for potato bacterial wilt. Management should focus on prevention, sanitation, certified seed and other integrated practices.',
        NULL,
        'Do not rely on chemical treatment as a cure. Follow local agricultural guidance for any products used for other purposes.',
        NULL
    );

INSERT INTO public.sources
    (source_id, health_problem_id, organization, title, url, accessed_date)
VALUES
    (
        'SRC_POTATO_BACTERIAL_WILT_NPCK',
        'HP_POTATO_BACTERIAL_WILT',
        'National Potato Council of Kenya',
        'Managing Potato Diseases: Common Issues and Solutions',
        'https://npck.org/managing-potato-diseases-common-issues-and-solutions/',
        NULL
    ),
    (
        'SRC_POTATO_BACTERIAL_WILT_AGVICT',
        'HP_POTATO_BACTERIAL_WILT',
        'Agriculture Victoria',
        'Bacterial wilt of potatoes',
        'https://agriculture.vic.gov.au/biosecurity/plant-diseases/vegetable-diseases/bacterial-wilt-of-potatoes',
        NULL
    )
ON CONFLICT (source_id) DO NOTHING;
