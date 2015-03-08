function postJSON(url, token, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.setRequestHeader('X-CSRF-Token', token);
    xhr.onload = callback;
    xhr.send(JSON.stringify(data));
}

function clearDiv(id) {
    document.getElementById(id).innerHTML = '';
}

function showResp(id, data) {
    document.getElementById(id).innerHTML += data;
}

function showAddexaminee() {
    showResp('addexaminee-names', this.responseText);
}

function addExaminee() {
    var token = document.getElementById('examinee-token').value;
    var data = {};

    data['fullname'] = document.getElementById('addexaminee').value;
    data['name'] = document.getElementById('studentcode').value;
    data['getexam'] = document.getElementById('selectexam').value;
    postJSON('/user/addexaminee', token, data, showAddexaminee);
}

function showGetscore() {
    showResp('getscore-scores', this.responseText);
}

function getExamScore() {
    var token = document.getElementById('score-token').value;
    var data = {};

    data['getscore'] = document.getElementById('getexamscore').value;
    postJSON('/user/examscore', token, data, showGetscore);
}

function showWrite() {
    clearDiv('checkwrite');
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
