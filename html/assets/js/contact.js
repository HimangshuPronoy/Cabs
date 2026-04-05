/*
*
* Contact JS - Using Web3Forms
* @BufCanTaxi
*/
$(function() {
    // Get the form.
    var form = $('#ajax_contact');

    // Get the messages div.
    var formMessages = $('#form-messages');

    // Set up an event listener for the contact form.
    $(form).submit(function(event) {
        // Stop the browser from submitting the form.
        event.preventDefault();

        // Collect form data
        var formData = {
            firstname: $('#firstname').val(),
            lastname: $('#lastname').val(),
            email: $('#email').val(),
            phone: $('#phone').val(),
            message: $('#message').val(),
            to_name: "Buffalo Canada Taxi",
            to_email: "buffalocanadataxi@gmail.com"
        };

        // Send email via Web3Forms
        $.ajax({
            type: 'POST',
            url: 'https://api.web3forms.com/submit',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            headers: {
                'X-API-Key': '1ee30b3b-7ed6-44a4-87fb-6c7dfa35a919'
            }
        })
        .done(function(response) {
            // Make sure that the formMessages div has the 'success' class.
            $(formMessages).removeClass('alert-danger');
            $(formMessages).addClass('alert-success');

            // Set the message text.
            $(formMessages).html('✓ Thank you for your message! We\'ll get back to you soon.<br><br>You can also reach us directly at: <strong>+1 716-957-8900</strong> or <strong>buffalocanadataxi@gmail.com</strong>');

            // Clear the form.
            $('#firstname').val('');
            $('#lastname').val('');
            $('#email').val('');
            $('#phone').val('');
            $('#message').val('');

            // Scroll to message
            $('html, body').animate({
                scrollTop: $(formMessages).offset().top - 100
            }, 500);
        })
        .fail(function(data) {
            // Make sure that the formMessages div has the 'error' class.
            $(formMessages).removeClass('alert-success');
            $(formMessages).addClass('alert-danger');

            // Set the message text.
            $(formMessages).html('⚠ There was an issue sending your message. Please try again or contact us directly at <strong>+1 716-957-8900</strong>');
            
            // Scroll to message
            $('html, body').animate({
                scrollTop: $(formMessages).offset().top - 100
            }, 500);
        });
    });
});
			}
		});

	});

});
