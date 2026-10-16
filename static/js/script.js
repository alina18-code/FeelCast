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

document.querySelectorAll('.temp_graph polyline').forEach((polyline) => {
  const points = (polyline.getAttribute('points') || '')
    .trim()
    .split(/\s+/)
    .map((point) => point.split(',').map(Number))
    .filter((point) => point.length === 2 && point.every(Number.isFinite));

  if (points.length < 3) {
    return;
  }

  let pathData = `M ${points[0][0]} ${points[0][1]}`;

  for (let index = 0; index < points.length - 1; index += 1) {
    const previous = points[Math.max(index - 1, 0)];
    const current = points[index];
    const next = points[index + 1];
    const following = points[Math.min(index + 2, points.length - 1)];
    const control1 = [
      current[0] + (next[0] - previous[0]) / 6,
      current[1] + (next[1] - previous[1]) / 6,
    ];
    const control2 = [
      next[0] - (following[0] - current[0]) / 6,
      next[1] - (following[1] - current[1]) / 6,
    ];
    const segmentMinY = Math.min(current[1], next[1]);
    const segmentMaxY = Math.max(current[1], next[1]);
    control1[1] = Math.min(Math.max(control1[1], segmentMinY), segmentMaxY);
    control2[1] = Math.min(Math.max(control2[1], segmentMinY), segmentMaxY);

    pathData += ` C ${control1[0]} ${control1[1]}, ${control2[0]} ${control2[1]}, ${next[0]} ${next[1]}`;
  }

  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  Array.from(polyline.attributes).forEach((attribute) => {
    if (attribute.name !== 'points') {
      path.setAttribute(attribute.name, attribute.value);
    }
  });
  path.setAttribute('d', pathData);
  path.setAttribute('class', 'graph_curve');

  const area = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  area.setAttribute(
    'd',
    `${pathData} L ${points[points.length - 1][0]} 150 L ${points[0][0]} 150 Z`
  );
  area.setAttribute('fill', 'url(#tempAreaGradient)');
  area.setAttribute('class', 'graph_area');
  polyline.before(area);
  polyline.replaceWith(path);
});

function createWeatherParticles(theme) {
  const container = document.getElementById('weather_particles');
  if (!container) return;

  container.innerHTML = '';

  if (theme === 'rain' || theme === 'storm') {
    for (let i = 0; i < 60; i++) {
      const drop = document.createElement('div');
      drop.classList.add('raindrop');
      drop.style.left = `${Math.random() * 100}%`;
      drop.style.animationDuration = `${0.5 + Math.random() * 0.5}s`;
      drop.style.animationDelay = `${Math.random() * 2}s`;
      container.appendChild(drop);
    }
  }

  if (theme === 'snow') {
    for (let i = 0; i < 40; i++) {
      const flake = document.createElement('div');
      flake.classList.add('snowflake');
      flake.textContent = '❄';
      flake.style.left = `${Math.random() * 100}%`;
      flake.style.fontSize = `${8 + Math.random() * 10}px`;
      flake.style.animationDuration = `${6 + Math.random() * 6}s`;
      flake.style.animationDelay = `${Math.random() * 5}s`;
      container.appendChild(flake);
    }
  }
}

const currentPageTheme = document.querySelector('.main_page').classList[1];
createWeatherParticles(currentPageTheme);

const dailyRow = document.getElementById('daily_forecast_row');
const scrollNextBtn = document.getElementById('daily_scroll_next');
const scrollPrevBtn = document.getElementById('daily_scroll_prev');


if (scrollNextBtn) {
  scrollNextBtn.addEventListener('click', () => {
    dailyRow.scrollBy({ left: 160, behavior: 'smooth' });
  });
}

if (scrollPrevBtn) {
  scrollPrevBtn.addEventListener('click', () => {
    dailyRow.scrollBy({ left: -160, behavior: 'smooth' });
  });
}