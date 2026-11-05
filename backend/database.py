import os
from dotenv import load_dotenv

load_dotenv()

import mysql.connector
from mysql.connector import Error


def get_db_connection():
    """
    Establish and return a MySQL database connection.
    """
    try:
        connection = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "resume_analyzer")
)

        if connection.is_connected():
            print("MySQL Connected Successfully")
            return connection

    except Error as error:
        print("MySQL Connection Error:", error)

    return None

def save_analysis(filename, match_score, resume_skills,
                  required_skills, matched_skills, missing_skills):
    """
    Save resume analysis results into MySQL.
    """
    connection = get_db_connection()

    if connection is None:
        return False

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO analysis_history (
                filename,
                match_score,
                resume_skills,
                required_skills,
                matched_skills,
                missing_skills
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            filename,
            match_score,
            ", ".join(resume_skills),
            ", ".join(required_skills),
            ", ".join(matched_skills),
            ", ".join(missing_skills)
        )

        cursor.execute(query, values)
        connection.commit()

        print("Analysis saved successfully!")
        return True

    except Error as error:
        print("Error saving analysis:", error)
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_analysis_history():
    """
    Retrieve all saved resume analyses.
    """
    connection = get_db_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT *
            FROM analysis_history
            ORDER BY created_at DESC
        """

        cursor.execute(query)
        results = cursor.fetchall()

        return results

    except Error as error:
        print("Error retrieving analysis history:", error)
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_analysis(analysis_id):
    """
    Delete a resume analysis using its ID.
    """
    connection = get_db_connection()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            DELETE FROM analysis_history
            WHERE id = %s
        """

        cursor.execute(query, (analysis_id,))
        connection.commit()

        if cursor.rowcount > 0:
            print("Analysis deleted successfully!")
            return True

        return False

    except Error as error:
        print("Error deleting analysis:", error)
        return None

    finally:
        if cursor:
            cursor.close()

        connection.close()

def get_dashboard_stats():
    """
    Retrieve dashboard statistics from MySQL.
    """
    connection = get_db_connection()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                COUNT(*) AS total_analyses,
                COALESCE(ROUND(AVG(match_score), 2), 0)
                    AS average_score,
                COALESCE(MAX(match_score), 0)
                    AS best_score,
                COALESCE(
                    SUM(DATE(created_at) = CURDATE()), 0
                ) AS analyses_today
            FROM analysis_history
        """

        cursor.execute(query)
        result = cursor.fetchone()

        return result

    except Error as error:
        print("Error retrieving dashboard statistics:", error)
        return None

    finally:
        if cursor:
            cursor.close()

        connection.close()

