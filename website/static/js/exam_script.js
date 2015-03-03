function startExam() {
    var audio = document.getElementById('listening');

    document.getElementById('exam-body').style.display = 'block';
    document.querySelector('.slide').className = 'slide-up';
    if (audio) {
        audio.play();
    }
    setInterval(function() {
        updateResults();
    }, 1000 * 60 * 1);
}

function updateResults() {
    var form = document.forms[0];
    var data = {};

    for (var i = 0, ii = form.length; i < ii; i++) {
        var input = form[i];
        if (input.type === 'radio' && input.checked) {
            data[input.name] = input.value;
        }
        if (input.type === 'textarea') {
            data[input.name] = input.value;
        }
    }

    var xhr = new XMLHttpRequest();
    var token = document.getElementById('token').value;

    xhr.open('POST', '/exam/update_results', true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.setRequestHeader('X-CSRF-Token', token);
    xhr.send(JSON.stringify(data));
}
