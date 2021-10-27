// Invoke Functions Call on Document Loaded
//document.addEventListener('DOMContentLoaded', () =>{
  //hljs.highlightAll();
//});

var alertWrapper = document.querySelector(".alert")
var alertClose = document.querySelector(".alert__close")
if (alertWrapper) {
  alertClose.addEventListener('click', () =>
    alertWrapper.style.display = 'none'
  )
}