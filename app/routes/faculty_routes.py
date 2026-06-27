from flask import Blueprint, render_template
from sqlalchemy import func

from app import db
from app.models import Feedback

faculty_bp = Blueprint('faculty', __name__)


@faculty_bp.route("/statistics")
def statistics():
    feedbacks = Feedback.query.order_by(
        Feedback.created_at.desc()
    ).all()

    total_feedback = len(feedbacks)

    avg_rating = db.session.query(
        func.avg(Feedback.rating)
    ).scalar() or 0

    positive_feedback = Feedback.query.filter(
        Feedback.rating >= 4
    ).count()

    negative_feedback = Feedback.query.filter(
        Feedback.rating <= 2
    ).count()

    rating_labels = ["1", "2", "3", "4", "5"]
    rating_values = []

    for rating in range(1, 6):
        count = Feedback.query.filter(
            Feedback.rating == rating
        ).count()
        rating_values.append(count)

    trend_data = (
        db.session.query(
            func.date(Feedback.created_at),
            func.count(Feedback.id)
        )
        .group_by(func.date(Feedback.created_at))
        .order_by(func.date(Feedback.created_at))
        .all()
    )

    trend_labels = [str(item[0]) for item in trend_data]
    trend_values = [item[1] for item in trend_data]

    return render_template(
        "faculty/statistics.html",
        feedbacks=feedbacks,
        avg_rating=round(avg_rating, 2),
        total_feedback=total_feedback,
        positive_feedback=positive_feedback,
        negative_feedback=negative_feedback,
        rating_labels=rating_labels,
        rating_values=rating_values,
        trend_labels=trend_labels,
        trend_values=trend_values,
    )