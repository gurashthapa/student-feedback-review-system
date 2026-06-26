from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models.department import Department
from app.models.course import Course
from app.models.faculty import Faculty
from app.models.student import Student


class DepartmentController:

    # =====================================
    # Display All Departments
    # =====================================
    @staticmethod
    @login_required
    def index():

        departments = Department.query.order_by(
            Department.department_name.asc()
        ).all()

        return render_template(
            "admin/departments.html",
            departments=departments
        )

    # =====================================
    # Add Department
    # =====================================
    @staticmethod
    @login_required
    def add():

        if request.method == "POST":

            department_name = request.form.get("department_name")
            department_code = request.form.get("department_code")

            existing = Department.query.filter_by(
                department_code=department_code
            ).first()

            if existing:

                flash(
                    "Department code already exists.",
                    "warning"
                )

                return redirect(
                    url_for("department.add")
                )

            department = Department(

                department_name=department_name,
                department_code=department_code

            )

            db.session.add(department)
            db.session.commit()

            flash(
                "Department added successfully.",
                "success"
            )

            return redirect(
                url_for("department.index")
            )

        return render_template(
            "admin/add_department.html"
        )

    # =====================================
    # Edit Department
    # =====================================
    @staticmethod
    @login_required
    def edit(department_id):

        department = Department.query.get_or_404(
            department_id
        )

        if request.method == "POST":

            department.department_name = request.form.get(
                "department_name"
            )

            department.department_code = request.form.get(
                "department_code"
            )

            db.session.commit()

            flash(
                "Department updated successfully.",
                "success"
            )

            return redirect(
                url_for("department.index")
            )

        return render_template(
            "admin/edit_department.html",
            department=department
        )

    # =====================================
    # Delete Department
    # =====================================
    @staticmethod
    @login_required
    def delete(department_id):

        department = Department.query.get_or_404(
            department_id
        )

        total_courses = Course.query.filter_by(
            department_id=department.id
        ).count()

        if total_courses > 0:

            flash(
                "Cannot delete department because it has courses.",
                "danger"
            )

            return redirect(
                url_for("department.index")
            )

        db.session.delete(department)
        db.session.commit()

        flash(
            "Department deleted successfully.",
            "success"
        )

        return redirect(
            url_for("department.index")
        )

    # =====================================
    # Department Details
    # =====================================
    @staticmethod
    @login_required
    def details(department_id):

        department = Department.query.get_or_404(
            department_id
        )

        faculty = Faculty.query.filter_by(
            department_id=department.id
        ).all()

        students = Student.query.filter_by(
            department_id=department.id
        ).all()

        courses = Course.query.filter_by(
            department_id=department.id
        ).all()

        return render_template(
            "admin/department_details.html",
            department=department,
            faculty=faculty,
            students=students,
            courses=courses
        )

    # =====================================
    # Search Department
    # =====================================
    @staticmethod
    @login_required
    def search():

        keyword = request.args.get(
            "keyword",
            ""
        )

        departments = Department.query.filter(
            Department.department_name.contains(keyword)
        ).all()

        return render_template(
            "admin/departments.html",
            departments=departments,
            keyword=keyword
        )

    # =====================================
    # Department Statistics
    # =====================================
    @staticmethod
    @login_required
    def statistics():

        total_departments = Department.query.count()

        total_students = Student.query.count()

        total_faculty = Faculty.query.count()

        total_courses = Course.query.count()

        return render_template(
            "admin/department_statistics.html",
            total_departments=total_departments,
            total_students=total_students,
            total_faculty=total_faculty,
            total_courses=total_courses
        )