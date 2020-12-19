function quote(postnumber) {
    var text = '\n>>'+postnumber+'\n';
    var textarea = document.getElementById("reply");
    textarea.value += text;
}    
