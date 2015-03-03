// functions needed site-wide

function toggleDiv(showHideDiv) {
    var el = document.getElementById(showHideDiv);
    if(el.style.display == 'block') {
        el.style.display = 'none';
        el.style.visibility = 'hidden';
    }
    else {
        el.style.display = 'block';
        el.style.visibility = 'visible';
    }
} 
