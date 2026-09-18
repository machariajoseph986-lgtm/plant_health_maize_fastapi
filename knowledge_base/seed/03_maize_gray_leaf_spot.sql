-- Maize Gray Leaf Spot knowledge-base seed
-- Health problem: HP_MAIZE_GRAY_LEAF_SPOT

INSERT INTO public.health_problems
    (health_problem_id, plant_id, name, type, description)
VALUES
    (
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'PLANT_MAIZE',
        'Maize Gray Leaf Spot',
        'fungal',
        'A fungal disease of maize caused by Cercospora zeae-maydis. Characteristic rectangular gray lesions develop on leaves and can cause substantial loss of functional leaf area.'
    )
ON CONFLICT (health_problem_id) DO NOTHING;

INSERT INTO public.pathogens
    (pathogen_id, health_problem_id, scientific_name, type, role)
VALUES
    (
        'PATH_MAIZE_GRAY_LEAF_SPOT_C_ZEAE_MAYDIS',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'Cercospora zeae-maydis',
        'fungus',
        'Causal pathogen of maize gray leaf spot.'
    )
ON CONFLICT (pathogen_id) DO NOTHING;

INSERT INTO public.symptoms
    (symptom_id, health_problem_id, category, description)
VALUES
    (
        'SYM_MAIZE_GRAY_LEAF_SPOT_EARLY',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'early',
        'Small brown lesions may first appear on lower maize leaves.'
    ),
    (
        'SYM_MAIZE_GRAY_LEAF_SPOT_LESION',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'lesion',
        'Lesions elongate and become limited by leaf veins, producing a characteristic rectangular shape.'
    ),
    (
        'SYM_MAIZE_GRAY_LEAF_SPOT_COLOUR',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'colour',
        'Lesions become gray or gray-brown as disease develops and sporulation occurs.'
    ),
    (
        'SYM_MAIZE_GRAY_LEAF_SPOT_SEVERITY',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'severity',
        'Lesions can coalesce and kill substantial areas of leaf tissue.'
    )
ON CONFLICT (symptom_id) DO NOTHING;

INSERT INTO public.transmission
    (transmission_id, health_problem_id, method, description)
VALUES
    (
        'TRANS_MAIZE_GRAY_LEAF_SPOT_AIRBORNE',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'airborne_spores',
        'Fungal spores can be dispersed through the air and initiate infections on susceptible maize foliage.'
    ),
    (
        'TRANS_MAIZE_GRAY_LEAF_SPOT_RESIDUE',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'crop_residue',
        'The pathogen can survive in infected maize crop residue and provide inoculum for subsequent disease development.'
    )
ON CONFLICT (transmission_id) DO NOTHING;

INSERT INTO public.conditions
    (condition_id, health_problem_id, factor, value, description)
VALUES
    (
        'COND_MAIZE_GRAY_LEAF_SPOT_TEMPERATURE',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'temperature/warm',
        'Warm conditions',
        'Warm conditions can favour gray leaf spot development.'
    ),
    (
        'COND_MAIZE_GRAY_LEAF_SPOT_HUMIDITY',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'humidity/high',
        'High humidity and leaf wetness',
        'High humidity and prolonged leaf wetness can favour infection and disease development.'
    ),
    (
        'COND_MAIZE_GRAY_LEAF_SPOT_CROPPING',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'cropping_pattern/continuous_maize',
        'Continuous maize production',
        'Continuous maize production can increase disease pressure where infected residue carries inoculum between crops.'
    )
ON CONFLICT (condition_id) DO NOTHING;

INSERT INTO public.management
    (management_id, health_problem_id, category, action)
VALUES
    (
        'MGMT_MAIZE_GRAY_LEAF_SPOT_RESISTANCE',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'resistance',
        'Use maize hybrids with appropriate resistance where available.'
    ),
    (
        'MGMT_MAIZE_GRAY_LEAF_SPOT_ROTATION',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'crop_rotation',
        'Use crop rotation where appropriate to reduce disease pressure from pathogens that survive in crop residue.'
    ),
    (
        'MGMT_MAIZE_GRAY_LEAF_SPOT_RESIDUE',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'residue_management',
        'Manage infected maize residue to reduce potential sources of fungal inoculum.'
    ),
    (
        'MGMT_MAIZE_GRAY_LEAF_SPOT_MONITORING',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'monitoring',
        'Monitor maize fields for early gray leaf spot lesions and disease progression.'
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
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'Fungicide',
        'Disease management',
        'Azoxystrobin + propiconazole',
        'Strobilurin (QoI) + triazole (DMI)',
        'According to disease development and registered product label',
        'Use a registered combination product according to label instructions.',
        'Rotate fungicide modes of action where appropriate to reduce resistance risk.',
        'Wear appropriate personal protective equipment and follow the registered product label.',
        NULL
    ),
    (
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'Fungicide',
        'Disease management',
        'Prothioconazole + trifloxystrobin',
        'Triazole (DMI) + strobilurin (QoI)',
        'According to disease development and registered product label',
        'Use a registered combination product according to label instructions.',
        'Rotate fungicide modes of action where appropriate to reduce resistance risk.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'Fungicide',
        'Disease management',
        'Difenoconazole',
        'Triazole (DMI)',
        'According to disease development and registered product label',
        'Use a registered difenoconazole-based fungicide according to label instructions.',
        'Rotate fungicide modes of action where appropriate to reduce resistance risk.',
        'Wear appropriate personal protective equipment and follow the registered product label.',
        NULL
    ),
    (
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'Fungicide',
        'Disease management',
        'Tebuconazole',
        'Triazole (DMI)',
        'According to disease development and registered product label',
        'Use a registered tebuconazole-based fungicide according to label instructions.',
        'Rotate fungicide modes of action where appropriate to reduce resistance risk.',
        'Wear appropriate personal protective equipment and follow the registered product label.',
        NULL
    ),
    (
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'Fungicide',
        'Disease management',
        'Carbendazim + flusilazole',
        'Systemic fungicide combination',
        'According to disease development and registered product label',
        'Use a registered formulation according to label instructions.',
        'Use appropriate resistance-management practices and rotate modes of action where applicable.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'Fungicide',
        'Disease management',
        'Carbendazim + propiconazole',
        'Systemic fungicide combination',
        'According to disease development and registered product label',
        'Use a registered formulation according to label instructions.',
        'Use appropriate resistance-management practices and rotate modes of action where applicable.',
        'Follow the registered product label and required protective measures.',
        NULL
    ),
    (
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'Fungicide',
        'Disease management',
        'Fluindapyr + flutriafol + azoxystrobin',
        'Fungicide combination',
        'According to disease development and registered product label',
        'Use appropriate resistance-management practices and rotate modes of action where applicable.',
        'Follow the registered product label and required protective measures.',
        'Follow the registered product label and required protective measures.',
        NULL
    );

INSERT INTO public.sources
    (source_id, health_problem_id, organization, title, url, accessed_date)
VALUES
    (
        'SRC_MAIZE_GRAY_LEAF_SPOT_UDEL',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'University of Delaware Cooperative Extension',
        'Gray Leaf Spot',
        'https://www.udel.edu/academics/colleges/canr/cooperative-extension/fact-sheets/gray-leaf-spot/',
        NULL
    ),
    (
        'SRC_MAIZE_GRAY_LEAF_SPOT_CORNELL',
        'HP_MAIZE_GRAY_LEAF_SPOT',
        'Cornell University',
        'Gray Leaf Spot',
        'https://cals.cornell.edu/field-crops/corn/diseases-of-corn/gray-leaf-spot',
        NULL
    )
ON CONFLICT (source_id) DO NOTHING;
