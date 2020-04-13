const {ipcRenderer} = require('electron');
const numLeds = 2700;

$(function(){
  let body = $('body');
  for(let i = 0; i < numLeds; i++){
    body.append('<div id="' + i + '" class="led"></div>');
    let led = $('#' + String(i));
    let value = 'translate(' + String(getRandomInt(0, window.innerWidth)) + 'px,'  + String(getRandomInt(0,window.innerHeight)) + 'px)';
    led.css({
      'transform': value,
    });
  }
});

ipcRenderer.on('msg', (e, msg) => {
  let decode = new TextDecoder().decode(msg);
  if(decode.startsWith('/init/')){
    let arg = decode.replace('/init/', '');
    init(arg);
  }
  else if(decode.startsWith('/video/')){
    let arg = decode.replace('/video/', '');
    video(arg);
  }
});

let getRandomInt = function(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;
}

let alloff = function(){
  let leds = $('.led');
  for(let i = 0; i < leds.length; i++){
    $('#' + String(i)).css({
      'background': '#191919',
    });
  }
}

let init = function(msg){
  if(msg == 'off'){
    console.log(msg);
    alloff();
  }
  else{
    let onLed = JSON.parse(msg);
    for(let i = 0; i < onLed.length; i++){
      $('#' + String(onLed[i])).css({
        'background': '#e5e5e5',
      });
    }
  }
}

let video = function(msg){
  if(msg == 'off'){
    console.log(msg);
    alloff();
  }
  else{
    let onLed = JSON.parse(msg);
    for(let i = 0; i < onLed.length; i += 2){
      let color = 'rgb(' + String(onLed[i+1][1]) + ',' + String(onLed[i+1][2]) + ',' + String(onLed[i+1][2]) + ')';
      $('#' + String(onLed[i])).css({
        'background': color,
      });
    }
  }
}