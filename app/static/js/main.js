document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.querySelector(".menu-toggle");
    const sidebar = document.querySelector(".sidebar");
    const content = document.querySelector(".content");

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener("click", function () {
            sidebar.classList.toggle("active");
        });
    }

    /* Close sidebar when clicking outside (mobile) */
    document.addEventListener("click", function (e) {
        if (
            sidebar &&
            !sidebar.contains(e.target) &&
            toggleBtn &&
            !toggleBtn.contains(e.target) &&
            window.innerWidth <= 991
        ) {
            sidebar.classList.remove("active");
        }
    });
});


function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    if (!dropdown) return;

    dropdown.classList.toggle("show");
}

window.addEventListener("click", function (e) {
    document.querySelectorAll(".dropdown-menu").forEach(menu => {
        if (!menu.contains(e.target)) {
            menu.classList.remove("show");
        }
    });
});


function autoHideAlerts() {
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = "0";
            alert.style.transition = "0.5s ease";

            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 3000);
    });
}


function setLoadingState(button, isLoading) {
    if (!button) return;

    if (isLoading) {
        button.disabled = true;
        button.dataset.originalText = button.innerHTML;
        button.innerHTML = "Loading...";
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText || "Submit";
    }
}

function tableSearch(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);

    if (!input || !table) return;

    input.addEventListener("keyup", function () {
        const filter = input.value.toLowerCase();
        const rows = table.getElementsByTagName("tr");

        for (let i = 1; i < rows.length; i++) {
            let rowText = rows[i].textContent.toLowerCase();

            if (rowText.includes(filter)) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    });
}


function confirmDelete(message = "Are you sure you want to delete this item?") {
    return confirm(message);
}

function togglePassword(inputId, iconId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);

    if (!input) return;

    if (input.type === "password") {
        input.type = "text";
        if (icon) icon.classList.add("fa-eye-slash");
    } else {
        input.type = "password";
        if (icon) icon.classList.remove("fa-eye-slash");
    }
}


function setActiveMenu() {
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll(".sidebar a");

    menuItems.forEach(item => {
        if (item.getAttribute("href") === currentPath) {
            item.classList.add("active");
        }
    });
}


document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
        e.preventDefault();

        const target = document.querySelector(this.getAttribute("href"));

        if (target) {
            target.scrollIntoView({
                behavior: "smooth"
            });
        }
    });
});


function updateNotificationCount(count) {
    const badge = document.querySelector(".notification-badge");
    if (!badge) return;

    badge.textContent = count;

    if (count === 0) {
        badge.style.display = "none";
    } else {
        badge.style.display = "inline-block";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    autoHideAlerts();
    setActiveMenu();
});