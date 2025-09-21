/** TO DISABLE SCREEN CAPTURE **/
document.addEventListener('keyup', (e) => {
    if (e.key == 'PrintScreen') {
        navigator.clipboard.writeText('');
        alert('Screenshots disabled!');
    }
});

/** TO DISABLE PRINTS WHIT CTRL+P **/
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key == 'p') {
        alert('This section is not allowed to print or export to PDF');
        e.cancelBubble = true;
        e.preventDefault();
        e.stopImmediatePropagation();
    }
});

/** TO DISABLE PRINTS WHIT CTRL+SHIFT+I **/
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key == 'I') {
        alert('This section is not allowed to print or export to PDF');
        e.cancelBubble = true;
        e.preventDefault();
        e.stopImmediatePropagation();
    }
}
);

/** TO DISABLE PRINTS WHIT CTRL+SHIFT+J **/
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key == 'J') {
        alert('This section is not allowed to print or export to PDF');
        e.cancelBubble = true;
        e.preventDefault();
        e.stopImmediatePropagation();
    }
}
);

/** TO DISABLE PRINTS WHIT win+SHIFT+s **/
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key == 'S') {
        alert('This section is not allowed to print or export to PDF');
        e.cancelBubble = true;
        e.preventDefault();
        e.stopImmediatePropagation();
    }
}
);

/** TO DISABLE PRINTS WHIT CTRL+SHIFT+C **/
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key == 'C') {
        alert('This section is not allowed to print or export to PDF');
        e.cancelBubble = true;
        e.preventDefault();
        e.stopImmediatePropagation();
    }
}
);

document.addEventListener("contextmenu", function(event) {
    event.preventDefault();
  });


  document.addEventListener('keydown', function(event) {
    if ((event.key === "S" || event.key === "s") && event.shiftKey && event.metaKey) {
        event.preventDefault();
        alert("Screenshots using this shortcut are not allowed on this page.");
        // You can perform other actions here to handle the attempted screenshot.
    }
});

