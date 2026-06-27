document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("historySearch");
    const table = document.getElementById("historyTable");

    if (!searchInput || !table) return;

    searchInput.addEventListener("keyup", function () {

        const value = this.value.toLowerCase();
        const rows = table.querySelectorAll("tbody tr");

        rows.forEach(row => {

            const text = row.innerText.toLowerCase();

            if (text.includes(value)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });

});