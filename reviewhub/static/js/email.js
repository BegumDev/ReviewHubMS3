let contactForm = document.querySelector('.email-form');
let emailMsg = document.querySelector('.email-msg')
let clearForm = document.querySelector('.email-form')


function emailSent() {
    emailMsg.innerHTML = "Thanks! Your email has been sent."
}

function emailNotSent() {
    emailMsg.innerHTML = "Sorry! That didn't quite work. Please try again."
}


function sendMail(contactForm) {
    emailjs.send('gmail', 'Test email', {
        'from_name':contactForm.name.value,
        'from_email':contactForm.email.value,
        'project_request':contactForm.message.value,
    })
    .then(
        function(response) {
            console.log('Success', response);
            console.log("email sent");
            emailSent();
            clearForm.reset();
        },
        function (error){
            console.log("email has not sent")
            emailNotSent();
        }
    );
    return false;
}