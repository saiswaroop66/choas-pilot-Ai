from database.database import get_connection


# =========================================================
# USERS
# =========================================================

def create_user(name, email, password):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
        """,
        (name, email, password)
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


def get_user_by_email(email):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    return user


# =========================================================
# APPLICATIONS
# =========================================================

def create_application(
    user_id,
    name,
    description="",
    repository="",
    environment="development"
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO applications
        (
            user_id,
            name,
            description,
            repository,
            environment
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            name,
            description,
            repository,
            environment
        )
    )

    connection.commit()

    application_id = cursor.lastrowid

    connection.close()

    return application_id


def get_application(application_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM applications
        WHERE id = ?
        """,
        (application_id,)
    )

    application = cursor.fetchone()

    connection.close()

    return application


def get_user_applications(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM applications
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    applications = cursor.fetchall()

    connection.close()

    return applications


def delete_application(application_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM applications
        WHERE id = ?
        """,
        (application_id,)
    )

    connection.commit()

    connection.close()

    return True


# =========================================================
# ANALYSIS
# =========================================================

def create_analysis(
    application_id,
    analysis_type,
    result
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO analyses
        (
            application_id,
            analysis_type,
            result
        )
        VALUES (?, ?, ?)
        """,
        (
            application_id,
            analysis_type,
            result
        )
    )

    connection.commit()

    analysis_id = cursor.lastrowid

    connection.close()

    return analysis_id


def get_application_analyses(application_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM analyses
        WHERE application_id = ?
        ORDER BY created_at DESC
        """,
        (application_id,)
    )

    analyses = cursor.fetchall()

    connection.close()

    return analyses


# =========================================================
# FAILURES
# =========================================================

def create_failure(
    application_id,
    component,
    severity,
    file_name,
    function_name,
    line_number,
    root_cause,
    impact,
    recommendation
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO failures
        (
            application_id,
            component,
            severity,
            file_name,
            function_name,
            line_number,
            root_cause,
            impact,
            recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            application_id,
            component,
            severity,
            file_name,
            function_name,
            line_number,
            root_cause,
            impact,
            recommendation
        )
    )

    connection.commit()

    failure_id = cursor.lastrowid

    connection.close()

    return failure_id


def get_application_failures(application_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM failures
        WHERE application_id = ?
        ORDER BY created_at DESC
        """,
        (application_id,)
    )

    failures = cursor.fetchall()

    connection.close()

    return failures


# =========================================================
# EXPERIMENTS
# =========================================================

def create_experiment(
    application_id,
    experiment_name,
    failure_type
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO experiments
        (
            application_id,
            experiment_name,
            failure_type
        )
        VALUES (?, ?, ?)
        """,
        (
            application_id,
            experiment_name,
            failure_type
        )
    )

    connection.commit()

    experiment_id = cursor.lastrowid

    connection.close()

    return experiment_id


def update_experiment(
    experiment_id,
    status,
    result
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE experiments
        SET status = ?, result = ?
        WHERE id = ?
        """,
        (
            status,
            result,
            experiment_id
        )
    )

    connection.commit()

    connection.close()


def get_application_experiments(application_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM experiments
        WHERE application_id = ?
        ORDER BY created_at DESC
        """,
        (application_id,)
    )

    experiments = cursor.fetchall()

    connection.close()

    return experiments


# =========================================================
# REPORTS
# =========================================================

def create_report(
    application_id,
    title,
    content,
    resilience_score
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO reports
        (
            application_id,
            title,
            content,
            resilience_score
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            application_id,
            title,
            content,
            resilience_score
        )
    )

    connection.commit()

    report_id = cursor.lastrowid

    connection.close()

    return report_id


def get_application_reports(application_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM reports
        WHERE application_id = ?
        ORDER BY created_at DESC
        """,
        (application_id,)
    )

    reports = cursor.fetchall()

    connection.close()

    return reports
