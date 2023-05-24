// Importing necessary assets
import bot from './assets/bot.svg'
import user from './assets/user.svg'

// Selecting DOM elements
const form = document.querySelector('form')
const chatContainer = document.querySelector('#chat_container')

let loadInterval

// Function to display a loading indicator
function loader(element) {
    element.textContent = ''

    // Update the loading indicator text every 300 milliseconds
    loadInterval = setInterval(() => {
        element.textContent += '.';

        // Reset the loading indicator if it reaches three dots
        if (element.textContent === '....') {
            element.textContent = '';
        }
    }, 300);
}

// Function to type text gradually
function typeText(element, text) {
    let index = 0

    // Add a character from the text to the element every 20 milliseconds
    let interval = setInterval(() => {
        if (index < text.length) {
            element.innerHTML += text.charAt(index)
            index++
        } else {
            clearInterval(interval)
        }
    }, 20)
}

// Generate a unique ID for each message div of the bot
function generateUniqueId() {
    const timestamp = Date.now();
    const randomNumber = Math.random();
    const hexadecimalString = randomNumber.toString(16);

    return `id-${timestamp}-${hexadecimalString}`;
}

// Create a chat stripe HTML markup
function chatStripe(isAi, value, uniqueId) {
    return (
        `
        <div class="wrapper ${isAi && 'ai'}">
            <div class="chat">
                <div class="profile">
                    <img 
                      src=${isAi ? bot : user} 
                      alt="${isAi ? 'bot' : 'user'}" 
                    />
                </div>
                <div class="message" id=${uniqueId}>${value}</div>
            </div>
        </div>
    `
    )
}

// Handle form submission
const handleSubmit = async (e) => {
    e.preventDefault()

    // Get data from the form
    const data = new FormData(form)

    // Add user's chat stripe to the chat container
    chatContainer.innerHTML += chatStripe(false, data.get('prompt'))

    // Clear the textarea input
    form.reset()

    // Add bot's chat stripe to the chat container
    const uniqueId = generateUniqueId()
    chatContainer.innerHTML += chatStripe(true, " ", uniqueId)

    // Scroll to the bottom to focus on the latest message
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Get the specific message div using the unique ID
    const messageDiv = document.getElementById(uniqueId)

    // Display a loading indicator in the message div
    loader(messageDiv)

    // Send a request to the backend for a response
    const response = await fetch('https://codex-im0y.onrender.com/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prompt: data.get('prompt')
        })
    })

    clearInterval(loadInterval)
    messageDiv.innerHTML = " "

    if (response.ok) {
        // If the response = successful, extract the bot's reply
        const data = await response.json();
        const parsedData = data.bot.trim() // Trim any trailing spaces or '\n' characters

        // display generated text 
        typeText(messageDiv, parsedData)
    } else {
        // If there is an error in the response, display an error message
        const err = await response.text()

        messageDiv.innerHTML = "Something went wrong"
        alert(err)
    }
}

// Add event listeners for form submission and pressing enter key
form.addEventListener('submit', handleSubmit)
form.addEventListener('keyup', (e) => {
    if (e.keyCode === 13) {
        handleSubmit(e)
    }
})

