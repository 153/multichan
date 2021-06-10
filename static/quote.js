function quote(postnumber) {
    var text = '>>'+postnumber+'\n';
    var textarea = document.getElementById("reply");
    textarea.value += text;
}    
