const usernameField = document.querySelector("#usernameField");
const usernameFeedbackArea = document.querySelector("#usernameFeedback");
const usernameSuccess = document.querySelector("#usernameSuccess");

const emailField = document.querySelector("#emailField");
const emailFeedbackArea = document.querySelector("#emailFeedback");
const emailSuccess = document.querySelector("#emailSuccess");

const passwordField = document.querySelector("#passwordField");
const showPasswordToggle = document.querySelector(".showPasswordToggle");

const submitBtn = document.querySelector(".submit-btn");

usernameField.addEventListener("keyup", (e) => {
  const usernameValue = e.target.value;

  usernameField.classList.remove("is-invalid");
  usernameField.classList.remove("is-valid");
  usernameFeedbackArea.style.display = "none";

  if (usernameValue.length > 0) {
    usernameSuccess.style.display = "block";
    usernameSuccess.textContent = `Checking ${usernameValue}`;

    fetch("/auth/validate-username/", {
      body: JSON.stringify({
        username: usernameValue,
      }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        usernameSuccess.style.display = "none";

        if (data.username_error) {
          // disable submit button
          submitBtn.disabled = true;
          usernameField.classList.add("is-invalid");
          usernameFeedbackArea.style.display = "block";
          usernameFeedbackArea.innerHTML = `<p>${data.username_error}</p>`;
        }
        if (data.username_valid) {
          submitBtn.removeAttribute("disabled");
          usernameField.classList.add("is-valid");
        }
      });
  }
});

emailField.addEventListener("keyup", (e) => {
  const emailValue = e.target.value;

  emailField.classList.remove("is-invalid");
  emailField.classList.remove("is-valid");
  emailFeedbackArea.style.display = "none";

  if (emailValue.length > 0) {
    emailSuccess.style.display = "block";
    emailSuccess.textContent = `Checking ${emailValue}`;

    fetch("/auth/validate-email/", {
      body: JSON.stringify({
        email: emailValue,
      }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        emailSuccess.style.display = "none";

        if (data.email_error) {
          // disable submit btn
          submitBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedbackArea.style.display = "block";
          emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
        }
        if (data.email_valid) {
          submitBtn.removeAttribute("disabled");
          emailField.classList.add("is-valid");
        }
      });
  }
});

showPasswordToggle.addEventListener("click", () => {
  if (showPasswordToggle.textContent === "View Password") {
    showPasswordToggle.textContent = "Hide Password";
    passwordField.setAttribute("type", "text");
  } else {
    showPasswordToggle.textContent = "View Password";
    passwordField.setAttribute("type", "password");
  }
});
