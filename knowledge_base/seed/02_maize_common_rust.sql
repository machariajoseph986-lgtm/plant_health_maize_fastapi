-- Maize Common Rust knowledge-base seed
-- Health problem: HP_MAIZE_COMMON_RUST

INSERT INTO public.health_problems
    (health_problem_id, plant_id, name, type, description)
VALUES
    (
        'HP_MAIZE_COMMON_RUST',
        'PLANT_MAIZE',
        'Maize Common Rust',
        'fungal',
        'A fungal disease of maize caused by Puccinia sorghi. It produces characteristic rust-coloured pustules on above-ground plant tissues, especially leaves.'
    )
ON CONFLICT (health_problem_id) DO NOTHING;

INSERT INTO public.pathogens
    (pathogen_id, health_problem_id, scientific_name, type, role)
VALUES
    (
        'PATH_MAIZE_COMMON_RUST_P_SORGHI',
        'HP_MAIZE_COMMON_RUST',
        'Puccinia sorghi',
        'fungus',
        'Causal pathogen of maize common rust.'
    )
ON CONFLICT (pathogen_id) DO NOTHING;

INSERT INTO public.symptoms
    (symptom_id, health_problem_id, category, description)
VALUES
    (
        'SYM_MAIZE_COMMON_RUST_EARLY',
        'HP_MAIZE_COMMON_RUST',
        'early',
        'Small flecks may appear on maize leaves.'
    ),
    (
        'SYM_MAIZE_COMMON_RUST_PUSTULES',
        'HP_MAIZE_COMMON_RUST',
        'pustules',
        'Circular to elongated brown, cinnamon-brown or rust-coloured pustules develop on leaf surfaces.'
    ),
    (
        'SYM_MAIZE_COMMON_RUST_MATURE',
        'HP_MAIZE_COMMON_RUST',
        'mature',
        'Pustules become darker as fungal spores mature.'
    ),
    (
        'SYM_MAIZE_COMMON_RUST_SEVERE',
        'HP_MAIZE_COMMON_RUST',
        'severe',
        'Severe infection may cause leaf yellowing and premature death.'
    )
ON CONFLICT (symptom_id) DO NOTHING;

INSERT INTO public.transmission
    (transmission_id, health_problem_id, method, description)
VALUES
    (
        'TRANS_MAIZE_COMMON_RUST_WIND',
        'HP_MAIZE_COMMON_RUST',
        'wind',
        'Windborne spores can spread the pathogen between plants and fields.'
    ),
    (
        'TRANS_MAIZE_COMMON_RUST_AIRBORNE',
        'HP_MAIZE_COMMON_RUST',
        'airborne_spores',
        'Urediniospores can be carried through air and initiate new infections.'
    )
ON CONFLICT (transmission_id) DO NOTHING;

INSERT INTO public.conditions
    (condition_id, health_problem_id, factor, value, description)
VALUES
    (
        'COND_MAIZE_COMMON_RUST_TEMPERATURE',
        'HP_MAIZE_COMMON_RUST',
        'temperature/cool',
        'Cool temperatures',
        'Cool temperatures favour common rust development.'
    ),
    (
        'COND_MAIZE_COMMON_RUST_HUMIDITY',
        'HP_MAIZE_COMMON_RUST',
        'humidity/high',
        'High relative humidity and prolonged leaf wetness',
        'High relative humidity and prolonged leaf wetness favour infection and disease development.'
    )
ON CONFLICT (condition_id) DO NOTHING;

INSERT INTO public.management
    (management_id, health_problem_id, category, action)
VALUES
    (
        'MGMT_MAIZE_COMMON_RUST_RESISTANCE',
        'HP_MAIZE_COMMON_RUST',
        'resistance',
        'Use resistant maize hybrids where available.'
    ),
    (
        'MGMT_MAIZE_COMMON_RUST_MONITORING',
        'HP_MAIZE_COMMON_RUST',
        'monitoring',
        'Monitor maize fields for rust-coloured pustules, especially during cool and humid conditions.'
    ),
    (
        'MGMT_MAIZE_COMMON_RUST_IRRIGATION',
        'HP_MAIZE_COMMON_RUST',
        'irrigation',
        'Where irrigation is necessary, practices that reduce prolonged leaf wetness can help reduce infection risk.'
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
        'HP_MAIZE_COMMON_RUST',
        'Fungicide',
        'Disease management',
        'Mancozeb',
        'Protectant fungicide',
        'When disease is detected and according to the registered product label',
        'Use a registered mancozeb-based fungicide according to product label instructions.',
        'Use appropriate fungicide resistance-management practices and rotate modes of action where applicable.',
        'Wear appropriate personal protective equipment and follow the registered product label.',
        NULL
    ),
    (
        'HP_MAIZE_COMMON_RUST',
        'Fungicide',
        'Disease management',
        'Tebuconazole',
        'Triazole (DMI)',
        'When disease is detected and according to the registered product label',
        'Use a registered tebuconazole-based fungicide according to product label instructions.',
        'Rotate fungicide modes of action where appropriate to reduce resistance risk.',
        'Wear appropriate personal protective equipment and follow the registered product label.',
        NULL
    ),
    (
        'HP_MAIZE_COMMON_RUST',
        'Fungicide',
        'Disease management',
        'Azoxystrobin + propiconazole',
        'Strobilurin (QoI) + triazole (DMI)',
        'When disease is detected and according to the registered product label',
        'Use a registered combination product according to label instructions.',
        'Rotate or combine fungicide modes of action appropriately to reduce resistance risk.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_MAIZE_COMMON_RUST',
        'Fungicide',
        'Disease management',
        'Pyraclostrobin + metconazole',
        'Strobilurin (QoI) + triazole (DMI)',
        'When disease is detected and according to the registered product label',
        'Use a registered combination product according to label instructions.',
        'Rotate fungicide modes of action where appropriate to reduce resistance risk.',
        'Follow the registered product label and required protective measures.',
        NULL
    );

INSERT INTO public.sources
    (source_id, health_problem_id, organization, title, url, accessed_date)
VALUES
    (
        'SRC_MAIZE_COMMON_RUST_CORNELL',
        'HP_MAIZE_COMMON_RUST',
        'Cornell University',
        'Common Rust',
        'https://cals.cornell.edu/field-crops/corn/diseases-of-corn/common-rust',
        NULL
    ),
    (
        'SRC_MAIZE_COMMON_RUST_UCIPM',
        'HP_MAIZE_COMMON_RUST',
        'UC Statewide Integrated Pest Management Program',
        'Common Rust - Corn',
        'https://ipm.ucanr.edu/agriculture/corn/common-rust/',
        NULL
    )
ON CONFLICT (source_id) DO NOTHING;
