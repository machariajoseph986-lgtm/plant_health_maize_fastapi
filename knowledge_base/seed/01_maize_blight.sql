-- Maize Blight knowledge-base seed
-- Health problem: HP_MAIZE_BLIGHT

INSERT INTO public.health_problems
    (health_problem_id, plant_id, name, type, description)
VALUES
    (
        'HP_MAIZE_BLIGHT',
        'PLANT_MAIZE',
        'Maize Blight',
        'fungal',
        'A fungal leaf disease class represented as Blight in the maize CNN dataset. The current dataset label does not by itself establish a specific blight species, so the knowledge profile is intentionally kept at the generic maize blight level.'
    )
ON CONFLICT (health_problem_id) DO NOTHING;

INSERT INTO public.symptoms
    (symptom_id, health_problem_id, category, description)
VALUES
    ('SYM_MAIZE_BLIGHT_LEAF', 'HP_MAIZE_BLIGHT', 'leaf',
     'Leaf lesions or necrotic areas may develop on maize foliage.'),
    ('SYM_MAIZE_BLIGHT_FOLIAR', 'HP_MAIZE_BLIGHT', 'foliar',
     'Affected leaf tissue may progressively lose its normal green colour.'),
    ('SYM_MAIZE_BLIGHT_SEVERITY', 'HP_MAIZE_BLIGHT', 'severity',
     'Severe foliar infection can reduce functional leaf area and plant performance.')
ON CONFLICT (symptom_id) DO NOTHING;

INSERT INTO public.transmission
    (transmission_id, health_problem_id, method, description)
VALUES
    ('TRANS_MAIZE_BLIGHT_SPORES', 'HP_MAIZE_BLIGHT', 'airborne_spores',
     'Fungal foliar pathogens may spread through airborne spores from infected plant material.'),
    ('TRANS_MAIZE_BLIGHT_RESIDUE', 'HP_MAIZE_BLIGHT', 'infected_residue',
     'Some maize blight pathogens can survive in infected crop residue and produce inoculum for subsequent crops.')
ON CONFLICT (transmission_id) DO NOTHING;

INSERT INTO public.conditions
    (condition_id, health_problem_id, factor, value, description)
VALUES
    ('COND_MAIZE_BLIGHT_MOISTURE', 'HP_MAIZE_BLIGHT', 'moisture/high',
     'Extended leaf wetness and humid conditions',
     'Extended leaf wetness and humid conditions can favour fungal foliar disease development.'),
    ('COND_MAIZE_BLIGHT_RESIDUE', 'HP_MAIZE_BLIGHT', 'crop_residue/infected',
     'Infected maize residue',
     'Infected maize residue can provide a source of inoculum for some maize blight pathogens.')
ON CONFLICT (condition_id) DO NOTHING;

INSERT INTO public.management
    (management_id, health_problem_id, category, action)
VALUES
    ('MGMT_MAIZE_BLIGHT_RESISTANCE', 'HP_MAIZE_BLIGHT', 'resistance',
     'Use maize hybrids with appropriate resistance to important foliar blight diseases.'),
    ('MGMT_MAIZE_BLIGHT_ROTATION', 'HP_MAIZE_BLIGHT', 'crop_rotation',
     'Use crop rotation where appropriate to reduce disease pressure from pathogens that survive in crop residue.'),
    ('MGMT_MAIZE_BLIGHT_RESIDUE', 'HP_MAIZE_BLIGHT', 'residue_management',
     'Manage infected maize residue to reduce potential sources of fungal inoculum.')
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
        'HP_MAIZE_BLIGHT',
        'Fungicide',
        'Disease management',
        'Propiconazole',
        'Triazole (DMI)',
        'At first appearance of lesions',
        'Use registered propiconazole-based fungicide according to product label',
        'Rotate or combine fungicide modes of action where appropriate to reduce resistance risk',
        'PPE + registered label',
        NULL
    ),
    (
        'HP_MAIZE_BLIGHT',
        'Fungicide',
        'Disease management',
        'Azoxystrobin + difenoconazole',
        'Strobilurin (QoI) + triazole (DMI)',
        'At first appearance of lesions',
        'Use registered combination product according to label',
        'Rotate modes of action',
        'Follow registered product label and required protective measures',
        NULL
    ),
    (
        'HP_MAIZE_BLIGHT',
        'Fungicide',
        'Disease management',
        'Carbendazim + mancozeb',
        'Systemic + protectant fungicide combination',
        'When symptoms begin and according to label',
        'Use a registered formulation according to label',
        'Use appropriate resistance-management practices',
        'PPE + label',
        NULL
    );

INSERT INTO public.sources
    (source_id, health_problem_id, organization, title, url, accessed_date)
VALUES
    (
        'SRC_MAIZE_BLIGHT_UDEL',
        'HP_MAIZE_BLIGHT',
        'University of Delaware Cooperative Extension',
        'Northern Corn Leaf Blight',
        'https://www.udel.edu/academics/colleges/canr/cooperative-extension/fact-sheets/northern-corn-leaf-blight/',
        NULL
    ),
    (
        'SRC_MAIZE_BLIGHT_CORNELL',
        'HP_MAIZE_BLIGHT',
        'Cornell University',
        'Northern Corn Leaf Blight',
        'https://cals.cornell.edu/field-crops/corn/diseases-of-corn/northern-corn-leaf-blight',
        NULL
    )
ON CONFLICT (source_id) DO NOTHING;
