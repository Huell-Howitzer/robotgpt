// theme.js
function setTheme(theme) {
  const themeLink = document.getElementById("theme-style");
  themeLink.href = `/static/css/${theme}-theme.css`;
}

// Get the selected radio button value and call the setTheme function
const radios = document.querySelectorAll('input[name="theme"]');
radios.forEach((radio) => {
  radio.addEventListener("change", function () {
    if (this.checked) {
      setTheme(this.value);
    }
  });
});
