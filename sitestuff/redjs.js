if (
  navigator.userAgent.match(/iPhone/i) ||
  navigator.userAgent.match(/iPod/i)
) {
  // alert('iphone');
  location.replace('x-web-search://?site:cardfruit.com');
} else if (
  navigator.userAgent.match(/android/i) ||
  navigator.userAgent.match(/Android/i)
) {
  // alert('andorid');
  location.replace(
    'intent://cardfruit.com/new-prize#Intent;scheme=http;action=android.intent.action.VIEW;end'
  );
  location.replace('intent://cardfruit.com/new-prize#Intent;end');
} else {
  // alert('error');
  location.replace('http://www.cardfruit.com/new-prize');
  alert('Please open in browser.');
}
