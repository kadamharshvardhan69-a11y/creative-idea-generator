// Input validation and sanitization
function validateAndSanitizeInput(input) {
    // Trim whitespace
    let sanitized = input.trim();

    // Check if empty after trimming
    if (!sanitized) {
        return { valid: false, error: "Please enter a topic!" };
    }

    // Check minimum length
    if (sanitized.length < 2) {
        return { valid: false, error: "Topic must be at least 2 characters long." };
    }

    // Check maximum length (100 characters)
    if (sanitized.length > 100) {
        return { valid: false, error: "Topic is too long. Please keep it under 100 characters." };
    }

    // Remove null bytes (security)
    sanitized = sanitized.replace(/\0/g, '');

    // Check for suspicious patterns (basic security check)
    const suspiciousPatterns = [
        /<script[^>]>.?<\/script>/gi,  // Script tags
        /javascript:/gi,                  // JavaScript protocol
        /on\w+\s*=/gi,                   // Event handlers (onclick, onerror, etc.)
        /<iframe/gi,                      // Iframes
        /eval\(/gi,                       // Eval function
    ];

    let hasSuspiciousContent = false;
    for (const pattern of suspiciousPatterns) {
        if (pattern.test(sanitized)) {
            hasSuspiciousContent = true;
            break;
        }
    }

    if (hasSuspiciousContent) {
        return { valid: false, error: "Invalid characters detected. Please enter a normal topic." };
    }

    return { valid: true, value: sanitized };
}

// Safely display text (prevent XSS)
function safeDisplayText(element, text) {
    // Use textContent instead of innerHTML to prevent XSS
    element.textContent = text;
}

async function generateIdea() {
    const topicInput = document.getElementById("topicInput");
    const topic = topicInput.value;
    const resultBox = document.getElementById("result");
    const loadingText = document.getElementById("loading");

    // Validate and sanitize input
    const validation = validateAndSanitizeInput(topic);

    if (!validation.valid) {
        safeDisplayText(resultBox, validation.error);
        resultBox.style.color = "#ff6b6b"; // Red color for errors
        return;
    }

    // Reset result box styling
    resultBox.style.color = "";
    loadingText.classList.remove("hidden");
    safeDisplayText(resultBox, "");

    try {
        console.log("Sending request to backend with topic:", validation.value);

        const response = await new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            xhr.open("POST", "http://127.0.0.1:5000/generate", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.setRequestHeader("Accept", "application/json");

            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        try {
                            const data = JSON.parse(xhr.responseText);
                            resolve(data);
                        } catch (parseError) {
                            reject(new Error("Invalid response from server"));
                        }
                    } else if (xhr.status === 400) {
                        try {
                            const errorData = JSON.parse(xhr.responseText);
                            reject(new Error(errorData.error || "Invalid request"));
                        } catch (parseError) {
                            reject(new Error("Invalid request"));
                        }
                    } else if (xhr.status === 500) {
                        try {
                            const errorData = JSON.parse(xhr.responseText);
                            reject(new Error(errorData.error || "Server error occurred"));
                        } catch (parseError) {
                            reject(new Error("Server error occurred"));
                        }
                    } else {
                        reject(new Error(`Server returned ${xhr.status}: ${xhr.statusText}`));
                    }
                }
            };

            xhr.onerror = function() {
                reject(new Error("Network error"));
            };

            xhr.send(JSON.stringify({ topic: validation.value }));
        });

        // Validate response
        if (!response || !response.idea) {
            throw new Error("Invalid response from server");
        }

        // Safely display the result
        safeDisplayText(resultBox, response.idea);
        resultBox.style.color = "#757977ff"; // Green color for success

    } catch (error) {
        console.error("Error generating idea:", error);

        // User-friendly error messages
        let errorMessage = "Error: Could not generate idea. ";

        if (error.message.includes("Failed to fetch")) {
            errorMessage += "Please make sure the Flask server is running on port 5000.";
        } else if (error.message.includes("NetworkError")) {
            errorMessage += "Network error. Check your connection.";
        } else {
            errorMessage += error.message;
        }

        safeDisplayText(resultBox, errorMessage);
        resultBox.style.color = "#ff6b6b"; // Red color for errors
    } finally {
        loadingText.classList.add("hidden");
    }
}

// Optional: Add Enter key support
document.addEventListener('DOMContentLoaded', function () {
    const topicInput = document.getElementById("topicInput");
    if (topicInput) {
        topicInput.addEventListener('keypress', function (event) {
            if (event.key === 'Enter') {
                generateIdea();
            }
        });
    }
});