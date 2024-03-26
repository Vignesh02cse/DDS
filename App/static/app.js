const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener('click', () =>{
    container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener('click', () =>{
    container.classList.remove("sign-up-mode");
});
      // Include your JavaScript here
      document.querySelector('.sign-in-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form from submitting immediately

        var username = document.querySelector('.sign-in-form input[type="text"]').value;
        var password = document.querySelector('.sign-in-form input[type="password"]').value;

        if (!username || !password) {
            alert('Username and password are required.');
            return;
        }

        // If validation passes, submit the form
        this.submit();
      });
