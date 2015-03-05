function postJSON(url, token, data) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.setRequestHeader('X-CSRF-Token', token);
    xhr.send(JSON.stringify(data));
    xhr.onload = displayExaminee;
}

function displayExaminee(data) {
    var output = document.getElementById('addexaminee-results');
    output.innerHTML = '<h4>Name: ' + data.name +
        'Student Id: ' + data.code +
        'Password: ' + data.password + '</h4>';
}

function addExaminee() {
    var fullname = document.getElementById('addexaminee');
    var code = document.getElementById('studentcode');
    var exams = document.getElementById('selectexam');
    var token = document.getElementById('examinee-token').value;
    var data = {};

    data['fullname'] = fullname.value;
    data['name'] = code.value;
    data['getexam'] = exams.selectedIndex.value;
    postJSON('/user/addexaminee', token, data);
}

function getExamScore() {
    var exams = document.getElementById('getexamscore');
    var token = document.getElementById('score-token').value;
    var data = {};

    data['getscore'] = exams.selectedIndex.value;
    postJSON('/user/examscore', token, data);
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

    postJSON('/user/examwriting', token, data);
}
