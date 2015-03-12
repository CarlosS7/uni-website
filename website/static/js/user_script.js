var Admin = (function () {
    var postJSON = function (url, token, data, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xhr.setRequestHeader('X-CSRF-Token', token);
        xhr.onload = callback;
        xhr.send(JSON.stringify(data));
    };
    var empty = function (id) {
        document.getElementById(id).innerHTML = '';
    };
    var prepend = function (id, text) {
        old = document.getElementById(id).innerHTML;
        document.getElementById(id).innerHTML = text + old;
    };
    var clearSignup = function () {
        document.getElementById('signup-info').innerHTML = '<p>No students to contact.</p>'
    };
    var showAddExaminee = function () {
        prepend('addexaminee-names', this.responseText);
    };
    var addExaminee = function () {
        var token = document.getElementById('examinee-token').value;
        var data = {};
        data['fullname'] = document.getElementById('addexaminee').value;
        data['name'] = document.getElementById('studentcode').value;
        data['getexam'] = document.getElementById('selectexam').value;
        if (document.getElementById('addexaminee-names').innerHTML) {
            data['button'] = true;
        }
        postJSON('/user/addexaminee', token, data, showAddExaminee);
    };
    var showGetScore = function () {
        prepend('getscore-scores', this.responseText);
    };
    var getExamScore = function () {
        var token = document.getElementById('score-token').value;
        var data = {};

        data['getscore'] = document.getElementById('getexamscore').value;
        if (document.getElementById('getscore-scores').innerHTML) {
            data['button'] = true;
        }
        postJSON('/user/examscore', token, data, showGetScore);
    };
    var showWrite = function () {
        document.getElementById('checkwrite').innerHTML = '';
        prepend('getexamscore', '<option>' + this.responseText + '</option>');
    };
    var sendWriteScore = function () {
        var form = document.getElementById('writescore-form');
        var token = document.getElementById('write-token').value;
        var data = {};

        for (var i = 0, ii = form.length; i < ii; i++) {
            var input = form[i];
            if (input.type === 'text') {
                data[input.name] = input.value;
            }
        }
        postJSON('/user/examwriting', token, data, showWrite);
    };
    return {
        empty: empty,
        clearSignup: clearSignup,
        addExaminee: addExaminee,
        getExamScore: getExamScore,
        sendWriteScore: sendWriteScore
    };
})();
