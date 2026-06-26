from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.user import User
from app.models.student import Student
from app.models.faculty import Faculty


class ProfileController:

    # ==========================================
    # View Profile
    # ==========================================
    @staticmethod
    @login_required
    def index():

        user = User.query.get(current_user.id)

        student = None
        faculty = None

        if user.role == "student":
            student = Student.query.filter_by(
                user_id=user.id
            ).first()

        elif user.role == "faculty":
            faculty = Faculty.query.filter_by(
                user_id=user.id
            ).first()

        return render_template(
            "profile/profile.html",
            user=user,
            student=student,
            faculty=faculty
        )

    # ==========================================
    # Update Profile
    # ==========================================
    @staticmethod
    @login_required
    def update():

        user = User.query.get(current_user.id)

        if request.method == "POST":

            user.fullname = request.form.get("fullname")
            user.email = request.form.get("email")

            if user.role == "student":

                student = Student.query.filter_by(
                    user_id=user.id
                ).first()

                student.phone = request.form.get("phone")
                student.address = request.form.get("address")
                student.year = request.form.get("year")
                student.semester = request.form.get("semester")

            elif user.role == "faculty":

                faculty = Faculty.query.filter_by(
                    user_id=user.id
                ).first()

                faculty.phone = request.form.get("phone")
                faculty.address = request.form.get("address")
                faculty.designation = request.form.get("designation")

            db.session.commit()

            flash(
                "Profile updated successfully.",
                "success"
            )

            return redirect(
                url_for("profile.index")
            )

        return render_template(
            "profile/edit_profile.html",
            user=user
        )

    # ==========================================
    # Change Password
    # ==========================================
    @staticmethod
    @login_required
    def change_password():

        user = User.query.get(current_user.id)

        if request.method == "POST":

            current_password = request.form.get(
                "current_password"
            )

            new_password = request.form.get(
                "new_password"
            )

            confirm_password = request.form.get(
                "confirm_password"
            )

            if not check_password_hash(
                user.password,
                current_password
            ):

                flash(
                    "Current password is incorrect.",
                    "danger"
                )

                return redirect(
                    url_for("profile.change_password")
                )

            if new_password != confirm_password:

                flash(
                    "Passwords do not match.",
                    "warning"
                )

                return redirect(
                    url_for("profile.change_password")
                )

            user.password = generate_password_hash(
                new_password
            )

            db.session.commit()

            flash(
                "Password changed successfully.",
                "success"
            )

            return redirect(
                url_for("profile.index")
            )

        return render_template(
            "profile/change_password.html"
        )

    # ==========================================
    # Upload Profile Image
    # ==========================================
    @staticmethod
    @login_required
    def upload_photo():

        user = User.query.get(current_user.id)

        if request.method == "POST":

            image = request.files.get("profile_image")

            if image and image.filename != "":

                filename = image.filename

                image.save(
                    "app/static/uploads/" + filename
                )

                user.profile_image = filename

                db.session.commit()

                flash(
                    "Profile image uploaded successfully.",
                    "success"
                )

                return redirect(
                    url_for("profile.index")
                )

            flash(
                "Please select an image.",
                "warning"
            )

        return render_template(
            "profile/upload_photo.html"
        )

    # ==========================================
    # Delete Profile Photo
    # ==========================================
    @staticmethod
    @login_required
    def remove_photo():

        user = User.query.get(current_user.id)

        user.profile_image = "default.png"

        db.session.commit()

        flash(
            "Profile photo removed successfully.",
            "success"
        )

        return redirect(
            url_for("profile.index")
        )