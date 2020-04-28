
$(document).ready(function () {
    $('#signupForm').submit(function () {
        const email = $('#emailInput').val();
        const firstName = $('#firstNameInput').val();
        const lastName = $('#lastNameInput').val();
        const password = $('#passwordInput').val();

        const requestData = {'email': email, 'firstName': firstName, 'lastName': lastName, 'password': password};

        $.ajax({
            type: "POST",
            url: "/signup",
            cache: false,
            data: requestData,
            success: data => {
                console.log("Success!");
                window.location.pathname = "/home";
                // Will most likely reroute the user to the home page
            },
            error: (jqXHR, textStatus, errorThrown) => {
                const message = jqXHR.responseJSON['message'];
                const msgElem = $('#usrMsg');
                msgElem.text(message);
                msgElem.css("color", "red");
                // Response should be of the form {'message': <message>}
                // Message will be the reason why the signup request failed.
            }
        });


        return false;
    });
});