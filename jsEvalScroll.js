let scrollInt = setInterval(() => {
  window.scrollBy(0, 1000);
}, 1000);

setTimeout(() => {
  clearInterval(scrollInt);
  document.querySelector('body').style.backgroundColor = 'blue';
}, 10000);
