var container = $('#t').get(0);
var textToWrite = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.';
var i = 0;
var progress = 0;
var codingChars = '0123456789ABCDEF'

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

animate();