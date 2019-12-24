var request = require('request');
var iconv = require('iconv-lite');
var charset = require('charset');

module.exports.getSchoolMeal = function (office, schoolcode, year, month, date) {
    var token = "N7hF1WPya01sJFLBvPVZWPFoo0d7lqqeKaLqU2DnhOuiDSa15qS9K5XeAhzwlIPXJk2Y1TjeK5iWvVIf8VDMuGWu4vA8RL0TnChnkqFpFHa6JmzB2VFVI3iZddXme4Ll";
    var url = `http://localhost:10/?token=${token}&office_of_education=${office}&school_code=${schoolcode}&year=${year}&month=${month}&date=${date}`;
    request(url, (err, res, body)=> {
        console.log(url);
        console.log(body);
    })

}