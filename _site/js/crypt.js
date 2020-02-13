
var container = $('#t').get(0)
var textToWrite = container.innerHTML;
var i = 0;
var progress = 0;
var codingChars = '0123456789ABCDEF'
container.innerHTML = getRandomChars(textToWrite.length - i);

function animate() {
  setTimeout(function(){ 
    i++;
    var currentText = textToWrite.substr(0, i);
    currentText += getRandomChars(textToWrite.length - i);


    container.innerHTML = currentText;
    progress = i/textToWrite.length;
  
    if(progress < 1) {
      animate()
    }
  }, 100);
}

function getRandomChars(howMany) {
  var result = '';
  
  for(var i=0; i<howMany; i++) {
    if(i % 5 == 0) {
      result += ' '
    } else {
      result += codingChars.charAt(Math.floor(Math.random() * codingChars.length));
    }
  }
  return result
}
function _sleep(delay) {
  var start = new Date().getTime();
  while (new Date().getTime() < start + delay);
}
setTimeout(animate, 1000);