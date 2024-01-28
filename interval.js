document.body.style.backgroundColor = 'yellow';

let int = setInterval(() => {
  try {
    document
      .querySelectorAll('div[class*="DivCommentItemContainer"]')
      .forEach((e) => {
        e.scrollIntoView();
        if (e.innerHTML.includes('CARDFRUIT')) {
          clearInterval(int);
          e.setAttribute('class', 'target');
          e.style.backgroundColor = 'blue';
          e.querySelector('div[class*=DivLikeWrapper]').setAttribute(
            'class',
            'heart_box'
          );
        } else {
          e.setAttribute('class', 'pass');
          window.scrollBy(0, 10);
          window.scrollBy(0, -20);
          e.remove();
        }
      });
  } catch (error) {
    print(error);
  }
}, 1000);

setTimeout(() => {
  document.body.style.backgroundColor = 'red';

  clearInterval(int);
}, 60000);
