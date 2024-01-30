document.body.style.backgroundColor = 'yellow';

let int = setInterval(() => {
  try {
    document
      .querySelectorAll('div[class*="DivCommentItemContainer"]')
      .forEach((e) => {
        e.scrollIntoView();
        if (
          e.innerHTML.includes('hey thats great!') ||
          e.innerHTML.includes('check this out!') ||
          e.innerHTML.includes('im on my way!') ||
          e.innerHTML.includes('this is so crazy i cant') ||
          e.innerHTML.includes('wow thats so cool haha')
        ) {
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
