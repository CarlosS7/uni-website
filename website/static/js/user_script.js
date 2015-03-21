var Admin = (function () {
    function postJSON(url, token, data, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xhr.setRequestHeader('X-CSRF-Token', token);
        xhr.onload = callback;
        xhr.send(JSON.stringify(data));
    }
    function empty(id) {
        document.getElementById(id).innerHTML = '';
    }
    function prepend(id, text) {
        var old = document.getElementById(id).innerHTML;
        document.getElementById(id).innerHTML = text + old;
    }
    function removeSignup() {
        document.getElementById('signup-info').innerHTML = this.responseText;
    }
    function clearSignup() {
        postJSON('/user/delsignup', csrftoken, '', removeSignup);
    }
    function showAddExaminee() {
        prepend('addexaminee-names', this.responseText);
    }
    function addExaminee() {
        var data = {};
        data.fullname = document.getElementById('addexaminee').value;
        data.name = document.getElementById('studentcode').value;
        data.getexam = document.getElementById('selectexam').value;
        if (document.getElementById('addexaminee-names').innerHTML) {
            data.button = true;
        }
        postJSON('/user/addexaminee', csrftoken, data, showAddExaminee);
    }
    function showGetScore() {
        prepend('getscore-scores', this.responseText);
    }
    function getExamScore() {
        var data = {};
        data.getscore = document.getElementById('getexamscore').value;
        if (document.getElementById('getscore-scores').innerHTML) {
            data.button = true;
        }
        postJSON('/user/examscore', csrftoken, data, showGetScore);
    }
    function showWrite() {
        document.getElementById('checkwrite').innerHTML = '';
        prepend('getexamscore', '<option>' + this.responseText + '</option>');
    }
    function sendWriteScore() {
        var form = document.getElementById('writescore-form'),
            data = {},
            i = 0,
            len = form.length;

        for (i; i < len; ++i) {
            var input = form[i];
            if (input.type === 'text') {
                data[input.name] = input.value;
            }
        }
        postJSON('/user/examwriting', csrftoken, data, showWrite);
    }

    return {
        empty: empty,
        clearSignup: clearSignup,
        addExaminee: addExaminee,
        getExamScore: getExamScore,
        sendWriteScore: sendWriteScore
    };
}());
