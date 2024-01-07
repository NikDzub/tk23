let sv = document.querySelector('svg');

sv.addEventListener('click', () => {
  document.querySelector("div[class='cap']").toggleAttribute('class');
});
