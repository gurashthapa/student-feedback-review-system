import csv
from io import StringIO

from flask import (
    render_template,
    make_response
)

from flask_login import login_required
from sqlalchemy import func

from app import db
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.department import Department
from app.models.course import Course
from app.models.feedback import Feedback


class ReportController:

    # =====================================
    # Dashboard Report
    # =====================================

    @staticmethod
    @login_required
    def dashboard():

        total_students = Student.query.count()
        total_faculty = Faculty.query.count()
        total_departments = Department.query.count()
        total_courses = Course.query.count()
        total_feedback = Feedback.query.count()

        average_rating = db.session.query(
            func.avg(Feedback.rating)
        ).scalar()

        if average_rating is None:
            average_rating = 0

        return render_template(
            "admin/reports/dashboard.html",
            total_students=total_students,
            total_faculty=total_faculty,
            total_departments=total_departments,
            total_courses=total_courses,
            total_feedback=total_feedback,
            average_rating=round(average_rating, 2)
        )

    # =====================================
    # Student Report
    # =====================================

    @staticmethod
    @login_required
    def students():

        students = Student.query.all()

        return render_template(
            "admin/reports/students.html",
            students=students
        )

    # =====================================
    # Faculty Report
    # =====================================

    @staticmethod
    @login_required
    def faculty():

        faculty = Faculty.query.all()

        return render_template(
            "admin/reports/faculty.html",
            faculty=faculty
        )

    # =====================================
    # Department Report
    # =====================================

    @staticmethod
    @login_required
    def departments():

        departments = Department.query.all()

        return render_template(
            "admin/reports/departments.html",
            departments=departments
        )

    # =====================================
    # Course Report
    # =====================================

    @staticmethod
    @login_required
    def courses():

        courses = Course.query.all()

        return render_template(
            "admin/reports/courses.html",
            courses=courses
        )

    # =====================================
    # Feedback Report
    # =====================================

    @staticmethod
    @login_required
    def feedback():

        feedbacks = Feedback.query.order_by(
            Feedback.created_at.desc()
        ).all()

        return render_template(
            "admin/reports/feedback.html",
            feedbacks=feedbacks
        )

    # =====================================
    # Rating Statistics
    # =====================================

    @staticmethod
    @login_required
    def ratings():

        five = Feedback.query.filter_by(rating=5).count()
        four = Feedback.query.filter_by(rating=4).count()
        three = Feedback.query.filter_by(rating=3).count()
        two = Feedback.query.filter_by(rating=2).count()
        one = Feedback.query.filter_by(rating=1).count()

        return render_template(
            "admin/reports/ratings.html",
            five=five,
            four=four,
            three=three,
            two=two,
            one=one
        )

    # =====================================
    # Top Rated Faculty
    # =====================================

    @staticmethod
    @login_required
    def top_faculty():

        faculty = db.session.query(

            Faculty,

            func.avg(
                Feedback.rating
            ).label("average")

        ).join(

            Feedback,
            Faculty.id == Feedback.faculty_id

        ).group_by(

            Faculty.id

        ).order_by(

            func.avg(
                Feedback.rating
            ).desc()

        ).all()

        return render_template(
            "admin/reports/top_faculty.html",
            faculty=faculty
        )

    # =====================================
    # Feedback per Department
    # =====================================

    @staticmethod
    @login_required
    def department_summary():

        report = db.session.query(

            Department.department_name,

            func.count(
                Feedback.id
            )

        ).join(

            Course,
            Department.id == Course.department_id

        ).join(

            Feedback,
            Course.id == Feedback.course_id

        ).group_by(

            Department.department_name

        ).all()

        return render_template(
            "admin/reports/department_summary.html",
            report=report
        )

    # =====================================
    # Export Feedback CSV
    # =====================================

    @staticmethod
    @login_required
    def export_feedback_csv():

        feedbacks = Feedback.query.all()

        output = StringIO()

        writer = csv.writer(output)

        writer.writerow([
            "Student ID",
            "Faculty ID",
            "Course ID",
            "Rating",
            "Review",
            "Date"
        ])

        for feedback in feedbacks:

            writer.writerow([

                feedback.student_id,

                feedback.faculty_id,

                feedback.course_id,

                feedback.rating,

                feedback.review,

                feedback.created_at

            ])

        response = make_response(output.getvalue())

        response.headers[
            "Content-Disposition"
        ] = "attachment; filename=feedback_report.csv"

        response.headers[
            "Content-Type"
        ] = "text/csv"

        return response

    # =====================================
    # Overall Statistics
    # =====================================

    @staticmethod
    @login_required
    def statistics():

        statistics = {

            "students": Student.query.count(),

            "faculty": Faculty.query.count(),

            "departments": Department.query.count(),

            "courses": Course.query.count(),

            "feedback": Feedback.query.count(),

            "average_rating": round(

                db.session.query(

                    func.avg(
                        Feedback.rating
                    )

                ).scalar() or 0,

                2

            )

        }

        return render_template(
            "admin/reports/statistics.html",
            statistics=statistics
        )