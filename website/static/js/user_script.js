var Admin = (function (mod) {
    function postJSON(url, token, data, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xhr.setRequestHeader('X-CSRF-Token', token);
        xhr.onload = callback;
        xhr.send(JSON.stringify(data));
    }
    function prepend(id, text) {
        old = document.getElementById(id).innerHTML;
        document.getElementById(id).innerHTML = text + old;
    }
    function removeSignup() {
        document.getElementById('signup-info').innerHTML = this.responseText;
    }
    function showAddExaminee() {
        prepend('addexaminee-names', this.responseText);
    }
    function showGetScore() {
        prepend('getscore-scores', this.responseText);
    }
    function showWrite() {
        document.getElementById('checkwrite').innerHTML = '';
        prepend('getexamscore', '<option>' + this.responseText + '</option>');
    }

    mod.empty = function (id) {
        document.getElementById(id).innerHTML = '';
    };
    mod.clearSignup = function () {
        postJSON('/user/delsignup', csrftoken, '', removeSignup);
    };
    mod.addExaminee = function () {
        var data = {};
        data['fullname'] = document.getElementById('addexaminee').value;
        data['name'] = document.getElementById('studentcode').value;
        data['getexam'] = document.getElementById('selectexam').value;
        if (document.getElementById('addexaminee-names').innerHTML) {
            data['button'] = true;
        }
        postJSON('/user/addexaminee', csrftoken, data, showAddExaminee);
    };
    mod.getExamScore = function () {
        var data = {};
        data['getscore'] = document.getElementById('getexamscore').value;
        if (document.getElementById('getscore-scores').innerHTML) {
            data['button'] = true;
        }
        postJSON('/user/examscore', csrftoken, data, showGetScore);
    };
    mod.sendWriteScore = function () {
        var form = document.getElementById('writescore-form');
        var data = {};
        for (var i = 0, ii = form.length; i < ii; i++) {
            var input = form[i];
            if (input.type === 'text') {
                data[input.name] = input.value;
            }
        }
        postJSON('/user/examwriting', csrftoken, data, showWrite);
    };

    return mod;
})({});
