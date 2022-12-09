/* --- Autocomplete ---
* Step 1: Read a list from text file
* Step 2: Use user input to get e.g. three nearest neighbors (without accents)
* Step 3: Display three nearest neighbors and replace current word upon click
*/

// TODO Read list from text file
var wordlist = ['comorens', 'comensnsddd', 'Cómerase', 'Cómo', 'comen', 'come']
// wordlist_t = ['como', 'comen', 'comer', 'come']
console.log(wordlist)

var word1 = document.getElementById('word1')
var word2 = document.getElementById('word2')
var word3 = document.getElementById('word3')

function normalizeWord(word) {
    var normalized = word.toLowerCase()
    normalized = normalized.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    return normalized
}

function findMostSimilar(word, listOfWords) {
    // Find words that start with same characters
    var similars = []
    listOfWords.forEach(w => {
        var w_normalized = normalizeWord(w)
        if (w_normalized.startsWith(word)) {
            similars.push(w)
        }
    })

    // Sort list of similar words according to word length,
    // then return three shortest ones
    similars.sort((a, b) => a.length - b.length)
    return similars.slice(0, 3)
}

function resetWordSuggestions(words) {
    words.forEach(w => {
        w.value = ''
        w.style.cursor = 'text'
    })
}

function setSuggestionValue(word, similarWords, idx) {
    if (similarWords.length >= idx + 1) {
        word.style.cursor = 'pointer'
        word.value = similarWords[idx]
    } else {
        word.value = ''
        word.style.cursor = 'text'
    }
}

// Get user input (from last space)
var message_area = document.getElementById('msg_id')
var wordSuggestions = [word1, word2, word3]

// Functionality to replace current word with selected one upon click
wordSuggestions.forEach(w => {
    w.addEventListener('click', () => {
        if (w.value.length > 0) {
            var currentinput = message_area.value.split(' ')
            currentinput = currentinput.slice(0, currentinput.length - 1).join(' ')
            if (currentinput.length > 0) {
                currentinput = currentinput + ' '
            }
            message_area.value = currentinput + w.value + ' '
            message_area.focus()
            resetWordSuggestions(wordSuggestions)
        } else {
            message_area.focus()
        }
    })
})

message_area.addEventListener('keyup', () => {
    // Get current word
    var currentInput = message_area.value.split(' ')
    var currentWord = currentInput[currentInput.length - 1]

    // Make lower caps
    currentWord = normalizeWord(currentWord)

    var threeMostSimilar = []
    if (currentWord.length > 0) {
        // Check for most similar words (create descending order but crop dissimilar ones)
        threeMostSimilar = findMostSimilar(currentWord, wordlist)
    }

    // Display three (or more/ less) words to select from
    setSuggestionValue(word1, threeMostSimilar, 0)
    setSuggestionValue(word2, threeMostSimilar, 1)
    setSuggestionValue(word3, threeMostSimilar, 2)
})

// TODO: Problem: what about lower/ upper case?