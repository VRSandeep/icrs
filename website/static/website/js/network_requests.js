// Redirect function
function Redirect(url) {
    var ua = navigator.userAgent.toLowerCase(),
        isIE = ua.indexOf('msie') !== -1,
        version = parseInt(ua.substr(4, 2), 10);
    // Internet Explorer 8 and lower
    if (isIE && version < 9) {
        var link = document.createElement('a');
        link.href = url;
        document.body.appendChild(link);
        link.click();
    }
    // All other browsers
    else {
        window.location.href = url;
    }
}
// Get cookie function from w3 schools
function getCookie(cname) {
    var name = cname + '=';
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return '';
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

window.local_url = document.location.origin;


$(window).load(function() {
    var csrftoken = getCookie('csrftoken');
    // var token_auth = localStorage.getItem('Token');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // if (token_auth) {
                //     xhr.setRequestHeader('Authorization', token_auth);
                // }
                if (!csrfSafeMethod(settings.type))
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                if (csrftoken) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        }
    });
});

$('#logout').click(function() {
    // e.preventDefault();
    $.ajax({
        type: 'GET',
        url: window.local_url + '/accounts/logout/',
        xhrFields: {
            withCredentials: true
        },
        success: function(response) {
            location.reload();
        },
        error: function(xhr, ajaxOptions, thrownError) {
            console.log('Could not logout');
        },
    });
});

$('#rlogin_form').submit(function(e) {

    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: window.local_url + $(this).attr('action'),
        data: $(this).serialize(),
        xhrFields: {
            withCredentials: true
        },
        success: function(response) {
            console.log('success');
            // location.reload();
            Redirect('/interviewer/');
        },
        error: function(xhr, ajaxOptions, thrownError) {
            // lolz
            alert('Invalid username or password');
        },
    });
});

$('#cregister_form').submit(function(e) {

    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: window.local_url + $(this).attr('action'),
        data: $(this).serialize(),
        xhrFields: {
            withCredentials: true
        },
        success: function(response) {
            console.log('success');
            // location.reload();
            Redirect('/candidate/');
        },
        error: function(xhr, ajaxOptions, thrownError) {
            // lolz
            alert('Incorrect Input. Please check if the input entered is correct; If everything is fine, then username is taken :(');
        },
    });
});
