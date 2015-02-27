// show quotes on startup

var quotes = [
{q: 'I am very thankful to have taken this course -- it gave me a solid base from which to teach.', a: 'Alison, TESOL Certificate' },
{q: 'I learned a lot and now feel ready to study a university course in English.', a:'Seng, IEP Advanced'},
{q:'I study English in class and it is very interesting. Now I learn many things such as writing, speaking and listening skills. I really enjoy to meet friends and study here.', a:'Souaney, IEP Intermediate'},
{q:'This class helped my English get better and I meet new people. I really like this class because it is fun and makes me improve my English.', a:'Sal Lao Khay Sue, IEP Intermediate'},
{q:'My TESOL training has given me invaluable resources for working with my students. I\'m continuously pulling from things I learned in my training to find the most effective teaching technique with each particular student.', a:'Katie, TESOL Certificate'}
];

$(document).ready(function() {
    randQuotes(quotes);
    fadeQuotes('#randomquote, #author', quotes, 5000);
});

function randQuotes(quotes) {
    var i = Math.floor(Math.random()*quotes.length);
    $('#randomquote').text(quotes[i].q);
    $('#author').text(quotes[i].a);
}

function fadeQuotes(divID, quotes, interval) {
    setInterval(function() {
        $(divID).fadeOut('slow', function() {
            randQuotes(quotes);
            $(this).fadeIn('slow');
        });
    }, interval);
}

function toggleDiv(showHideDiv) {
    var el = document.getElementById(showHideDiv);
    if(el.style.display == "block") {
        el.style.display = "none";
        el.style.visibility = "hidden";
    }
    else {
        el.style.display = "block";
        el.style.visibility = "visible";
    }
} 
