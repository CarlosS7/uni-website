var Exam = (function () {
    var postJSON = function (url, token, data) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xhr.setRequestHeader('X-CSRF-Token', token);
        xhr.send(JSON.stringify(data));
    };
    var updateResults = function () {
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
        var token = document.getElementById('token').value;
        postJSON('/exam/update_results', token, data);
    };
    var counter = function () {
        var countdown = document.getElementById('countdown');
        var target_date = new Date().getTime() + 10800 * 1000;
        setInterval(function () {
            var current_date = new Date().getTime();
            var seconds_left = (target_date - current_date) / 1000;
            hours = parseInt(seconds_left / 3600);
            seconds_left = seconds_left % 3600;
            minutes = ('0' + parseInt(seconds_left / 60)).slice(-2);
            countdown.innerHTML = 'Time remaining: ' + hours + ':' + minutes;
        }, 1000 * 60);
    };
    var start = function () {
        var audio = document.getElementById('listening');
        var exam = document.getElementById('exam-body');
        var slide = document.querySelector('.slide');
        exam.style.display = 'block';
        slide.className = 'slide-up';
        counter();
        if (audio) {
            audio.play();
        }
        setInterval(function() {
            updateResults();
        }, 1000 * 60 * 5);
    };

    return {
        start: start
    };
})();
