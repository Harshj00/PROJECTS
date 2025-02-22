const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const deleteButton = document.querySelector("#delete-btn");
const themeButton = document.querySelector("#theme-btn");
const body = document.body;

let userText = null;

// Add theme colors
const lightTheme = {
    '--text-color': '#343541',
    '--icon-color': '#5b5e71',
    '--icon-hover-bg': '#ACACBE',
    '--placeholder-color': '#666666',
    '--outgoing-chat-bg': '#ffffff',
    '--incoming-chat-bg': '#f7f7f8',
    '--outgoing-chat-border': '#e5e5e5',
    '--incoming-chat-border': '#e5e5e5',
    '--chat-shadow': '0 2px 5px rgba(0, 0, 0, 0.05)'
};

const darkTheme = {
    '--text-color': '#FFFFFF',
    '--icon-color': '#ACACBE',
    '--icon-hover-bg': '#5b5e71',
    '--placeholder-color': '#cccccc',
    '--outgoing-chat-bg': '#343541',
    '--incoming-chat-bg': '#444654',
    '--outgoing-chat-border': '#343541',
    '--incoming-chat-border': '#444654',
    '--chat-shadow': '0 2px 5px rgba(0, 0, 0, 0.1)'
};

// Function to set theme
const setTheme = (theme) => {
    const root = document.documentElement;
    for (const [property, value] of Object.entries(theme)) {
        root.style.setProperty(property, value);
    }
};

// Theme toggle handler
themeButton.addEventListener("click", () => {
    // Toggle theme icon
    themeButton.textContent = themeButton.textContent === "light_mode" 
        ? "dark_mode" 
        : "light_mode";
    
    // Toggle theme colors
    const isLightMode = themeButton.textContent === "dark_mode";
    setTheme(isLightMode ? lightTheme : darkTheme);
    
    // Save preference
    localStorage.setItem("theme", isLightMode ? "light" : "dark");
});

// Load saved theme preference
window.addEventListener("load", () => {
    const savedTheme = localStorage.getItem("theme") || "dark";
    if (savedTheme === "light") {
        themeButton.click(); // Trigger theme switch if light theme was saved
    }
});

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
    
    // Creator response
    if (text.includes("who created you") || 
        text.includes("who made you") || 
        text.includes("your creator") ||
        text.includes("who developed you") ||
        text.includes("who designed you")) {
        return "Mr. Harsh Jha created me";
    }

    // Advanced Math Keywords
    if (text.includes("integrate") || text.includes("integration")) {
        return "For integration problems, I recommend breaking them down step by step:\n" +
               "1. For basic integrals: ∫x dx = x²/2 + C\n" +
               "2. For exponential: ∫eˣ dx = eˣ + C\n" +
               "3. For trigonometric: ∫sin(x) dx = -cos(x) + C\n" +
               "Please specify the function you'd like to integrate.";
    }

    if (text.includes("differentiate") || text.includes("derivative")) {
        return "For differentiation problems:\n" +
               "1. Power rule: d/dx(xⁿ) = n·xⁿ⁻¹\n" +
               "2. Exponential: d/dx(eˣ) = eˣ\n" +
               "3. Trigonometric: d/dx(sin(x)) = cos(x)\n" +
               "Please specify the function you'd like to differentiate.";
    }

    if (text.includes("logarithm") || text.includes("log")) {
        return "Logarithm properties:\n" +
               "1. log(xy) = log(x) + log(y)\n" +
               "2. log(x/y) = log(x) - log(y)\n" +
               "3. log(xⁿ) = n·log(x)\n" +
               "Please specify your logarithm question.";
    }

    if (text.includes("trigonometry") || text.includes("trig")) {
        return "Trigonometric formulas:\n" +
               "1. sin²(x) + cos²(x) = 1\n" +
               "2. tan(x) = sin(x)/cos(x)\n" +
               "3. sin(A+B) = sin(A)cos(B) + cos(A)sin(B)\n" +
               "Please specify your trigonometry question.";
    }

    // Basic Math Operations
    if (text.includes("calculate") || text.includes("solve") || /[0-9+\-*/()]/.test(text)) {
        const mathExpression = text.match(/[0-9+\-*/().]+/g);
        if (mathExpression) {
            const result = evaluateMathExpression(mathExpression[0]);
            return `The result is: ${result}`;
        }
    }
    
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

    if (text.includes("factorial")) {
        const number = text.match(/\d+/);
        if (number) {
            const n = parseInt(number[0]);
            if (n > 170) return "Number too large for factorial calculation";
            let result = 1;
            for (let i = 2; i <= n; i++) result *= i;
            return `The factorial is: ${result}`;
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

    // Standard responses
    if (text.includes("hello") || text.includes("hi") || text.includes("hey")) {
        return "Hello! I'm your mathematical assistant. I can help with:\n" +
               "- Basic arithmetic\n" +
               "- Integration and differentiation\n" +
               "- Trigonometry\n" +
               "- Logarithms\n" +
               "- And much more!\n" +
               "What would you like to calculate?";
    } 
    else if (text.includes("how are you")) {
        return "I'm doing well, thank you for asking! Ready to solve some math problems!";
    }
    else if (text.includes("your name")) {
        return "I'm HarshGPT, your mathematical genius assistant!";
    }
    else if (text.includes("bye") || text.includes("goodbye")) {
        return "Goodbye! Remember, math is beautiful!";
    }
    else if (text.includes("thank")) {
        return "You're welcome! Math is my passion, and I'm happy to help!";
    }
    else {
        return "I can help you with various mathematical topics including:\n" +
               "1. Basic Arithmetic:\n" +
               "   - Addition, subtraction, multiplication, division\n" +
               "   - Square roots and powers\n" +
               "   - Factorial calculations\n\n" +
               "2. Advanced Mathematics:\n" +
               "   - Integration\n" +
               "   - Differentiation\n" +
               "   - Trigonometry\n" +
               "   - Logarithms\n\n" +
               "Please ask your question, and I'll help you solve it!";
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