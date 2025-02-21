const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const deleteButton = document.querySelector("#delete-btn");

let userText = null;

const createElement = (html, className) => {
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className);
    chatDiv.innerHTML = html;
    return chatDiv;
}

const evaluateMathExpression = (expression) => {
    try {
        // Remove any unsafe characters and evaluate
        const sanitizedExp = expression.replace(/[^0-9+\-*/().]/g, '');
        return eval(sanitizedExp);
    } catch (error) {
        return "Sorry, I couldn't calculate that. Please check your expression.";
    }
}

const getSimpleResponse = (userText) => {
    const text = userText.toLowerCase();
    
    // Add creator response
    if (text.includes("who created you") || 
        text.includes("who made you") || 
        text.includes("your creator") ||
        text.includes("who developed you") ||
        text.includes("who designed you")) {
        return "Mr. Harsh Jha created me";
    }
    
    // Math operations detection
    if (text.includes("calculate") || text.includes("solve") || /[0-9+\-*/()]/.test(text)) {
        // Extract numbers and operators
        const mathExpression = text.match(/[0-9+\-*/().]+/g);
        if (mathExpression) {
            const result = evaluateMathExpression(mathExpression[0]);
            return `The result is: ${result}`;
        }
    }
    
    // Basic math keywords
    if (text.includes("add") || text.includes("plus") || text.includes("sum")) {
        const numbers = text.match(/\d+/g);
        if (numbers && numbers.length >= 2) {
            const sum = numbers.reduce((a, b) => parseInt(a) + parseInt(b), 0);
            return `The sum is: ${sum}`;
        }
    }
    
    if (text.includes("subtract") || text.includes("minus")) {
        const numbers = text.match(/\d+/g);
        if (numbers && numbers.length >= 2) {
            const difference = numbers.reduce((a, b) => parseInt(a) - parseInt(b));
            return `The difference is: ${difference}`;
        }
    }
    
    if (text.includes("multiply") || text.includes("times")) {
        const numbers = text.match(/\d+/g);
        if (numbers && numbers.length >= 2) {
            const product = numbers.reduce((a, b) => parseInt(a) * parseInt(b));
            return `The product is: ${product}`;
        }
    }
    
    if (text.includes("divide") || text.includes("divided by")) {
        const numbers = text.match(/\d+/g);
        if (numbers && numbers.length >= 2) {
            if (numbers[1] === '0') {
                return "Cannot divide by zero!";
            }
            const quotient = (parseInt(numbers[0]) / parseInt(numbers[1])).toFixed(2);
            return `The result is: ${quotient}`;
        }
    }
    
    if (text.includes("square root") || text.includes("sqrt")) {
        const number = text.match(/\d+/);
        if (number) {
            const sqrt = Math.sqrt(parseInt(number[0])).toFixed(2);
            return `The square root is: ${sqrt}`;
        }
    }
    
    if (text.includes("power") || text.includes("squared") || text.includes("cubed")) {
        const numbers = text.match(/\d+/g);
        if (numbers) {
            let power = 2; // default to square
            if (text.includes("cubed")) power = 3;
            const result = Math.pow(parseInt(numbers[0]), power);
            return `The result is: ${result}`;
        }
    }

    // Original responses
    if (text.includes("hello") || text.includes("hi") || text.includes("hey")) {
        return "Hello! How can I help you today? You can ask me to perform mathematical calculations!";
    } 
    else if (text.includes("how are you")) {
        return "I'm doing well, thank you for asking! I can help you with math problems!";
    }
    else if (text.includes("your name")) {
        return "I'm HarshGPT, your friendly chat assistant! I'm great at math!";
    }
    else if (text.includes("bye") || text.includes("goodbye")) {
        return "Goodbye! Have a great day!";
    }
    else if (text.includes("thank")) {
        return "You're welcome! Let me know if you need help with more calculations!";
    }
    else {
        return "I can help you with mathematical calculations! Try asking me to:\n" +
               "- Calculate simple expressions (e.g., '2 + 2')\n" +
               "- Add numbers (e.g., 'add 5 and 3')\n" +
               "- Subtract numbers (e.g., 'subtract 10 from 20')\n" +
               "- Multiply numbers (e.g., 'multiply 4 and 5')\n" +
               "- Divide numbers (e.g., 'divide 10 by 2')\n" +
               "- Find square root (e.g., 'square root of 16')\n" +
               "- Calculate powers (e.g., 'what is 2 squared')";
    }
}

const handleOutgoingChat = () => {
    userText = chatInput.value.trim();
    if (!userText) return;
    
    // Clear input and disable temporarily
    chatInput.value = "";
    chatInput.disabled = true;
    sendButton.disabled = true;
    
    // Add user's message to chat
    const html = `
    <div class="chat-content">
        <div class="chat-details">
            <p>${userText}</p>
            <img src="public/user.jpg" alt="user" width="20px" height="20px">
        </div>
    </div>`;
    const outgoingChatDiv = createElement(html, "outgoing");
    chatContainer.appendChild(outgoingChatDiv);
    
    // Get response after a short delay
    setTimeout(() => {
        const response = getSimpleResponse(userText);
        
        const responseHtml = `
        <div class="chat-content">
            <div class="chat-details">
                <img src="public/thinking.png" alt="chatbot" width="20px" height="20px">
                <p>${response}</p>
            </div>
            <span class="material-symbols-rounded">content_copy</span>
        </div>`;
        const incomingChatDiv = createElement(responseHtml, "incoming");
        chatContainer.appendChild(incomingChatDiv);
        
        // Re-enable input and button
        chatInput.disabled = false;
        sendButton.disabled = false;
        chatInput.focus();
    }, 1000);
}

// Event listeners
sendButton.addEventListener("click", handleOutgoingChat);

chatInput.addEventListener("keyup", (e) => {
    if (e.key === "Enter") {
        handleOutgoingChat();
    }
});

deleteButton.addEventListener("click", () => {
    chatContainer.innerHTML = "";
});

// Add title attribute for hover text
deleteButton.setAttribute("title", "Clear Chat");

// Add input placeholder
chatInput.setAttribute("placeholder", "Type your message here...");