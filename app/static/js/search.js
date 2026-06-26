function liveSearch(inputId, itemClass) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener("keyup", function () {
        const filter = this.value.toLowerCase();
        const items = document.querySelectorAll("." + itemClass);

        items.forEach(item => {
            const text = item.textContent.toLowerCase();

            if (text.includes(filter)) {
                item.style.display = "";
            } else {
                item.style.display = "none";
            }
        });
    });
}


function columnSearch(inputId, tableId, columnIndex) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);

    if (!input || !table) return;

    input.addEventListener("keyup", function () {
        const filter = this.value.toLowerCase();
        const rows = table.getElementsByTagName("tr");

        for (let i = 1; i < rows.length; i++) {
            const cells = rows[i].getElementsByTagName("td");

            if (cells[columnIndex]) {
                const cellText = cells[columnIndex].textContent.toLowerCase();

                if (cellText.includes(filter)) {
                    rows[i].style.display = "";
                } else {
                    rows[i].style.display = "none";
                }
            }
        }
    });
}


function dropdownFilter(selectId, itemClass, attributeName) {
    const select = document.getElementById(selectId);
    if (!select) return;

    select.addEventListener("change", function () {
        const value = this.value.toLowerCase();
        const items = document.querySelectorAll("." + itemClass);

        items.forEach(item => {
            const attrValue = item.getAttribute(attributeName);

            if (!value || attrValue === value) {
                item.style.display = "";
            } else {
                item.style.display = "none";
            }
        });
    });
}

function multiFieldSearch(inputId, itemClass, fields = []) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener("keyup", function () {
        const filter = this.value.toLowerCase();
        const items = document.querySelectorAll("." + itemClass);

        items.forEach(item => {
            let matchFound = false;

            fields.forEach(field => {
                const el = item.querySelector("." + field);

                if (el && el.textContent.toLowerCase().includes(filter)) {
                    matchFound = true;
                }
            });

            item.style.display = matchFound ? "" : "none";
        });
    });
}

function autocompleteSearch(inputId, dataList) {
    const input = document.getElementById(inputId);
    if (!input) return;

    let currentFocus;

    input.addEventListener("input", function () {
        let val = this.value;

        closeAllLists();

        if (!val) return false;

        currentFocus = -1;

        const list = document.createElement("div");
        list.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(list);

        dataList.forEach(item => {
            if (item.substr(0, val.length).toLowerCase() === val.toLowerCase()) {

                const itemDiv = document.createElement("div");

                itemDiv.innerHTML = "<strong>" + item.substr(0, val.length) + "</strong>";
                itemDiv.innerHTML += item.substr(val.length);

                itemDiv.addEventListener("click", function () {
                    input.value = item;
                    closeAllLists();
                });

                list.appendChild(itemDiv);
            }
        });
    });

    function closeAllLists() {
        document.querySelectorAll(".autocomplete-items").forEach(el => el.remove());
    }

    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

function highlightSearchText(inputId, containerClass) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener("keyup", function () {
        const filter = this.value.toLowerCase();
        const containers = document.querySelectorAll("." + containerClass);

        containers.forEach(container => {
            const text = container.textContent;

            if (!filter) {
                container.innerHTML = text;
                return;
            }

            const regex = new RegExp(filter, "gi");
            container.innerHTML = text.replace(regex, match => {
                return `<span class="highlight">${match}</span>`;
            });
        });
    });
}


function clearSearch(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        input.value = "";
        input.dispatchEvent(new Event("keyup"));
    }
}

document.addEventListener("DOMContentLoaded", function () {

    
});