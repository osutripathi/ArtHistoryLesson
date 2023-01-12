let currentSlide = 0;
let score = 0;

const sleep = ms => new Promise(r => setTimeout(r, ms));

function setInformation(slides) {
    document.getElementById("artTitle").innerText = slides[currentSlide].getAttribute("artTitle");
    document.getElementById("artistName").innerText = slides[currentSlide].getAttribute("artist");
}

function resetSlideshow(slides) {
    for(let i = 1; i < slides.length; i++)
        slides[i].style.display = "none";
    
    currentSlide = 0;
    setInformation(slides, currentSlide);
}

function cleanUp(slides) {
    console.log("started cleanup");
    for(let i = 0; i < slides.length; i++)
        slides[i].style.display = "none";

    document.getElementById("artistName").style.display = "none";
    document.getElementById("userResponse").style.display = "none";
    document.getElementsByClassName("form-group")[0].style.display = "none";
    document.getElementById("submit-button").style.display = "none";
    document.getElementById("artTitle").innerText = "Your Score: " + score;
    
}

async function checkAnswer() {
    let textField = document.getElementById("userResponse");
    let answer = textField.value;
    textField.value = "";

    let slides = document.getElementsByClassName("slideshow-images");
    let correctAnswer = slides[currentSlide].getAttribute("artMovement");
    if(answer.toLowerCase() === correctAnswer.toLowerCase()) {
        party.confetti(document.getElementById("submit-button"));
        score++;
    }
    else {
        document.getElementById("artTitle").innerText = "Sorry!";
        document.getElementById("artistName").innerText = "The correct answer is " + correctAnswer;
        await sleep(2500);
    }

    if(currentSlide == slides.length - 1)
        cleanUp(slides);
    else {
        slides[currentSlide].style.display = "none";
        currentSlide++;
        slides[currentSlide].style.display = "block";
        setInformation(slides);
    }
}

window.onload = function() {
    let slides = document.getElementsByClassName("slideshow-images");
    resetSlideshow(slides);
}