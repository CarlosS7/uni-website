function postJSON(url, token, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.setRequestHeader('X-CSRF-Token', token);
    xhr.onload = callback;
    xhr.send(JSON.stringify(data));
}

function showAddexaminee() {
    var output = document.getElementById('addexaminee-results');
    var data = this.responseText;
    output.innerHTML += data;
}

function addExaminee() {
    var fullname = document.getElementById('addexaminee');
    var code = document.getElementById('studentcode');
    var exams = document.getElementById('selectexam');
    var token = document.getElementById('examinee-token').value;
    var data = {};

    data['fullname'] = fullname.value;
    data['name'] = code.value;
    data['getexam'] = exams.value;
    postJSON('/user/addexaminee', token, data, showAddexaminee);
}

function showGetscore() {
    var output = document.getElementById('getscore-results');
    var data = this.responseText;
    output.innerHTML += data;
}

function getExamScore() {
    var exams = document.getElementById('getexamscore');
    var token = document.getElementById('score-token').value;
    var data = {};

    data['getscore'] = exams.value;
    postJSON('/user/examscore', token, data, showGetscore);
}

function showWrite() {
    var output = document.getElementById('checkwrite');
    output.innerHTML = '';
}

function sendWriteScore() {
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
}
