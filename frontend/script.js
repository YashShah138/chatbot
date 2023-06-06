import bot from './assets/bot.svg'
import user from './assets/user.svg'

// Selecting DOM elements
const form = document.querySelector('form') // Select the first 'form' element in the document
const chatContainer = document.querySelector('#chat_container') // Select the element with the ID 'chat_container'

let loadInterval // Variable to store the interval ID for the loading indicator

// Function to display a loading indicator
function loader(element) {
    element.textContent = '' // Clear the content of the provided element

    // Update the loading indicator text every 300 milliseconds
    loadInterval = setInterval(() => {
        element.textContent += '.'; // Append a dot to the loading indicator text

        // Reset the loading indicator if it reaches three dots
        if (element.textContent === '....') {
            element.textContent = '';
        }
    }, 300);
}

// Function to type text gradually
function typeText(element, text) {
    let index = 0 // Initialize the index for iterating over the characters of the text

    // Add a character from the text to the element every 20 milliseconds
    let interval = setInterval(() => {
        if (index < text.length) {
            element.innerHTML += text.charAt(index); // Append the current character to the element's HTML content
            index++; // Increment the index for the next character
        } else {
            clearInterval(interval); // Stop the interval once all characters have been added
        }
    }, 20);
}

// Generate a unique ID for each message div of the bot
function generateUniqueId() {
    const timestamp = Date.now(); // Get the current timestamp
    const randomNumber = Math.random(); // Generate a random number
    const hexadecimalString = randomNumber.toString(16); // Convert the random number to a hexadecimal string

    return `id-${timestamp}-${hexadecimalString}`; // Return the unique ID string
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
    ); // Return the HTML markup for the chat stripe
}

// Handle form submission
const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the default form submission behavior

    // Get data from the form
    const data = new FormData(form); // Create a FormData object from the form

    // Add user's chat stripe to the chat container
    chatContainer.innerHTML += chatStripe(false, data.get('prompt')); // Append the user's chat stripe HTML to the chat container

    // Clear the textarea input
    form.reset(); // Reset the form to clear the input fields

    // Add bot's chat stripe to the chat container
    const uniqueId = generateUniqueId(); // Generate a unique ID for the bot's chat stripe
    chatContainer.innerHTML += chatStripe(true, " ", uniqueId); // Append the bot's chat stripe HTML to the chat container

    // Scroll to the bottom to focus on the latest message
    chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll the chat container to the bottom

    // Get the specific message div using the unique ID
    const messageDiv = document.getElementById(uniqueId); // Get the element with the unique ID

    // Display a loading indicator in the message div
    loader(messageDiv); // Call the loader function to display the loading indicator

    // Send a request to the backend for a response
    // const response = /* connect to backend */; // Placeholder for the actual backend connection code

    clearInterval(loadInterval); // Clear the loading indicator interval
    messageDiv.innerHTML = " "; // Clear the loading indicator text

    if (response.ok) {
        // If the response = successful, extract the bot's reply
        const data = await response.json(); // Parse the response as JSON
        const parsedData = data.bot.trim(); // Trim any trailing spaces or '\n' characters

        // Display the generated text gradually
        typeText(messageDiv, parsedData); // Call the typeText function to gradually display the bot's reply
    } else {
        // If there is an error in the response, display an error message
        const err = await response.text(); // Get the error message from the response

        messageDiv.innerHTML = "Something went wrong"; // Display a generic error message
        alert(err); // Show the actual error message in an alert dialog
    }
}

// Add event listeners for form submission and pressing enter key
form.addEventListener('submit', handleSubmit); // Handle form submission on 'submit' event
form.addEventListener('keyup', (e) => {
    if (e.keyCode === 13) {
        handleSubmit(e); // Handle form submission when the Enter key is pressed
    }
});
