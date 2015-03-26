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
        document.getElementById(id).className = 'quickslide';
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
        var el = document.getElementById('check-write-btn');
        toggleDiv('writing-score');
        el.style.display = 'none';
    }
    function updateGetScore() {
        var text = document.getElementById('getexamscore').innerHTML;
        if (text.indexOf(this.responseText) === -1)
            prepend('getexamscore', '<option>' + this.responseText + '</option>');
    }
    function sendWriteScore(formId) {
        var form = document.getElementById(formId),
            data = {},
            i = 0,
            len = form.length;

        for (i; i < len; ++i) {
            var input = form[i];
            if (input.type === 'text') {
                data[input.name] = input.value;
            }
        }
        postJSON('/user/examwriting', csrftoken, data, updateGetScore);
        document.getElementById(formId).className = 'quickslide';
    }

    return {
        empty: empty,
        clearSignup: clearSignup,
        addExaminee: addExaminee,
        getExamScore: getExamScore,
        showWrite: showWrite,
        sendWriteScore: sendWriteScore
    };
}());
