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

if (soundToggle && soundIcon && soundText && audio) {
  const currentTheme = audio.dataset.theme;
  const audioExtension = currentTheme === 'storm' ? 'wav' : 'mp3';
  audio.src = `/static/audio/${currentTheme}.${audioExtension}`;
  audio.volume = 0;

  const targetVolume = 0.3;
  const fadeDuration = 250;
  let isSoundOn = false;
  let fadeFrame = 0;
  let playbackRequest = 0;

  const updateSoundControl = () => {
    soundToggle.setAttribute('aria-pressed', String(isSoundOn));
    soundToggle.setAttribute('aria-label', isSoundOn ? 'Turn weather sound off' : 'Turn weather sound on');
    soundIcon.textContent = isSoundOn ? '🔊' : '🔇';
    soundText.textContent = isSoundOn ? 'Sound On' : 'Sound Off';
  };

  const fadeVolume = (target, pauseWhenSilent = false) => {
    cancelAnimationFrame(fadeFrame);
    const startingVolume = audio.volume;
    const startTime = performance.now();

    const animate = (currentTime) => {
      const progress = Math.min((currentTime - startTime) / fadeDuration, 1);
      audio.volume = startingVolume + (target - startingVolume) * progress;

      if (progress < 1) {
        fadeFrame = requestAnimationFrame(animate);
      } else {
        fadeFrame = 0;
        if (pauseWhenSilent && !isSoundOn) {
          audio.pause();
        }
      }
    };

    fadeFrame = requestAnimationFrame(animate);
  };

  updateSoundControl();
  soundToggle.addEventListener('click', () => {
    const currentRequest = ++playbackRequest;
    isSoundOn = !isSoundOn;
    updateSoundControl();

    if (!isSoundOn) {
      fadeVolume(0, true);
      return;
    }

    audio.play()
      .then(() => {
        if (currentRequest !== playbackRequest) {
          return;
        }

        if (isSoundOn) {
          fadeVolume(targetVolume);
        } else {
          audio.pause();
        }
      })
      .catch((error) => {
        if (currentRequest === playbackRequest && isSoundOn) {
          isSoundOn = false;
          updateSoundControl();
          fadeVolume(0, true);
          console.error('Weather sound could not be played.', error);
        }
      });
  });
}


const cityInput = document.getElementById('city-input');
const suggestionsList = document.getElementById('suggestions_list');
let debounceTimer;

cityInput.addEventListener('input', () => {
  clearTimeout(debounceTimer);
  const query = cityInput.value.trim();

  if (query.length < 2) {
    suggestionsList.innerHTML = '';
    return;
  }

  debounceTimer = setTimeout(() => {
    fetch(`/autocomplete?q=${query}`)
      .then(response => response.json())
      .then(data => {
        suggestionsList.innerHTML = '';

        if (data.length === 0) return;

        const dropdown = document.createElement('div');
        dropdown.classList.add('suggestions_dropdown');

        data.forEach(place => {
          const item = document.createElement('div');
          item.classList.add('suggestion_item');
          item.textContent = place.label;

          item.addEventListener('click', () => {
            cityInput.value = place.name;
            suggestionsList.innerHTML = '';
          });

          dropdown.appendChild(item);
        });

        suggestionsList.appendChild(dropdown);
      });
  }, 300);
});


document.addEventListener('click', (event) => {
  if (!cityInput.contains(event.target) && !suggestionsList.contains(event.target)) {
    suggestionsList.innerHTML = '';
  }
});