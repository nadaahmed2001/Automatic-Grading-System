var selectedWords = [];

document.getElementById("inputText").addEventListener("mouseup", function() {
  var input = this;
  var selectionStart = input.selectionStart;
  var selectionEnd = input.selectionEnd;
  var selectedWord = input.value.substring(selectionStart, selectionEnd).trim();
  if (selectedWord !== "") {
    selectedWords.push(selectedWord);
    displaySelectedWords();
  }
});

function displaySelectedWords() {
  var selectedWordsElement = document.getElementById("selectedWords");
  selectedWordsElement.innerHTML = ""; // Clear previous selection

  selectedWords.forEach(function(word) {
    var wordContainer = document.createElement("div");
    wordContainer.className = "word-container";

    var wordText = document.createElement("span");
    wordText.textContent = word;
    wordContainer.appendChild(wordText);

    var deleteButton = document.createElement("button");
    deleteButton.textContent = "x";
    deleteButton.className = "delete-button";
    deleteButton.addEventListener("click", function() {
      deleteWord(word);
    });
    wordContainer.appendChild(deleteButton);

    selectedWordsElement.appendChild(wordContainer);
  });
}

function deleteWord(word) {
  var index = selectedWords.indexOf(word);
  if (index !== -1) {
    selectedWords.splice(index, 1);
    displaySelectedWords();
  }
}


document.getElementById("inputText").addEventListener("input", updateSize);
document.getElementById("inputText").addEventListener("change", updateSize);

function updateSize() {
  var input = this;
  var valueLength = input.value.length;
  var placeholderLength = input.placeholder.length;
  var maxLength = Math.max(valueLength, placeholderLength);
  input.size = maxLength + 2;
}
