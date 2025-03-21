// document.addEventListener("DOMContentLoaded", function () {
//     function loadContent(url) {
//         fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
//             .then(response => {
//                 if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
//                 return response.text();
//             })
//             .then(html => {
//                 document.getElementById("content-area").innerHTML = html;
//                 window.history.pushState({ path: url }, "", url);
//             })
//             .catch(error => console.error("Error loading content:", error));
//     }

//     // Attach event listeners to sidebar links
//     document.querySelectorAll(".sidebar a").forEach(link => {
//         link.addEventListener("click", function (event) {
//             event.preventDefault();
//             let url = this.getAttribute("href");
//             loadContent(url);
//         });
//     });

//     // Sidebar Toggle Function
//     let sidebar = document.querySelector(".sidebar");
//     let toggleButton = document.querySelector(".sidebar-toggle");

//     toggleButton.addEventListener("click", function () {
//         sidebar.classList.toggle("collapsed");
//     });

//     // Handle back/forward navigation
//     window.onpopstate = function (event) {
//         if (event.state && event.state.path) {
//             loadContent(event.state.path);
//         }
//     };

//     // Load correct content on refresh
//     if (window.location.pathname !== "/") {
//         loadContent(window.location.pathname);
//     }
// });







document.addEventListener("DOMContentLoaded", function () {
    function loadContent(url) {
        fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                document.getElementById("content-area").innerHTML = html;
                window.history.pushState({ path: url }, "", url);
                
                // Reinitialize JavaScript for the new page (like pos.html)
                initializePageScripts();    
            })
            .catch(error => console.error("Error loading content:", error));
    }

    // Attach event listeners to sidebar links
    document.querySelectorAll(".sidebar a").forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            let url = this.getAttribute("href");
            loadContent(url);
        });
    });
    
    let sidebar = document.querySelector(".sidebar");
    let toggleButton = document.querySelector(".sidebar-toggle");

    if (toggleButton) {
        toggleButton.addEventListener("click", function () {
            sidebar.classList.toggle("collapsed");
        });
    }

    // Handle back/forward navigation
    window.onpopstate = function (event) {
        if (event.state && event.state.path) {
            loadContent(event.state.path);
        }
    };
    
    function initializePageScripts() {
        if (window.location.pathname.includes("pos")) {
            console.log("POS page detected – initializing POS scripts...");
            
            // Example: Attach event listeners specific to POS
            let addItemButtons = document.querySelectorAll(".add-item");
            addItemButtons.forEach(button => {
                button.addEventListener("click", function () {
                    let itemId = this.dataset.itemId;
                    console.log("Item added to POS:", itemId);
                    // Additional POS-specific logic here
                });
            });
        }
    }

    // Run this once on initial page load
    initializePageScripts();
    });

    // Set the active link on page load
//     updateActiveLink();

//     // Load correct content on refresh
//     if (window.location.pathname !== "/") {
//         loadContent(window.location.pathname);
//     }
// });

// Sidebar toggle function
function toggleSidebar() {
    var sidebar = document.getElementById("sidebar");
    sidebar.style.width = sidebar.style.width === "250px" ? "70px" : "250px";
}


