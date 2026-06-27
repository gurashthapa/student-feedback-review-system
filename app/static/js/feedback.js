document.addEventListener("DOMContentLoaded", function () {

    const stars = document.querySelectorAll(".star");
    const ratingInput = document.getElementById("rating");
    const ratingText = document.querySelector(".rating-text");
    const emoji = document.querySelector(".emoji-display");
    const selectedRating = document.getElementById("selected-rating");

    const ratings = {
        1: {
            text: "Poor",
            emoji: "😞"
        },
        2: {
            text: "Fair",
            emoji: "😐"
        },
        3: {
            text: "Good",
            emoji: "🙂"
        },
        4: {
            text: "Very Good",
            emoji: "😊"
        },
        5: {
            text: "Excellent",
            emoji: "🤩"
        }
    };

    function updateStars(value) {

        stars.forEach((star, index) => {

            if (index < value) {
                star.classList.remove("far");
                star.classList.add("fas");
                star.style.color = "#fbbf24";
            } else {
                star.classList.remove("fas");
                star.classList.add("far");
                star.style.color = "#d1d5db";
            }

        });

    }

    stars.forEach(star => {

        star.addEventListener("mouseover", function () {

            updateStars(parseInt(this.dataset.value));

        });

        star.addEventListener("mouseout", function () {

            updateStars(parseInt(ratingInput.value || 0));

        });

        star.addEventListener("click", function () {

            const value = parseInt(this.dataset.value);

            ratingInput.value = value;

            updateStars(value);

            emoji.textContent = ratings[value].emoji;

            ratingText.textContent = ratings[value].text;

            selectedRating.textContent = value + " / 5 - " + ratings[value].text;

        });

    });

    const courseSelect = document.querySelector("select[name='course_id']");
    const summaryCourse = document.querySelector(".summary-item strong");

    if (courseSelect && summaryCourse) {

        courseSelect.addEventListener("change", function () {

            if (this.selectedIndex > 0) {
                summaryCourse.textContent =
                    this.options[this.selectedIndex].text;
            } else {
                summaryCourse.textContent = "Select a course";
            }

        });

    }

    const form = document.querySelector("form");

    if (form) {

        form.addEventListener("submit", function (e) {

            if (!ratingInput.value) {

                e.preventDefault();

                alert("Please select a star rating before submitting.");

                return;

            }

            const button = document.querySelector(".submit-btn");

            button.disabled = true;

            button.innerHTML =
                '<i class="fas fa-spinner fa-spin"></i> Submitting...';

        });

    }

});