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
