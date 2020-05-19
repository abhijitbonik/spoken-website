$("#id_search_foss, #id_search_language").change(
    function() {
        var foss = $('#id_search_foss').val();
        var lang = $('#id_search_language').val();
        if ((foss == '' || lang == '') && ($(this).val() != '')){
            $.ajax(
                {
                    url: "/get-language/main/", 
                    type: "POST",
                    data: {
                        foss : foss,
                        lang : lang,
                    },
                    beforeSend: function() {
                        if(foss == '')
                            $('.ajax-refresh-search-foss').show();
                        if(lang == '')
                            $('.ajax-refresh-search-language').show();
                    },
                    success: function(data) {
                        if(data[0] == 'foss'){
                            $('#id_search_language').html(data[1]);
                        } else if(data[0] == 'lang'){
                            $('#id_search_foss').html(data[1]);
                        } else if(data[0] == 'reset') {
                            $('#id_search_language').html(data[1]);
                            $('#id_search_foss').html(data[2]);
                        }
                        if(foss == '')
                            $('.ajax-refresh-search-foss').hide();
                        if(lang == '')
                            $('.ajax-refresh-search-language').hide();
                    }
                }
            );
        }
    }
);
$("#id_search_otherfoss, #id_search_otherlanguage").change(
    function() {
        var foss = $('#id_search_otherfoss').val();
        var lang = $('#id_search_otherlanguage').val();
        if ((foss == '' || lang == '') && ($(this).val() != '')){
            $.ajax(
                {
                    url: "/get-language/series/",
                    type: "POST",
                    data: {
                        foss : foss,
                        lang : lang,
                    },
                    beforeSend: function() {
                        if(foss == '')
                            $('.ajax-refresh-search-otherfoss').show();
                        if(lang == '')
                            $('.ajax-refresh-search-otherlanguage').show();
                    },
                    success: function(data) {
                        if(data[0] == 'foss'){
                            $('#id_search_otherlanguage').html(data[1]);
                        } else if(data[0] == 'lang'){
                            $('#id_search_otherfoss').html(data[1]);
                        } else if(data[0] == 'reset') {
                            $('#id_search_otherlanguage').html(data[1]);
                            $('#id_search_otherfoss').html(data[2]);
                        }
                        if(foss == '')
                            $('.ajax-refresh-search-otherfoss').hide();
                        if(lang == '')
                            $('.ajax-refresh-search-otherlanguage').hide();
                    }
                }
            );
        }
    }
);
$("#id_search_archivedfoss, #id_search_archivedlanguage").change(
    function() {
        var foss = $('#id_search_archivedfoss').val();
        var lang = $('#id_search_archivedlanguage').val();
        if ((foss == '' || lang == '') && ($(this).val() != '')){
            $.ajax(
                {
                    url: "/get-language/archived/",
                    type: "POST",
                    data: {
                        foss : foss,
                        lang : lang,
                    },
                    beforeSend: function() {
                        if(foss == '')
                            $('.ajax-refresh-search-archivedfoss').show();
                        if(lang == '')
                            $('.ajax-refresh-search-archivedlanguage').show();
                    },
                    success: function(data) {
                        if(data[0] == 'foss'){
                            $('#id_search_archivedlanguage').html(data[1]);
                        } else if(data[0] == 'lang'){
                            $('#id_search_archivedfoss').html(data[1]);
                        } else if(data[0] == 'reset') {
                            $('#id_search_archivedlanguage').html(data[1]);
                            $('#id_search_archivedfoss').html(data[2]);
                        }
                        if(foss == '')
                            $('.ajax-refresh-search-archivedfoss').hide();
                        if(lang == '')
                            $('.ajax-refresh-search-archivedlanguage').hide();
                    }
                }
            );
        }
    }
);
$('.reset-filter').click(
    function(evt) {
        evt.preventDefault();
        $('#id_search_foss').val('');
        $('#id_search_language').val('');
        $.ajax(
            {
                url: "/get-language/main/",
                type: "POST",
                data: {
                    foss : '',
                    lang : '',
                },
                beforeSend: function() {
                    $('.ajax-refresh-search-foss').show();
                    $('.ajax-refresh-search-language').show();
                },
                success: function(data) {
                    if(data[0] == 'reset') {
                        $('#id_search_language').html(data[1]);
                        $('#id_search_foss').html(data[2]);
                        $('.ajax-refresh-search-foss').hide();
                        $('.ajax-refresh-search-language').hide();
                    }
                }
            }
        );
    }
);

(function(i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r;
    i[r] = i[r] || function(){
        (i[r].q = i[r].q || []).push(arguments)
    }, i[r].l = 1 * new Date();
    a = s.createElement(o), m = s.getElementsByTagName(o)[0];
    a.async = 1;
    a.src = g;
    m.parentNode.insertBefore(a,m)
})(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');
ga('create', 'UA-57761078-1', 'auto');
ga('send', 'pageview');

function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

var os = [
    { name: 'Windows Phone', value: 'Windows Phone', version: 'OS' },
    { name: 'Windows', value: 'Win', version: 'NT' },
    { name: 'iPhone', value: 'iPhone', version: 'OS' },
    { name: 'iPad', value: 'iPad', version: 'OS' },
    { name: 'Kindle', value: 'Silk', version: 'Silk' },
    { name: 'Android', value: 'Android', version: 'Android' },
    { name: 'PlayBook', value: 'PlayBook', version: 'OS' },
    { name: 'BlackBerry', value: 'BlackBerry', version: '/' },
    { name: 'Macintosh', value: 'Mac', version: 'OS X' },
    { name: 'Linux', value: 'Linux', version: 'rv' },
    { name: 'Palm', value: 'Palm', version: 'PalmOS' }
];

var browser = [
    { name: 'Chrome', value: 'Chrome', version: 'Chrome' },
    { name: 'Firefox', value: 'Firefox', version: 'Firefox' },
    { name: 'Safari', value: 'Safari', version: 'Version' },
    { name: 'Internet Explorer', value: 'MSIE', version: 'MSIE' },
    { name: 'Opera', value: 'Opera', version: 'Opera' },
    { name: 'BlackBerry', value: 'CLDC', version: 'CLDC' },
    { name: 'Mozilla', value: 'Mozilla', version: 'Mozilla' }
];

var header = [
    navigator.platform,
    navigator.userAgent,
    navigator.appVersion,
    navigator.vendor,
    window.opera
];

function matchItem(string, data) {
    var i = 0,
        j = 0,
        html = '',
        regex,
        regexv,
        match,
        matches,
        version;
    
    for (i = 0; i < data.length; i += 1) {
        regex = new RegExp(data[i].value, 'i');
        match = regex.test(string);
        if (match) {
            regexv = new RegExp(data[i].version + '[- /:;]([\d._]+)', 'i');
            matches = string.match(regexv);
            version = '';
            if (matches) { if (matches[1]) { matches = matches[1]; } }
            if (matches) {
                matches = matches.split(/[._]+/);
                for (j = 0; j < matches.length; j += 1) {
                    if (j === 0) {
                        version += matches[j] + '.';
                    } else {
                        version += matches[j];
                    }
                }
            } else {
                version = '0';
            }
            return {
                name: data[i].name,
                version: parseFloat(version)
            };
        }
    }
    return { name: 'unknown', version: 0 };
}

// extracting event log info, AFTER the page has fully loaded.
window.addEventListener('load', (event) => {

    start = event.timeStamp;  // move it from onload to somewhere else?

    let url_name = window.location.href;

    let agent = header.join(' ');
    let OS = matchItem(agent, os);
    let Browser = matchItem(agent, browser);
    
    let os_name = OS.name;
    let os_version = OS.version;

    let browser_name = Browser.name;
    let browser_version = Browser.version;

    let platform = navigator.platform;
    let vendor = navigator.vendor;

    let referer = document.referer;

    let visited_by = user;  // check base.html, the variable 'user' is defined there.

    // let method = "GET";

    let datetime = new Date().getTime();

    let first_time_visit = true;

    if (getCookie('visited_before'))
        first_time_visit = false;

    setCookie('visited_before', true, 180);

    // using geoplugin for IP details and geolocation 

    let ip_address = geoplugin_request();

    let country = geoplugin_countryName();
    let region = geoplugin_region();
    let city = geoplugin_city();
    let latitude = geoplugin_latitude();
    let longitude = geoplugin_longitude();

    // Alternatively, can use ipinfo
    // jQuery.get("http://ipinfo.io", function(response) {
    //     country = response.country
    //     region = response.region
    //     city = response.city
    // }, "jsonp");
    

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8001/logs_api/save_website_log/",
        data: {
            
            url_name: url_name,
            visited_by: visited_by,
            referer: referer,
            os_name: os_name,
            os_version: os_version,
            browser_name: browser_name,
            browser_version: browser_version,
            platform: platform,
            vendor: vendor,
            ip_address: ip_address,
            datetime: datetime,
            first_time_visit: first_time_visit,
            country: country,
            region: region,
            city: city,
            latitude: latitude,
            longitude: longitude,
        },
        success: function(response) {
            // the tutorial progress log was successfully saved. 
            console.log("Success");
        },
        error: function(xhr, status, err) {
            console.log(err);
        }
    });
});

window.addEventListener('unload', function(event) {

    // TODO: send this as AJAX request?
    var time = event.timeStamp - start;
    alert (time);

});