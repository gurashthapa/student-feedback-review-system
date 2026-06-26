from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.user import User
from app import db


class AuthController:

    @staticmethod
    def login():
        if request.method == "POST":

            email = request.form.get("email")
            password = request.form.get("password")

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                login_user(user)

                flash("Login successful.", "success")

                if user.role == "admin":
                    return redirect(url_for("admin.dashboard"))

                elif user.role == "faculty":
                    return redirect(url_for("faculty.dashboard"))

                return redirect(url_for("student.dashboard"))

            flash("Invalid email or password.", "danger")

        return render_template("auth/login.html")


    @staticmethod
    def register():
        if request.method == "POST":

            fullname = request.form.get("fullname")
            email = request.form.get("email")
            password = request.form.get("password")
            role = request.form.get("role")

            existing = User.query.filter_by(email=email).first()

            if existing:
                flash("Email already exists.", "warning")
                return redirect(url_for("auth.register"))

            hashed_password = generate_password_hash(password)

            user = User(
                fullname=fullname,
                email=email,
                password=hashed_password,
                role=role
            )

            db.session.add(user)
            db.session.commit()

            flash("Account created successfully.", "success")

            return redirect(url_for("auth.login"))

        return render_template("auth/register.html")


    @staticmethod
    @login_required
    def logout():

        logout_user()

        flash("Logged out successfully.", "info")

        return redirect(url_for("auth.login"))