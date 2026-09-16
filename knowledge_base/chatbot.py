from knowledge_base.database_postgresql import (
    get_all_diseases,
    find_disease,
    get_disease_profile
)


# ---------------------------------------------------------
# FORMAT COMPLETE DISEASE PROFILE
# ---------------------------------------------------------

def format_disease_profile(profile):
    """
    Convert a complete disease profile into structured HTML
    for the chatbot interface.
    """

    response = []

    response.append(
        f'<div class="disease-introduction">'
        f'<h3>{profile["disease"]}</h3>'
        f'<p>{profile["disease"]} is a {profile["type"]} '
        f'health problem affecting {profile["crop"]}.</p>'
        f'</div>'
    )

    if profile["pathogens"]:
        items = []

        for pathogen in profile["pathogens"]:
            scientific_name = pathogen.get("scientific_name", "Unknown")
            pathogen_type = pathogen.get("type", "Unknown")
            role = pathogen.get("role", "")

            text = f"<strong>{scientific_name}</strong>"

            if pathogen_type:
                text += f" <em>({pathogen_type})</em>"

            if role:
                text += f" — {role}"

            items.append(f"<li>{text}</li>")

        response.append(
            '<section class="info-section">'
            '<h4>Causing organism(s)</h4>'
            f'<ul>{"".join(items)}</ul>'
            '</section>'
        )

    if profile["symptoms"]:
        items = []

        for symptom in profile["symptoms"]:
            category = symptom.get("category", "")
            description = symptom.get("description", "")

            if category:
                text = f"<strong>{category.title()}</strong> — {description}"
            else:
                text = description

            items.append(f"<li>{text}</li>")

        response.append(
            '<section class="info-section">'
            '<h4>Symptoms</h4>'
            f'<ul>{"".join(items)}</ul>'
            '</section>'
        )

    if profile["transmission"]:
        items = []

        for item in profile["transmission"]:
            method = item.get("method", "")
            description = item.get("description", "")

            if method:
                text = f"<strong>{method.replace('_', ' ').title()}</strong> — {description}"
            else:
                text = description

            items.append(f"<li>{text}</li>")

        response.append(
            '<section class="info-section">'
            '<h4>Transmission</h4>'
            f'<ul>{"".join(items)}</ul>'
            '</section>'
        )

    if profile["conditions"]:
        items = []

        for condition in profile["conditions"]:
            factor = condition.get("factor", "")
            value = condition.get("value", "")
            description = condition.get("description", "")

            text = f"<strong>{factor.replace('_', ' ').title()}</strong>"

            if value:
                text += f" <em>({value})</em>"

            if description:
                text += f" — {description}"

            items.append(f"<li>{text}</li>")

        response.append(
            '<section class="info-section">'
            '<h4>Favourable conditions</h4>'
            f'<ul>{"".join(items)}</ul>'
            '</section>'
        )

    if profile["management"]:
        items = []

        for item in profile["management"]:
            category = item.get("category", "")
            action = item.get("action", "")

            if category:
                text = f"<strong>{category.title()}</strong> — {action}"
            else:
                text = action

            items.append(f"<li>{text}</li>")

        response.append(
            '<section class="info-section">'
            '<h4>Management</h4>'
            f'<ul>{"".join(items)}</ul>'
            '</section>'
        )

    if profile["sources"]:
        items = []

        for source in profile["sources"]:
            organization = source.get("organization", "")
            title = source.get("title", "")
            url = source.get("url", "")

            source_name = organization

            if title:
                source_name += f" — {title}" if source_name else title

            if url:
                text = (
                    f'<a href="{url}" target="_blank" rel="noopener noreferrer">'
                    f'{source_name}</a>'
                )
            else:
                text = source_name

            items.append(f"<li>{text}</li>")

        response.append(
            '<section class="info-section">'
            '<h4>Sources</h4>'
            f'<ul>{"".join(items)}</ul>'
            '</section>'
        )

    return "".join(response)


# ---------------------------------------------------------
# FORMAT REQUESTED INFORMATION
# ---------------------------------------------------------

def format_requested_information(profile, intent):
    """
    Return the requested information as structured HTML.
    """

    sections = []

    if intent == "symptoms":
        items = []

        for symptom in profile["symptoms"]:
            category = symptom.get("category", "")
            description = symptom.get("description", "")

            if category:
                text = f"<strong>{category.title()}</strong> — {description}"
            else:
                text = description

            items.append(f"<li>{text}</li>")

        return (
            f'<div class="disease-introduction">'
            f'<h3>{profile["disease"]}</h3>'
            f'</div>'
            f'<section class="info-section">'
            f'<h4>Symptoms</h4>'
            f'<ul>{"".join(items)}</ul>'
            f'</section>'
        )

    if intent == "pathogens":
        items = []

        for pathogen in profile["pathogens"]:
            scientific_name = pathogen.get("scientific_name", "")
            pathogen_type = pathogen.get("type", "")
            role = pathogen.get("role", "")

            text = f"<strong>{scientific_name}</strong>"

            if pathogen_type:
                text += f" <em>({pathogen_type})</em>"

            if role:
                text += f" — {role}"

            items.append(f"<li>{text}</li>")

        return (
            f'<div class="disease-introduction">'
            f'<h3>{profile["disease"]}</h3>'
            f'</div>'
            f'<section class="info-section">'
            f'<h4>Causing organism(s)</h4>'
            f'<ul>{"".join(items)}</ul>'
            f'</section>'
        )

    if intent == "transmission":
        items = []

        for item in profile["transmission"]:
            method = item.get("method", "")
            description = item.get("description", "")

            text = (
                f"<strong>{method.replace('_', ' ').title()}</strong>"
                f" — {description}"
            )

            items.append(f"<li>{text}</li>")

        return (
            f'<div class="disease-introduction">'
            f'<h3>{profile["disease"]}</h3>'
            f'</div>'
            f'<section class="info-section">'
            f'<h4>Transmission</h4>'
            f'<ul>{"".join(items)}</ul>'
            f'</section>'
        )

    if intent == "conditions":
        items = []

        for condition in profile["conditions"]:
            factor = condition.get("factor", "")
            value = condition.get("value", "")
            description = condition.get("description", "")

            text = f"<strong>{factor.replace('_', ' ').title()}</strong>"

            if value:
                text += f" <em>({value})</em>"

            if description:
                text += f" — {description}"

            items.append(f"<li>{text}</li>")

        return (
            f'<div class="disease-introduction">'
            f'<h3>{profile["disease"]}</h3>'
            f'</div>'
            f'<section class="info-section">'
            f'<h4>Favourable conditions</h4>'
            f'<ul>{"".join(items)}</ul>'
            f'</section>'
        )

    if intent == "management":
        items = []

        for item in profile["management"]:
            category = item.get("category", "")
            action = item.get("action", "")

            if category:
                text = f"<strong>{category.title()}</strong> — {action}"
            else:
                text = action

            items.append(f"<li>{text}</li>")

        return (
            f'<div class="disease-introduction">'
            f'<h3>{profile["disease"]}</h3>'
            f'</div>'
            f'<section class="info-section">'
            f'<h4>Management</h4>'
            f'<ul>{"".join(items)}</ul>'
            f'</section>'
        )

    if intent == "sources":
        items = []

        for source in profile["sources"]:
            organization = source.get("organization", "")
            title = source.get("title", "")
            url = source.get("url", "")

            source_name = organization

            if title:
                source_name += f" — {title}" if source_name else title

            if url:
                text = (
                    f'<a href="{url}" target="_blank" rel="noopener noreferrer">'
                    f'{source_name}</a>'
                )
            else:
                text = source_name

            items.append(f"<li>{text}</li>")

        return (
            f'<div class="disease-introduction">'
            f'<h3>{profile["disease"]}</h3>'
            f'</div>'
            f'<section class="info-section">'
            f'<h4>Sources</h4>'
            f'<ul>{"".join(items)}</ul>'
            f'</section>'
        )

    return format_disease_profile(profile)


# ---------------------------------------------------------
# DETECT USER INTENT
# ---------------------------------------------------------

def detect_intent(user_input):
    """
    Determine what information the user is requesting.
    """

    text = user_input.lower()

    # Symptoms
    if any(word in text for word in [
        "symptom",
        "symptoms",
        "sign",
        "signs",
        "look like",
        "show"
    ]):
        return "symptoms"

    # Causes / pathogens
    if any(phrase in text for phrase in [
        "cause",
        "caused by",
        "pathogen",
        "pathogens",
        "organism",
        "organisms",
        "virus",
        "fungus",
        "fungi",
        "bacteria",
        "bacterial"
    ]):
        return "pathogens"

    # Transmission
    if any(word in text for word in [
        "transmission",
        "transmitted",
        "spread",
        "spreads",
        "spread by"
    ]):
        return "transmission"

    # Conditions
    if any(word in text for word in [
        "condition",
        "conditions",
        "favourable",
        "favorable",
        "environment"
    ]):
        return "conditions"

    # Management
    if any(word in text for word in [
        "management",
        "manage",
        "control",
        "prevent",
        "prevention",
        "treat",
        "treatment"
    ]):
        return "management"

    # Sources
    if any(word in text for word in [
        "source",
        "sources",
        "reference",
        "references"
    ]):
        return "sources"

    # If no specific intent is detected,
    # return the complete profile.
    return "profile"


# ---------------------------------------------------------
# FORMAT REQUESTED INFORMATION
# ---------------------------------------------------------

def format_requested_information(profile, intent):
    """
    Return only the section requested by the user.
    """

    # -----------------------------------------------------
    # SYMPTOMS
    # -----------------------------------------------------

    if intent == "symptoms":

        response = [
            f"Symptoms of {profile['disease']}:"
        ]

        for symptom in profile["symptoms"]:

            category = symptom.get(
                "category",
                ""
            )

            description = symptom.get(
                "description",
                ""
            )

            if category:
                response.append(
                    f"- [{category}] {description}"
                )
            else:
                response.append(
                    f"- {description}"
                )

        return "\n".join(response)

    # -----------------------------------------------------
    # PATHOGENS
    # -----------------------------------------------------

    if intent == "pathogens":

        response = [
            f"Cause/pathogens associated with "
            f"{profile['disease']}:"
        ]

        for pathogen in profile["pathogens"]:

            scientific_name = pathogen.get(
                "scientific_name",
                ""
            )

            pathogen_type = pathogen.get(
                "type",
                ""
            )

            role = pathogen.get(
                "role",
                ""
            )

            text = f"- {scientific_name}"

            if pathogen_type:
                text += f" ({pathogen_type})"

            if role:
                text += f": {role}"

            response.append(text)

        return "\n".join(response)

    # -----------------------------------------------------
    # TRANSMISSION
    # -----------------------------------------------------

    if intent == "transmission":

        response = [
            f"Transmission of {profile['disease']}:"
        ]

        for item in profile["transmission"]:

            method = item.get(
                "method",
                ""
            )

            description = item.get(
                "description",
                ""
            )

            response.append(
                f"- {method}: {description}"
            )

        return "\n".join(response)

    # -----------------------------------------------------
    # CONDITIONS
    # -----------------------------------------------------

    if intent == "conditions":

        response = [
            f"Favourable conditions for "
            f"{profile['disease']}:"
        ]

        for condition in profile["conditions"]:

            factor = condition.get(
                "factor",
                ""
            )

            value = condition.get(
                "value",
                ""
            )

            description = condition.get(
                "description",
                ""
            )

            text = f"- {factor}"

            if value:
                text += f" ({value})"

            if description:
                text += f": {description}"

            response.append(text)

        return "\n".join(response)

    # -----------------------------------------------------
    # MANAGEMENT
    # -----------------------------------------------------

    if intent == "management":

        response = [
            f"Management information for "
            f"{profile['disease']}:"
        ]

        for item in profile["management"]:

            category = item.get(
                "category",
                ""
            )

            action = item.get(
                "action",
                ""
            )

            if category:
                response.append(
                    f"- [{category}] {action}"
                )
            else:
                response.append(
                    f"- {action}"
                )

        return "\n".join(response)

    # -----------------------------------------------------
    # SOURCES
    # -----------------------------------------------------

    if intent == "sources":

        response = [
            f"Sources for {profile['disease']}:"
        ]

        for source in profile["sources"]:

            organization = source.get(
                "organization",
                ""
            )

            title = source.get(
                "title",
                ""
            )

            url = source.get(
                "url",
                ""
            )

            text = "- "

            if organization:
                text += organization

            if title:
                text += f": {title}"

            if url:
                text += f"\n  {url}"

            response.append(text)

        return "\n".join(response)

    # -----------------------------------------------------
    # DEFAULT: COMPLETE PROFILE
    # -----------------------------------------------------

    return format_disease_profile(profile)


# ---------------------------------------------------------
# SEARCH DISEASE
# ---------------------------------------------------------

def search_disease(search_term):
    """
    Search the knowledge base and retrieve matching diseases.
    """

    matches = find_disease(search_term)

    if not matches:

        return None, (
            f"I could not find a disease matching "
            f"'{search_term}' in the knowledge base."
        )

    if len(matches) > 1:

        response = [
            f"I found {len(matches)} matching records:"
        ]

        for match in matches:

            response.append(
                f"- {match['disease']} "
                f"({match['crop']})"
            )

        response.append(
            "\nPlease specify the disease you want."
        )

        return None, "\n".join(response)

    disease_id = matches[0]["health_problem_id"]

    profile = get_disease_profile(disease_id)

    if profile is None:

        return None, (
            "The disease profile could not be retrieved."
        )

    return profile, None


# ---------------------------------------------------------
# CHATBOT RESPONSE
# ---------------------------------------------------------

def chatbot_response(user_input):
    """
    Process a user question and retrieve grounded
    information from the knowledge base.
    """

    text = user_input.strip().lower()

    if not text:
        return "Please enter a question."

    # -----------------------------------------------------
    # LIST AVAILABLE DISEASES
    # -----------------------------------------------------

    if (
        "what diseases" in text
        or "available diseases" in text
        or "list diseases" in text
    ):

        diseases = get_all_diseases()

        response = [
            "The knowledge base currently contains:"
        ]

        for disease in diseases:

            response.append(
                f"- {disease['disease']} "
                f"({disease['crop']})"
            )

        return "\n".join(response)

    # -----------------------------------------------------
    # DETECT DISEASE
    # -----------------------------------------------------

        # Disease-specific phrases must be checked BEFORE
    # generic plant names. Otherwise, a question such as
    # "What are the symptoms of maize common rust?"
    # may match "maize" first and return multiple diseases.

    search_terms = [
        # -------------------------------------------------
        # MAIZE — SPECIFIC DISEASES FIRST
        # -------------------------------------------------

        "maize lethal necrosis",
        "lethal necrosis",
        "mln",

        "maize common rust",
        "common rust",

        "maize gray leaf spot",
        "gray leaf spot",
        "gray leafspot",

        "maize blight",

        # -------------------------------------------------
        # TEA
        # -------------------------------------------------

        "tea blister blight",
        "blister blight",

        # -------------------------------------------------
        # COFFEE
        # -------------------------------------------------

        "coffee berry disease",
        "berry disease",

        # -------------------------------------------------
        # POTATO
        # -------------------------------------------------

        "potato bacterial wilt",
        "bacterial wilt",

        # -------------------------------------------------
        # GENERIC PLANT NAMES — CHECK LAST
        # -------------------------------------------------

        "maize",
        "tea",
        "coffee",
        "potato"
    ]

    matched_term = None

    for term in search_terms:

        if term in text:

            matched_term = term
            break

    if matched_term is None:

        return (
            "I could not identify a plant or disease in your "
            "question. Try mentioning maize, tea, coffee, "
            "potato, MLN, or a disease in the knowledge base."
        )

    # -----------------------------------------------------
    # SEARCH DATABASE
    # -----------------------------------------------------

    profile, error = search_disease(
        matched_term
    )

    if error:
        return error

    # -----------------------------------------------------
    # DETECT INTENT
    # -----------------------------------------------------

    intent = detect_intent(user_input)

    # -----------------------------------------------------
    # RETURN REQUESTED INFORMATION
    # -----------------------------------------------------

    return format_requested_information(
        profile,
        intent
    )


# ---------------------------------------------------------
# INTERACTIVE CHAT
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("PLANT HEALTH KNOWLEDGE BASE CHATBOT")
    print("=" * 60)

    print("\nKnowledge-base chatbot started.")
    print("Type 'exit' or 'quit' to stop.")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower().strip() in {
            "exit",
            "quit"
        }:

            print("\nChatbot: Goodbye.")
            break

        answer = chatbot_response(
            user_input
        )

        print("\nChatbot:")
        print(answer)