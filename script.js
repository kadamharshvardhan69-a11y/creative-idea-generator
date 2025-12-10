async function generateIdea() {
    const topic = document.getElementById("topicInput").value;
    const resultBox = document.getElementById("result");
    const loadingText = document.getElementById("loading");

    if (!topic.trim()) {
        resultBox.innerText = "Please enter a topic!";
        return;
    }

    // Show loading animation
    loadingText.classList.remove("hidden");
    resultBox.innerText = "";


    try {
        console.log("Generating idea for topic:", topic);
        const response = await fetch("http://127.0.0.1:5000/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic })
        });


        const data = await response.json();
        console.log('data:', data);
        resultBox.innerText = data.idea;

    } catch (error) {
        resultBox.innerText = "Error: Could not generate idea. Check backend.";
        console.error(error);
    }

    // Hide loading
    loadingText.classList.add("hidden");
}
