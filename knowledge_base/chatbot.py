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
    Convert a complete disease profile into a readable
    chatbot response.
    """

    response = []

    response.append(
        f"{profile['disease']} is a {profile['type']} "
        f"health problem affecting {profile['crop']}."
    )

    # -----------------------------------------------------
    # PATHOGENS
    # -----------------------------------------------------

    if profile["pathogens"]:

        response.append("\nCausing organism(s):")

        for pathogen in profile["pathogens"]:

            scientific_name = pathogen.get(
                "scientific_name",
                "Unknown"
            )

            pathogen_type = pathogen.get(
                "type",
                "Unknown"
            )

            role = pathogen.get(
                "role",
                ""
            )

            text = f"- {scientific_name} ({pathogen_type})"

            if role:
                text += f": {role}"

            response.append(text)

    # -----------------------------------------------------
    # SYMPTOMS
    # -----------------------------------------------------

    if profile["symptoms"]:

        response.append("\nSymptoms:")

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

    # -----------------------------------------------------
    # TRANSMISSION
    # -----------------------------------------------------

    if profile["transmission"]:

        response.append("\nTransmission:")

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

    # -----------------------------------------------------
    # CONDITIONS
    # -----------------------------------------------------

    if profile["conditions"]:

        response.append("\nFavourable conditions:")

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

    # -----------------------------------------------------
    # MANAGEMENT
    # -----------------------------------------------------

    if profile["management"]:

        response.append("\nManagement:")

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

    # -----------------------------------------------------
    # SOURCES
    # -----------------------------------------------------

    if profile["sources"]:

        response.append("\nSources:")

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