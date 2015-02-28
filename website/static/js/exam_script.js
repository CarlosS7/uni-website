function startExam() {
    document.getElementById('exam-body').style.display = 'block';
    document.getElementById('top-panel').style.display = 'none';
    document.getElementById('listening').play();
    setInterval(function() {
      ajax.post('/exam/update_results', $('form').serializeArray()); // find alternative for serialize
    }, 1000 * 60 * 5);
}
