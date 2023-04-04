// get elements
const btnToggler = document.querySelector('.nav-toggle-btn');
const navListEle = document.querySelector('.nav-lists');

// Responsive navbar
btnToggler.addEventListener('click', function() {
    navListEle.classList.toggle('show-nav-lists');
})