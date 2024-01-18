const fieldPass = document.getElementById("password");
const fieldPassCheck = document.getElementById("password-repeat");
const warning = document.getElementById("password-warning");

function checkPasswords() {
  const pass1 = fieldPass.value;
  const pass2 = fieldPassCheck.value;

  if (pass1 === pass2) {
    warning.classList.replace("d-block", "d-none");
  } else {
    warning.classList.replace("d-none", "d-block");
  }
}

fieldPass.addEventListener("input", checkPasswords);
fieldPassCheck.addEventListener("input", checkPasswords);
