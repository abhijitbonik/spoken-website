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


// Code related to user data logging from this point onwards.

// Function to set value of a cookie
function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}


// Function to get value of a cookie
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

let datetime, url_name, title, referer, visited_by, method, first_time_visit, ip_address;
let country, region, city, latitude, longitude, report, device_type;

// Extracting user data info, AFTER the DOM has fully loaded.
$(document).ready(function () {

    url_name = window.location.href;
    title = document.title;

    referer = document.referer;

    visited_by = user;  // check base.html, the variable 'user' is defined there.

    method = "GET";

    datetime = new Date().getTime();

    first_time_visit = true;

    if (getCookie('visited_before'))
        first_time_visit = false;

    setCookie('visited_before', true, 180);

    // using geoplugin for IP details and geolocation 

    ip_address = "";

    country = "";
    region = "";
    city = "";
    latitude = "";
    longitude = "";

    // Alternatively, can use ipinfo
    // jQuery.get("http://ipinfo.io", function(response) {
    //     // country = response.country
    //     // region = response.region
    //     // city = response.city
    //     console.log (response)
    // }, "jsonp");

    // fetch('http://www.geoplugin.net/json.gp').then(r=> r.json().then(j=> console.log(j)));
    
    report = browserReportSync();

    device_type = deviceDetector.device;

    $.get('https://freegeoip.app/json/', function(data) {

        ip_address = data.ip;
        country = data.country_name;
        region = data.region_name;
        city = data.city;
        latitude = data.latitude;
        longitude = data.longitude;
    });

    // $.ajax({
    //     type: "GET",
    //     url: "https://freegeoip.app/json/",
    //     success: function(response) {
    //         console.log(response.country_name);
    //     },
    // });

});

let unloaded = false;

$(window).on('beforeunload', function() {

    if (unloaded)
        return;
    unloaded = true;
 
    let visit_duration = Math.round((new Date().getTime() - datetime) / 1000);
    
    $.ajax({
        type: "POST",
        url: "http://192.168.100.6:8001/logs_api/save_js_log/",
        data: {
            url_name: url_name,
            title: title,
            method: method,
            event_name: document.title,
            visited_by: visited_by,
            referer: referer,
            os_family: report.os.name,
            os_version: report.os.version,
            browser_family: report.browser.name,
            browser_version: report.browser.version,
            ip_address: ip_address,
            datetime: datetime,
            first_time_visit: first_time_visit,
            country: country,
            region: region,
            city: city,
            latitude: latitude,
            longitude: longitude,
            visit_duration: visit_duration,
            device_type: device_type
        },
    });

    
});

window.addEventListener("visibilitychange", function(e)
{
    if (document.visibilityState == 'hidden')
    {
        if (device_type == 'desktop' || unloaded)
            return;
        unloaded = true;
        
        let visit_duration = Math.round((new Date().getTime() - datetime) / 1000);
        
        $.ajax({
            type: "POST",
            url: "http://192.168.100.6:8001/logs_api/save_js_log/",
            data: {
                url_name: url_name,
                title: title,
                method: method,
                event_name: document.title,
                visited_by: visited_by,
                referer: referer,
                os_family: report.os.name,
                os_version: report.os.version,
                browser_family: report.browser.name,
                browser_version: report.browser.version,
                ip_address: ip_address,
                datetime: datetime,
                first_time_visit: first_time_visit,
                country: country,
                region: region,
                city: city,
                latitude: latitude,
                longitude: longitude,
                visit_duration: visit_duration,
                device_type: device_type
            },
        });
    }
});