import csv
import io
from flask import Response

def generate_csv_response(filename, header, rows):
    """
    Create downloadable CSV response

    :param filename: name of file (e.g. students.csv)
    :param header: list of column names
    :param rows: list of tuples/lists (data rows)
    """

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(header)

    # Write data rows
    for row in rows:
        writer.writerow(row)

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


def export_students_csv(students):
    header = ["ID", "Name", "Email", "Department", "Semester", "Created At"]

    rows = [
        (
            s.id,
            s.name,
            s.email,
            getattr(s, "department", ""),
            getattr(s, "semester", ""),
            getattr(s, "created_at", "")
        )
        for s in students
    ]

    return generate_csv_response("students.csv", header, rows)


def export_faculty_csv(faculty_list):
    header = ["ID", "Name", "Email", "Department", "Designation"]

    rows = [
        (
            f.id,
            f.name,
            f.email,
            getattr(f, "department", ""),
            getattr(f, "designation", "")
        )
        for f in faculty_list
    ]

    return generate_csv_response("faculty.csv", header, rows)


def export_feedback_csv(feedback_list):
    header = ["ID", "Student", "Faculty", "Course", "Rating", "Comment", "Date"]

    rows = [
        (
            fb.id,
            getattr(fb, "student_name", ""),
            getattr(fb, "faculty_name", ""),
            getattr(fb, "course_name", ""),
            fb.rating,
            fb.comment,
            getattr(fb, "created_at", "")
        )
        for fb in feedback_list
    ]

    return generate_csv_response("feedback.csv", header, rows)


def export_courses_csv(courses):
    header = ["ID", "Course Name", "Department", "Credits"]

    rows = [
        (
            c.id,
            c.name,
            getattr(c, "department", ""),
            getattr(c, "credits", "")
        )
        for c in courses
    ]

    return generate_csv_response("courses.csv", header, rows)

def export_custom_csv(filename, data, header):
    """
    Flexible exporter for any custom report
    """
    return generate_csv_response(filename, header, data)