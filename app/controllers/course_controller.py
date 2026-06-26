from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models.course import Course
from app.models.department import Department
from app.models.faculty import Faculty


class CourseController:

    # ==================================
    # Display All Courses
    # ==================================
    @staticmethod
    @login_required
    def index():

        courses = Course.query.order_by(Course.course_name.asc()).all()

        return render_template(
            "admin/courses.html",
            courses=courses
        )

    # ==================================
    # Add Course
    # ==================================
    @staticmethod
    @login_required
    def add():

        departments = Department.query.all()
        faculty = Faculty.query.all()

        if request.method == "POST":

            course_name = request.form.get("course_name")
            course_code = request.form.get("course_code")
            department_id = request.form.get("department_id")
            faculty_id = request.form.get("faculty_id")
            semester = request.form.get("semester")
            credit = request.form.get("credit")

            existing = Course.query.filter_by(
                course_code=course_code
            ).first()

            if existing:

                flash(
                    "Course code already exists.",
                    "warning"
                )

                return redirect(
                    url_for("course.add")
                )

            course = Course(

                course_name=course_name,
                course_code=course_code,
                department_id=department_id,
                faculty_id=faculty_id,
                semester=semester,
                credit=credit

            )

            db.session.add(course)
            db.session.commit()

            flash(
                "Course added successfully.",
                "success"
            )

            return redirect(
                url_for("course.index")
            )

        return render_template(
            "admin/add_course.html",
            departments=departments,
            faculty=faculty
        )

    # ==================================
    # Edit Course
    # ==================================
    @staticmethod
    @login_required
    def edit(course_id):

        course = Course.query.get_or_404(course_id)

        departments = Department.query.all()
        faculty = Faculty.query.all()

        if request.method == "POST":

            course.course_name = request.form.get("course_name")
            course.course_code = request.form.get("course_code")
            course.department_id = request.form.get("department_id")
            course.faculty_id = request.form.get("faculty_id")
            course.semester = request.form.get("semester")
            course.credit = request.form.get("credit")

            db.session.commit()

            flash(
                "Course updated successfully.",
                "success"
            )

            return redirect(
                url_for("course.index")
            )

        return render_template(
            "admin/edit_course.html",
            course=course,
            departments=departments,
            faculty=faculty
        )

    # ==================================
    # Delete Course
    # ==================================
    @staticmethod
    @login_required
    def delete(course_id):

        course = Course.query.get_or_404(course_id)

        db.session.delete(course)
        db.session.commit()

        flash(
            "Course deleted successfully.",
            "success"
        )

        return redirect(
            url_for("course.index")
        )

    # ==================================
    # Course Details
    # ==================================
    @staticmethod
    @login_required
    def details(course_id):

        course = Course.query.get_or_404(course_id)

        return render_template(
            "admin/course_details.html",
            course=course
        )

    # ==================================
    # Search Course
    # ==================================
    @staticmethod
    @login_required
    def search():

        keyword = request.args.get("keyword", "")

        courses = Course.query.filter(
            Course.course_name.contains(keyword)
        ).all()

        return render_template(
            "admin/courses.html",
            courses=courses,
            keyword=keyword
        )

    # ==================================
    # Filter by Department
    # ==================================
    @staticmethod
    @login_required
    def filter_department(department_id):

        courses = Course.query.filter_by(
            department_id=department_id
        ).all()

        return render_template(
            "admin/courses.html",
            courses=courses
        )

    # ==================================
    # Course Statistics
    # ==================================
    @staticmethod
    @login_required
    def statistics():

        total_courses = Course.query.count()

        departments = Department.query.count()

        faculty = Faculty.query.count()

        return render_template(
            "admin/course_statistics.html",
            total_courses=total_courses,
            departments=departments,
            faculty=faculty
        )