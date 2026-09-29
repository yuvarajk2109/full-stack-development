/*
  TODO 1: Select the elements.
  Use document.getElementById to grab the form (id="login-form").
  Use document.querySelector to grab the username input (#username),
  the password input (#password), and the message element (.message).
*/
const form = document.getElementById("login-form"); // replace with document.getElementById("login-form")
const usernameInput = document.querySelector("#username"); // replace with document.querySelector("#username")
const passwordInput = document.querySelector("#password"); // replace with document.querySelector("#password")
const message = document.querySelector(".message"); // replace with document.querySelector(".message")

function showMessage(text, kind) {
  message.textContent = text;
  message.classList.remove("hidden", "error", "success");
  message.classList.add(kind);
}

function markInvalid(input, isInvalid) {
  input.classList.toggle("invalid", isInvalid);
}

/*
  TODO 2: Handle the submit event.
  Add a "submit" listener to form. Inside it:
    - call event.preventDefault() so the page doesn't reload
    - read usernameInput.value and passwordInput.value
    - decide usernameOk (length >= 3) and passwordOk (length >= 8)
    - call markInvalid() on each input with the opposite of *Ok
    - if either is invalid, call showMessage() with kind "error" and
      return
    - otherwise call showMessage() with kind "success", then
      form.reset() and clear both invalid classes
*/

form.addEventListener("submit", (event) => {
    event.preventDefault();
    const username = usernameInput.value.trim();
    const password = passwordInput.value;

    const usernameOk = username.length >= 3;
    const passwordOk = password.length >= 8;

    markInvalid(usernameInput, !usernameOk);
    markInvalid(passwordInput, !passwordOk);

    if (!usernameOk || !passwordOk) {
      showMessage("Username or password invalid", "error");
    }
    return;

    showMessage("All good!", "success");
    form.reset();
    markInvalid(usernameInput, false);
    markInvalid(passwordInput, false);
  }
);


/*
  TODO 3: React as the user types.
  Add an "input" listener to usernameInput that removes the invalid
  class as soon as the value reaches 3+ characters, so the error
  clears itself without waiting for another submit.
*/

usernameInput.addEventListener("input", (event) => {
  if (username.value.trim().length >= 3) {
    markInvalid(usernameInput, false);
  }
})
