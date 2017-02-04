function getTimeRemaining() {
  var seconds = Math.floor((t / 1000) % 60);
  var minutes = Math.floor((t / 1000 / 60) % 60);
  var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
  // var days = Math.floor(t / (1000 * 60 * 60 * 24));
  t = t - 1000;
  //console.log(seconds);
  return {
    'total': t,
    // 'days': days,
    'hours': hours,
    'minutes': minutes,
    'seconds': seconds
  };
}
var t;
function initializeClock(id) {
  var clock = document.getElementById(id);
  if(!clock) return;
  t = Date.parse(endtime) - Date.parse(now);
  // var daysSpan = clock.querySelector('.days');
  var hoursSpan = clock.querySelector('.hours');
  var minutesSpan = clock.querySelector('.minutes');
  var secondsSpan = clock.querySelector('.seconds');

  function updateClock() {
    var tx = getTimeRemaining();

    // daysSpan.innerHTML = tx.days;
    hoursSpan.innerHTML = ('0' + tx.hours).slice(-2);
    minutesSpan.innerHTML = ('0' + tx.minutes).slice(-2);
    secondsSpan.innerHTML = ('0' + tx.seconds).slice(-2);
    //console.log(tx);

    if (tx.total <= 0) {
      location.reload(); 
      clearInterval(timeinterval);
    }
  }

  if(t == 0){
      hoursSpan.innerHTML = '0';
      minutesSpan.innerHTML = '0';
      secondsSpan.innerHTML = '0';
    }else{
      updateClock();
      var timeinterval = setInterval(updateClock, 1000);
    }
}
initializeClock('clockdiv');