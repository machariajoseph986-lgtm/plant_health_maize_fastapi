# PURPOSE: Provide the PostgreSQL database layer for the Plant Health Maize Project.
# EXPECTED OUTPUT: PostgreSQL versions of the existing knowledge-base functions
#                  with the same return structure as the SQLite database layer.

import os
import json
import psycopg
from dotenv import load_dotenv

load_dotenv()  # Load environment va


POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "plant_health")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")


def get_connection():
    """
    Create a PostgreSQL connection to the Plant Health database.

    The PostgreSQL password is read from the
    POSTGRES_PASSWORD environment variable.
    """

    password = os.getenv("POSTGRES_PASSWORD")

    if not password:
        raise RuntimeError(
            "POSTGRES_PASSWORD environment variable is not set."
        )

    return psycopg.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DATABASE,
        user=POSTGRES_USER,
        password=password
    )


def get_disease_profile(health_problem_id):
    """
    Retrieve a complete disease profile from PostgreSQL.
    """

    query = """
    SELECT
        hp.health_problem_id,
        hp.name AS disease,
        p.common_name AS crop,
        hp.type,
        hp.description
    FROM health_problems hp
    JOIN plants p
        ON hp.plant_id = p.plant_id
    WHERE hp.health_problem_id = %s
    """

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                query,
                (health_problem_id,)
            )

            row = cursor.fetchone()

    if row is None:
        return None

    profile = {
        "health_problem_id": row[0],
        "disease": row[1],
        "crop": row[2],
        "type": row[3],
        "description": row[4],
        "pathogens": [],
        "symptoms": [],
        "transmission": [],
        "conditions": [],
        "management": [],
        "sources": []
    }

    detail_queries = {

        "pathogens": """
            SELECT
                scientific_name,
                type,
                role
            FROM pathogens
            WHERE health_problem_id = %s
            ORDER BY pathogen_id
        """,

        "symptoms": """
            SELECT
                category,
                description
            FROM symptoms
            WHERE health_problem_id = %s
            ORDER BY symptom_id
        """,

        "transmission": """
            SELECT
                method,
                description
            FROM transmission
            WHERE health_problem_id = %s
            ORDER BY transmission_id
        """,

        "conditions": """
            SELECT
                factor,
                value,
                description
            FROM conditions
            WHERE health_problem_id = %s
            ORDER BY condition_id
        """,

        "management": """
            SELECT
                category,
                action
            FROM management
            WHERE health_problem_id = %s
            ORDER BY management_id
        """,

        "sources": """
            SELECT
                organization,
                title,
                url
            FROM sources
            WHERE health_problem_id = %s
            ORDER BY source_id
        """
    }

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                detail_queries["pathogens"],
                (health_problem_id,)
            )

            profile["pathogens"] = [
                {
                    "scientific_name": row[0],
                    "type": row[1],
                    "role": row[2]
                }
                for row in cursor.fetchall()
            ]

            cursor.execute(
                detail_queries["symptoms"],
                (health_problem_id,)
            )

            profile["symptoms"] = [
                {
                    "category": row[0],
                    "description": row[1]
                }
                for row in cursor.fetchall()
            ]

            cursor.execute(
                detail_queries["transmission"],
                (health_problem_id,)
            )

            profile["transmission"] = [
                {
                    "method": row[0],
                    "description": row[1]
                }
                for row in cursor.fetchall()
            ]

            cursor.execute(
                detail_queries["conditions"],
                (health_problem_id,)
            )

            profile["conditions"] = [
                {
                    "factor": row[0],
                    "value": row[1],
                    "description": row[2]
                }
                for row in cursor.fetchall()
            ]

            cursor.execute(
                detail_queries["management"],
                (health_problem_id,)
            )

            profile["management"] = [
                {
                    "category": row[0],
                    "action": row[1]
                }
                for row in cursor.fetchall()
            ]

            cursor.execute(
                detail_queries["sources"],
                (health_problem_id,)
            )

            profile["sources"] = [
                {
                    "organization": row[0],
                    "title": row[1],
                    "url": row[2]
                }
                for row in cursor.fetchall()
            ]

    return profile


def get_all_diseases():
    """
    Retrieve all health problems from PostgreSQL.
    """

    query = """
    SELECT
        hp.health_problem_id,
        hp.name AS disease,
        p.common_name AS crop,
        hp.type
    FROM health_problems hp
    JOIN plants p
        ON hp.plant_id = p.plant_id
    ORDER BY p.common_name, hp.name;
    """

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(query)

            rows = cursor.fetchall()

    return [
        {
            "health_problem_id": row[0],
            "disease": row[1],
            "crop": row[2],
            "type": row[3]
        }
        for row in rows
    ]


def find_disease(search_term):
    """
    Search PostgreSQL for diseases matching a search term.
    """

    search_term = search_term.strip().lower()

    aliases = {
        "mln": "maize lethal necrosis"
    }

    search_term = aliases.get(
        search_term,
        search_term
    )

    query = """
    SELECT
        hp.health_problem_id,
        hp.name AS disease,
        p.common_name AS crop,
        hp.type
    FROM health_problems hp
    JOIN plants p
        ON hp.plant_id = p.plant_id
    WHERE
        LOWER(hp.name) LIKE %s
        OR LOWER(p.common_name) LIKE %s
    ORDER BY hp.name;
    """

    pattern = f"%{search_term}%"

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                query,
                (pattern, pattern)
            )

            rows = cursor.fetchall()

    return [
        {
            "health_problem_id": row[0],
            "disease": row[1],
            "crop": row[2],
            "type": row[3]
        }
        for row in rows
    ]