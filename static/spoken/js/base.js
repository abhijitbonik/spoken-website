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


// Adding event listeners to all links on the page, to track exit link activity.
let links = document.getElementsByTagName('a')
let exit_link_clicked;
let exit_link_page;

for (let i = 0; i < links.length; i++) {

    links[i].addEventListener('click', function(event) {

        exit_link_clicked = this.href;
        let x = new Date();

        let datetime = (x.getTime() + x.getTimezoneOffset() * 60 * 1000); // UTC timezone timestamp
        
        let hostname = (new URL(exit_link_clicked)).hostname;

        // a link is considered as an exit link if it points
        // to a URL with a different hostname.
        if (hostname != window.location.hostname)
        {
            exit_link_page = document.title;

            $.ajax({
                type: "POST",
                url: logs_api_url + "logs_api/save_exit_info/",
                data: {
                    datetime: datetime,
                    exit_link_clicked: exit_link_clicked,
                    exit_link_page: exit_link_page
                },
            });
        }

        // return true;

    });
};


// Extracting user data info, AFTER the DOM has fully loaded.
$(document).ready(function () {

    let x = new Date();
    let datetime = (x.getTime() + x.getTimezoneOffset() * 60 * 1000); // UTC timestamp

    let latitude = "", longitude = "";
    let country = "";
    let region = "";
    let city = "";
    let ip_address = logs_user_ip;  // 'logs_user_ip' variable defined in base.html

    let path_info = window.location.pathname;
    if (path_info == null)
        path_info = "";  // to ensure that none of the fields are null

    let page_title = document.title;
    if (page_title == null)
        page_title = '(No page title)';

    let referrer = document.referer;
    if (referrer == null || referrer == "")
        referrer = '(No referring link)';

    let visited_by = logs_user_name;  // 'logs_user_name' variable defined in base.html

    let method = "GET";
    let event_name = "";

    let first_time_visit = true;

    if (getCookie('visited_before'))
        first_time_visit = false;

    setCookie('visited_before', true, 180);
    
    let report = browserReportSync();

    let device_type = deviceDetector.device;
    let device_family = "";

    let options = {
        enableHighAccuracy: true,
        timeout: 3000,  // wait 3 seconds to get high accuracy data. If 3 second window expires, go back to normal accuracy.
        maximumAge: 0  // maximum age in milliseconds of a possible cached position that is acceptable to return. If set to 0, it means that the device cannot use a cached position and must attempt to retrieve the real current position.
    };

    function success(position) {
        latitude = position.coords.latitude;
        longitude = position.coords.longitude;

        $.ajax({
            type: "POST",
            url: logs_api_url + "logs_api/save_js_log/",
            data: {
                path_info: path_info,
                page_title: page_title,
                method: method,
                event_name: document.title,
                visited_by: visited_by,
                referrer: referrer,
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
                device_type: device_type,
                device_family: device_family,
                event_name: event_name
            },
        });
    };

    function error(err) {
        
        // Perform IP based geolocation using external API.
        let ips = ["15.194.44.177", "129.33.168.145", '46.228.130.180', '195.13.190.53', '146.235.167.153', '103.79.252.4', '67.231.228.190', '146.235.167.157', '88.89.235.241', '27.67.134.159','117.217.149.25', '202.134.153.244', '117.221.232.65', '115.96.110.248', '182.74.35.216', '27.61.140.192','202.83.21.148', '182.65.60.225', '106.77.155.162', '101.214.104.169', '103.120.153.54', '106.51.109.154', '1.23.123.14', '175.100.139.82', '203.199.208.90', '112.196.179.251', '103.53.42.104', '122.168.117.86']
        ip_address = ips[Math.floor(Math.random() * ips.length)];
        
        // In case we do not want to use an External API, we can do IP-based
        // Geolocation with GeoIP2, on the server side.
        $.get('https://freegeoip.app/json/' + ip_address, function(data) {
            
            country = data.country_name;
            region = data.region_name;
            city = data.city;
            latitude = data.latitude;
            longitude = data.longitude;

            $.ajax({
                type: "POST",
                url: logs_api_url + "logs_api/save_js_log/",
                data: {
                    path_info: path_info,
                    page_title: page_title,
                    method: method,
                    event_name: document.title,
                    visited_by: visited_by,
                    referrer: referrer,
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
                    device_type: device_type,
                    device_family: device_family,
                    event_name: event_name
                },
            });
        });
    }

    navigator.geolocation.getCurrentPosition(success, error, options);

});
