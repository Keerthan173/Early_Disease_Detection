document.addEventListener("DOMContentLoaded", () => {
    displayGreeting();
});

function displayGreeting() {
    let hour = new Date().getHours();
    let greetingText = hour < 12 ? "Good Morning!" : hour < 18 ? "Good Afternoon!" : "Good Evening!";
    document.getElementById("greeting").innerText = greetingText;
}

function navigateToDetection() {
    window.location.href = "detection.html";
}


function startDetection() {
    let loading = document.getElementById("loading");
    let result = document.getElementById("result");

    loading.classList.remove("hidden");
    result.classList.add("hidden");

    setTimeout(() => {
        loading.classList.add("hidden");
        result.classList.remove("hidden");
    }, 3000);
}
document.getElementById("imageUpload").addEventListener("change", function(event) {
    const file = event.target.files[0];
    const previewImage = document.getElementById("previewImage");

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewImage.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});

