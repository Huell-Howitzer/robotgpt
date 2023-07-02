function startHyperloop() {
  $.ajax({
    type: "POST",
    url: "/start_hyperloop",
    data: $("form").serialize(),
    success: function (data, status, request) {
      const statusUrl = request.getResponseHeader("Location");
      updateProgress(statusUrl);
    },
    error: function () {
      alert("Unexpected error");
    },
  });
}

function updateProgress(statusUrl) {
  $.getJSON(statusUrl, function (data) {
    // Update your progress fields with data.iteration and data.similarity
    // If the task is still running, call updateProgress again after a delay
    if (data.state === "PROGRESS") {
      setTimeout(function () {
        updateProgress(statusUrl);
      }, 2000);
    }
  });
}
// Get the side nav and content elements
const sideNav = document.querySelector(".side-nav");
const content = document.querySelector(".content");

// Add event listeners for mouseover and mouseout
sideNav.addEventListener("mouseover", expandSideNav);
sideNav.addEventListener("mouseout", collapseSideNav);

// Function to expand the side nav
function expandSideNav() {
  sideNav.classList.add("expanded");
  content.classList.add("expanded");
}

// Function to collapse the side nav
function collapseSideNav() {
  sideNav.classList.remove("expanded");
  content.classList.remove("expanded");
}