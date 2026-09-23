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

    # Chemical treatment
    if any(phrase in text for phrase in [
        "which chemical",
        "what chemical",
        "which chemicals",
        "what chemicals",
        "active ingredient",
        "active ingredients",
        "fungicide",
        "fungicides",
        "insecticide",
        "insecticides",
        "chemical treatment",
        "chemical treatments"
    ]):
        return "chemical_treatment"

    # Management
    if any(word in text for word in [
    "management",
    "manage",
    "control",
    "prevent",
    "prevention",
    "treat",
    "treatment",
    "should i do",
    "should we do",
    "can i do",
    "can we do",
    "what can i do",
    "what can we do",
    "how do i manage",
    "how can i manage",
    "how do i control",
    "how can i control",
    "how do i treat",
    "how can i treat",
    "how do i prevent",
    "how can i prevent"
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
    Return the requested information as clean structured HTML.
    """

    disease = profile["disease"]

    def section(title, items, category_key=None, text_key="description"):
        blocks = []

        for item in items:
            label = item.get(category_key, "") if category_key else ""
            text = item.get(text_key, "")

            if not text:
                continue

            if label:
                blocks.append(
                    f'<div class="chatbot-item">'
                    f'<strong>{label.replace("_", " ").title()}</strong>'
                    f'<p>{text}</p>'
                    f'</div>'
                )
            else:
                blocks.append(
                    f'<div class="chatbot-item">'
                    f'<p>{text}</p>'
                    f'</div>'
                )

        if not blocks:
            return (
                f'<section class="info-section">'
                f'<h4>{title}</h4>'
                f'<p>No information is currently available in the knowledge base.</p>'
                f'</section>'
            )

        return (
            f'<section class="info-section">'
            f'<h4>{title}</h4>'
            f'{"".join(blocks)}'
            f'</section>'
        )

    if intent == "symptoms":
        return (
            f'<div class="disease-introduction"><h3>{disease}</h3></div>'
            + section("Symptoms", profile["symptoms"], "category", "description")
        )

    if intent == "pathogens":
        blocks = []
        for item in profile["pathogens"]:
            name = item.get("scientific_name", "")
            pathogen_type = item.get("type", "")
            role = item.get("role", "")

            if not name:
                continue

            details = f'<p><em>{name}</em>'
            if pathogen_type:
                details += f' ({pathogen_type})'
            if role:
                details += f'<br>{role}'
            details += '</p>'

            blocks.append(
                f'<div class="chatbot-item"><strong>Causing organism</strong>{details}</div>'
            )

        return (
            f'<div class="disease-introduction"><h3>{disease}</h3></div>'
            f'<section class="info-section"><h4>Causing organism(s)</h4>'
            f'{"".join(blocks) or "<p>No pathogen information is currently available in the knowledge base.</p>"}'
            f'</section>'
        )

    if intent == "transmission":
        return (
            f'<div class="disease-introduction"><h3>{disease}</h3></div>'
            + section("Transmission", profile["transmission"], "method", "description")
        )

    if intent == "conditions":
        blocks = []
        for item in profile["conditions"]:
            factor = item.get("factor", "")
            value = item.get("value", "")
            description = item.get("description", "")

            if not factor and not description:
                continue

            label = factor.replace("_", " ").title() if factor else "Condition"
            text = description or value

            if description and value:
                text = f"{value}. {description}"

            blocks.append(
                f'<div class="chatbot-item">'
                f'<strong>{label}</strong>'
                f'<p>{text}</p>'
                f'</div>'
            )

        return (
            f'<div class="disease-introduction"><h3>{disease}</h3></div>'
            f'<section class="info-section"><h4>Favourable conditions</h4>'
            f'{"".join(blocks) or "<p>No condition information is currently available in the knowledge base.</p>"}'
            f'</section>'
        )

    if intent == "chemical_treatment":
        blocks = []
        for item in profile.get("chemical_management", []):
            treatment_type = item.get("treatment_type", "")
            chemical_role = item.get("chemical_role", "")
            active_ingredient = item.get("active_ingredient", "")
            timing = item.get("application_timing", "")
            guidance = item.get("application_guidance", "")
            safety = item.get("safety_notes", "")

            title = active_ingredient if active_ingredient and active_ingredient.lower() != "none" else treatment_type
            if not title:
                title = "Chemical-management option"

            details = []
            if treatment_type and title != treatment_type:
                details.append(f"<p><strong>Type:</strong> {treatment_type}</p>")
            if chemical_role:
                details.append(f"<p><strong>Role:</strong> {chemical_role}</p>")
            if timing and timing.lower() != "not applicable":
                details.append(f"<p><strong>Timing:</strong> {timing}</p>")
            if guidance:
                details.append(f"<p><strong>Guidance:</strong> {guidance}</p>")
            if safety:
                details.append(f"<p><strong>Safety:</strong> {safety}</p>")

            blocks.append(
                f'<div class="chatbot-item">'
                f'<strong>{title}</strong>'
                f'{"".join(details)}'
                f'</div>'
            )

        return (
            f'<div class="disease-introduction"><h3>{disease}</h3></div>'
            f'<section class="info-section"><h4>Chemical treatment information</h4>'
            f'{"".join(blocks) or "<p>No chemical treatment information is currently available in the knowledge base.</p>"}'
            f'</section>'
        )

    if intent == "management":
        unique_management = []
        seen_management = set()

        for item in profile["management"]:
            category = item.get("category", "")
            action = item.get("action", "")
            key = (category.strip().lower(), action.strip().lower())

            if key in seen_management:
                continue

            seen_management.add(key)
            unique_management.append(item)

        return (
            f'<div class="disease-introduction"><h3>{disease}</h3></div>'
            + section("Management", unique_management, "category", "action")
        )

    if intent == "sources":
        blocks = []
        for source in profile["sources"]:
            organization = source.get("organization", "")
            title = source.get("title", "")
            url = source.get("url", "")

            if not title and not url:
                continue

            label = organization or "Source"
            text = title or url

            if url:
                text = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'

            blocks.append(
                f'<div class="chatbot-item">'
                f'<strong>{label}</strong>'
                f'<p>{text}</p>'
                f'</div>'
            )

        return (
            f'<div class="disease-introduction"><h3>{disease}</h3></div>'
            f'<section class="info-section"><h4>Sources</h4>'
            f'{"".join(blocks) or "<p>No sources are currently available in the knowledge base.</p>"}'
            f'</section>'
        )

    return "<p>The requested information is not available.</p>"


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

def chatbot_response(user_input, health_problem_id=None):
    """
    Process a user question and retrieve grounded
    information from the knowledge base.

    When health_problem_id is provided, the chatbot uses
    that diagnosis context instead of identifying the
    disease from the user question.
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
    # DIAGNOSIS CONTEXT
    # -----------------------------------------------------

    if health_problem_id:

        profile = get_disease_profile(
            health_problem_id
        )

        if profile is None:
            return (
                "The diagnosis context could not be retrieved "
                "from the knowledge base."
            )

        intent = detect_intent(user_input)

        return format_requested_information(
            profile,
            intent
        )

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