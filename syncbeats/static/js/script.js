const likeButton = document.getElementById("like-button");
const totalLikeCount = document.getElementById("total-like-count");
const youtubeLinkInput = document.getElementById("youtube-link");
const playYoutubeVideoButton = document.getElementById("play-youtube-video");
const videoContainer = document.getElementById("video-container");
const currentTimeDisplay = document.getElementById("current-time");
const setTimerButton = document.getElementById("set-timer");
const timerInput = document.getElementById("video-timer");
let timerId;

function updateTotalLikeCount(count) {
    totalLikeCount.textContent = count;
}

async function fetchTotalLikes() {
    const response = await fetch('/total-likes');
    const data = await response.json();
    updateTotalLikeCount(data.total_likes);
}

fetchTotalLikes();

const userId = "{{ user.id }}";
const ws = new WebSocket(`ws://localhost:9000/ws/like?user_id=${userId}`);

ws.onmessage = function(event) {
    const count = parseInt(event.data);
    updateTotalLikeCount(count);
};

likeButton.addEventListener("click", function() {
    ws.send("like");
});

playYoutubeVideoButton.addEventListener("click", function() {
const youtubeLink = youtubeLinkInput.value;
const url = new URL(youtubeLink);
const videoId = url.searchParams.get("v");
const startTimeParam = url.searchParams.get("t");
let startTimeInSeconds = 0;
if (startTimeParam) {
    const match = startTimeParam.match(/(\d+)s/);
    if (match) {
        startTimeInSeconds = parseInt(match[1]);
    }
}

if (videoId) {
    const iframe = document.createElement("iframe");
    iframe.width = "560";
    iframe.height = "315";
    iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`; // Убираем startTimeInSeconds
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    iframe.allowfullscreen = true;
    videoContainer.innerHTML = "";
    videoContainer.appendChild(iframe);
} else {
    alert("Invalid YouTube video link. Please provide a valid link.");
}
});


setTimerButton.addEventListener("click", function() {
    const videoTimeInput = timerInput.value;
    const videoTimeParts = videoTimeInput.split(":");
    const hours = parseInt(videoTimeParts[0]);
    const minutes = parseInt(videoTimeParts[1]);

    const youtubeLink = youtubeLinkInput.value;
    const url = new URL(youtubeLink);
    const startTimeParam = url.searchParams.get("t");
    let startTimeInSeconds = 0;
    if (startTimeParam) {
        const match = startTimeParam.match(/(\d+)s/);
        if (match) {
            startTimeInSeconds = parseInt(match[1]);
        }
    }

    const videoStartTime = new Date();
    videoStartTime.setHours(hours);
    videoStartTime.setMinutes(minutes);
    videoStartTime.setSeconds(0);

    const adjustedStartTime = videoStartTime.getTime() - startTimeInSeconds * 1000;

    const now = new Date().getTime();
    const difference = adjustedStartTime - now - 3;

    if (difference > 0) {
        clearTimeout(timerId);
        timerId = setTimeout(playVideoAfterTimeout, difference);
        const formattedTime = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
        alert(`Drop will start at ${formattedTime}`);
    } else {
        alert("Please enter a valid future time for video start.");
    }
});

function playVideoAfterTimeout() {
    playYoutubeVideoButton.click();
}

function updateCurrentTime() {
    const currentTime = new Date();
    const hours = currentTime.getHours().toString().padStart(2, '0');
    const minutes = currentTime.getMinutes().toString().padStart(2, '0');
    const seconds = currentTime.getSeconds().toString().padStart(2, '0');
    const formattedTime = `${hours}:${minutes}:${seconds}`;
    currentTimeDisplay.textContent = formattedTime;
}

setInterval(updateCurrentTime, 1000);

updateCurrentTime();