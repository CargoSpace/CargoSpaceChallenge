function getActiveTimeRemaining() {
  var seconds = Math.floor((tactive / 1000) % 60);
  var minutes = Math.floor((tactive / 1000 / 60) % 60);
  var hours = Math.floor((tactive / (1000 * 60 * 60)) % 24);
  // var days = Math.floor(tactive / (1000 * 60 * 60 * 24));
  tactive = tactive - 1000;
  //console.log(seconds);
  return {
    'total': tactive,
    // 'days': days,
    'hours': hours,
    'minutes': minutes,
    'seconds': seconds
  };
}
var tactive;
function initializeActiveClock(id) {
  var clock = document.getElementById(id);
  if(!clock) return;
  tactive = Math.abs(Date.parse(activeEndtime.replace('-','/').replace('-','/')) - Date.parse(activeNow.replace('-','/').replace('-','/')));
  // var daysSpan = clock.querySelector('.days');
  var hoursSpan = clock.querySelector('.hours');
  var minutesSpan = clock.querySelector('.minutes');
  var secondsSpan = clock.querySelector('.seconds');

  function updateClock() {
    var tx = getActiveTimeRemaining();

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

  if(tactive == 0){
      hoursSpan.innerHTML = '0';
      minutesSpan.innerHTML = '0';
      secondsSpan.innerHTML = '0';
    }else{
      updateClock();
      var timeinterval = setInterval(updateClock, 1000);
    }
}
initializeActiveClock('activeClockdiv');