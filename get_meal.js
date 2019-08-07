var request = require('request');
var iconv = require('iconv-lite');
var charset = require('charset');


module.exports.getSchoolMeal = function (office, schoolcode, year, month, date) {
    var url = `http://localhost:10/?office_of_education=${office}&school_code=${schoolcode}&year=${year}&month=${month}&date=${date}`;
    request(url, (err, res, body)=> {
        console.log(url);
        console.log(body);
    })

}