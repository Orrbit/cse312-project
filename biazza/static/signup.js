$(document).ready(function () {

    // check password length and everything

    var $password = $(".form-control[type='password']");
    var $passwordAlert = $(".password-alert");
    var $requirements = $(".requirements");
    var leng, bigLetter, num, specialChar;
    var $leng = $(".leng");
    var $bigLetter = $(".big-letter");
    var $num = $(".num");
    var $specialChar = $(".special-char");
    var specialChars = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~";
    var numbers = "0123456789";

    $requirements.addClass("wrong");
    $password.on("focus", function(){$passwordAlert.show();});

    $password.on("input blur", function (e) {
        var el = $(this);
        var val = el.val();
        $passwordAlert.show();

        if (val.length < 8) {
            leng = false;
        }
        else if (val.length > 7) {
            leng=true;
        }
        

        if(val.toLowerCase()==val){
            bigLetter = false;
        }
        else{bigLetter=true;}
        
        num = false;
        for(var i=0; i<val.length;i++){
            for(var j=0; j<numbers.length; j++){
                if(val[i]==numbers[j]){
                    num = true;
                }
            }
        }
        
        specialChar=false;
        for(var i=0; i<val.length;i++){
            for(var j=0; j<specialChars.length; j++){
                if(val[i]==specialChars[j]){
                    specialChar = true;
                }
            }
        }

        // console.log(leng, bigLetter, num, specialChar);
        
        if(leng==true&&bigLetter==true&&num==true&&specialChar==true){
            $(this).addClass("valid").removeClass("invalid");
            $requirements.removeClass("wrong").addClass("good");
            $passwordAlert.removeClass("alert-warning").addClass("alert-success");

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
                        console.log(data);
        
                        // check what kind of error is it. 
                        if(data == "email_found"){
        
                            console.log("EMAIL FOUND!!")
        
                            const msgElem = $('#usrMsg');
                            msgElem.text("Email has already been registered. Please use a different email address");
                            msgElem.css("color", "red");

                            document.getElementById("passwordInput").value = "";
        
                            // window.location.pathname = "/home/messages";
        
                        }else if(data == "Success"){
        
                            console.log("EMAIL NOT FOUND!!")
        
                            window.location.pathname = "/home";
        
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

        }
        else
        {
            $(this).addClass("invalid").removeClass("valid");
            $passwordAlert.removeClass("alert-success").addClass("alert-warning");

            if(leng==false){$leng.addClass("wrong").removeClass("good");}
            else{$leng.addClass("good").removeClass("wrong");}

            if(bigLetter==false){$bigLetter.addClass("wrong").removeClass("good");}
            else{$bigLetter.addClass("good").removeClass("wrong");}

            if(num==false){$num.addClass("wrong").removeClass("good");}
            else{$num.addClass("good").removeClass("wrong");}

            if(specialChar==false){$specialChar.addClass("wrong").removeClass("good");}
            else{$specialChar.addClass("good").removeClass("wrong");}
        }
        
        
        if(e.type == "blur"){
                $passwordAlert.hide();
            }
    });
});