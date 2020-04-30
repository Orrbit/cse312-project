$(document).ready(function () {
    $('#loginForm').submit(function () {

        console.log("??????");
    
        const email = $('#emailInput').val();
        const password = $('#passwordInput').val();
    
        const requestData = {'email': email, 'password': password};
    
        $.ajax({
            type: "POST",
            url: "",
            cache: false,
            data: requestData,
            success: data => {
                console.log(data);
    
                // check what kind of error is it. 
                if(data == "email_not_found"){
    
                    console.log("EMAIL FOUND!!")
    
                    const msgElem = $('#usrMsg');
                    msgElem.text("Email has not been registered. Please register the email address");
                    msgElem.css("color", "red");
    
                    document.getElementById("passwordInput").value = "";
    
                    // window.location.pathname = "/home/messages";
    
                }else if(data == "Success"){
    
                    console.log("EMAIL NOT FOUND!!")
    
                    window.location.pathname = "/home";
    
                }else if(data == "invalid_password"){

                    console.log("Invalid Password");

                    const msgElem = $('#usrMsg');
                    msgElem.text("Invalid Password");
                    msgElem.css("color", "red");
    
                    document.getElementById("passwordInput").value = "";
                }
    
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