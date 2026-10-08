document.querySelectorAll(".card_flip").forEach( card => {
    card.addEventListener("click", () => {
        console.log ("card clicked");
        card.classList.toggle("flipped");

    });
});

const soundToggle = document.getElementById('sound_toggle');
const soundIcon = document.getElementById('sound_icon');
const soundText = document.getElementById('sound_text');
const audio = document.getElementById('weather_audio');

const currentTheme = audio.dataset.theme;
audio.src = `/static/audio/${currentTheme}.mp3`;
const audio = document.getElementById('weather_audio');
audio.volume = 0.3;

let isSoundOn = false;

soundToggle.addEventListener('click', () => {
  isSoundOn = !isSoundOn;

  if (isSoundOn) {
    soundIcon.textContent = '🔊';
    soundText.textContent = 'Sound On';
    audio.play();
  } else {
    soundIcon.textContent = '🔇';
    soundText.textContent = 'Sound Off';
    audio.pause();
  }
});