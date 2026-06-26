from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db

from app.models.user import User
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.department import Department
from app.models.course import Course
from app.models.feedback import Feedback


class AdminController:

    # ==========================
    # Dashboard
    # ==========================

    @staticmethod
    @login_required
    def dashboard():

        total_students = Student.query.count()
        total_faculty = Faculty.query.count()
        total_departments = Department.query.count()
        total_courses = Course.query.count()
        total_feedback = Feedback.query.count()

        recent_feedback = Feedback.query.order_by(
            Feedback.created_at.desc()
        ).limit(5).all()

        return render_template(
            "admin/dashboard.html",
            total_students=total_students,
            total_faculty=total_faculty,
            total_departments=total_departments,
            total_courses=total_courses,
            total_feedback=total_feedback,
            recent_feedback=recent_feedback
        )

    # ==========================
    # Students
    # ==========================

    @staticmethod
    @login_required
    def students():

        students = Student.query.all()

        return render_template(
            "admin/students.html",
            students=students
        )

    @staticmethod
    @login_required
    def delete_student(student_id):

        student = Student.query.get_or_404(student_id)

        db.session.delete(student)
        db.session.commit()

        flash("Student deleted successfully.", "success")

        return redirect(url_for("admin.students"))

    # ==========================
    # Faculty
    # ==========================

    @staticmethod
    @login_required
    def faculty():

        faculty = Faculty.query.all()

        return render_template(
            "admin/faculty.html",
            faculty=faculty
        )

    @staticmethod
    @login_required
    def delete_faculty(faculty_id):

        faculty = Faculty.query.get_or_404(faculty_id)

        db.session.delete(faculty)
        db.session.commit()

        flash("Faculty deleted successfully.", "success")

        return redirect(url_for("admin.faculty"))

    # ==========================
    # Departments
    # ==========================

    @staticmethod
    @login_required
    def departments():

        departments = Department.query.all()

        return render_template(
            "admin/departments.html",
            departments=departments
        )

    @staticmethod
    @login_required
    def add_department():

        if request.method == "POST":

            department_name = request.form.get("department_name")

            department = Department(
                department_name=department_name
            )

            db.session.add(department)
            db.session.commit()

            flash("Department added successfully.", "success")

            return redirect(url_for("admin.departments"))

        return render_template("admin/add_department.html")

    @staticmethod
    @login_required
    def edit_department(department_id):

        department = Department.query.get_or_404(department_id)

        if request.method == "POST":

            department.department_name = request.form.get(
                "department_name"
            )

            db.session.commit()

            flash("Department updated successfully.", "success")

            return redirect(url_for("admin.departments"))

        return render_template(
            "admin/edit_department.html",
            department=department
        )

    @staticmethod
    @login_required
    def delete_department(department_id):

        department = Department.query.get_or_404(department_id)

        db.session.delete(department)
        db.session.commit()

        flash("Department deleted successfully.", "success")

        return redirect(url_for("admin.departments"))

    # ==========================
    # Courses
    # ==========================

    @staticmethod
    @login_required
    def courses():

        courses = Course.query.all()

        return render_template(
            "admin/courses.html",
            courses=courses
        )

    @staticmethod
    @login_required
    def add_course():

        departments = Department.query.all()
        faculty = Faculty.query.all()

        if request.method == "POST":

            course = Course(

                course_name=request.form.get("course_name"),

                department_id=request.form.get("department_id"),

                faculty_id=request.form.get("faculty_id")

            )

            db.session.add(course)
            db.session.commit()

            flash("Course added successfully.", "success")

            return redirect(url_for("admin.courses"))

        return render_template(
            "admin/add_course.html",
            departments=departments,
            faculty=faculty
        )

    @staticmethod
    @login_required
    def edit_course(course_id):

        course = Course.query.get_or_404(course_id)

        departments = Department.query.all()
        faculty = Faculty.query.all()

        if request.method == "POST":

            course.course_name = request.form.get("course_name")
            course.department_id = request.form.get("department_id")
            course.faculty_id = request.form.get("faculty_id")

            db.session.commit()

            flash("Course updated successfully.", "success")

            return redirect(url_for("admin.courses"))

        return render_template(
            "admin/edit_course.html",
            course=course,
            departments=departments,
            faculty=faculty
        )

    @staticmethod
    @login_required
    def delete_course(course_id):

        course = Course.query.get_or_404(course_id)

        db.session.delete(course)
        db.session.commit()

        flash("Course deleted successfully.", "success")

        return redirect(url_for("admin.courses"))

    # ==========================
    # Feedback
    # ==========================

    @staticmethod
    @login_required
    def feedback():

        feedback_list = Feedback.query.order_by(
            Feedback.created_at.desc()
        ).all()

        return render_template(
            "admin/feedback.html",
            feedback_list=feedback_list
        )

    @staticmethod
    @login_required
    def delete_feedback(feedback_id):

        feedback = Feedback.query.get_or_404(feedback_id)

        db.session.delete(feedback)
        db.session.commit()

        flash("Feedback deleted successfully.", "success")

        return redirect(url_for("admin.feedback"))

    # ==========================
    # Reports
    # ==========================

    @staticmethod
    @login_required
    def reports():

        total_students = Student.query.count()
        total_faculty = Faculty.query.count()
        total_feedback = Feedback.query.count()

        return render_template(
            "admin/reports.html",
            total_students=total_students,
            total_faculty=total_faculty,
            total_feedback=total_feedback
        )

    # ==========================
    # Settings
    # ==========================

    @staticmethod
    @login_required
    def settings():

        return render_template(
            "admin/settings.html"
        )