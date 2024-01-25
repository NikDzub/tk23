let sv = document.querySelector('.gftimg'); //svg
let ht = document.querySelector('body');
let cap = document.querySelector('#cap');

sv.addEventListener('click', () => {
  document.querySelector("div[class='hide']").toggleAttribute('class');
  // sv.style.filter = 'brightness(0.5)';
  // ht.style.filter = 'brightness(0.5)';
});
