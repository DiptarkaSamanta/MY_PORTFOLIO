// Loader
window.addEventListener('load', () => {
  const loader = document.getElementById('loader');
  
  setTimeout(() => {
    if (loader) {
      loader.style.opacity = 0;
      setTimeout(() => {
        loader.style.display = 'none';
      }, 800);
    }
  }, 1000);

  // Initialize map graphics on startup based on loaded values
  if (typeof window.onThemeChangedMap === 'function') {
    window.onThemeChangedMap(window.currentTheme || 'day');
  }
  if (typeof window.onWeatherChangedMap === 'function') {
    window.onWeatherChangedMap(window.weatherType || 'clear');
  }
  
  // Start weather loop
  initWeatherParticles();
  drawWeather();

  // Initialize dynamic positioning of hotspot preview cards
  initHotspotAdjuster();
});

// Map specific hooks called by toolbox.js when themes or weather change
window.onThemeChangedMap = function(time) {
  // Update Background Images (cross-fade)
  document.querySelectorAll('.map-bg').forEach(img => {
    img.classList.remove('active');
  });
  const bgImg = document.getElementById(`bg-${time}`);
  if (bgImg) bgImg.classList.add('active');
};

window.onWeatherChangedMap = function(type) {
  // Apply atmospheric CSS filters to map-wrapper
  const mapWrapper = document.getElementById('mapWrapper');
  if (mapWrapper) {
    if (type === 'clear') {
      mapWrapper.style.filter = '';
    } else if (type === 'rain') {
      mapWrapper.style.filter = 'brightness(90%) contrast(105%)';
    } else if (type === 'snow') {
      mapWrapper.style.filter = 'brightness(95%) contrast(90%)';
    } else if (type === 'thunderstorm') {
      mapWrapper.style.filter = 'brightness(80%) contrast(110%)';
    } else if (type === 'fog') {
      mapWrapper.style.filter = 'blur(2px) brightness(95%)';
    } else if (type === 'cloudy') {
      mapWrapper.style.filter = 'brightness(85%) contrast(95%)';
    }
  }
  
  // Reset particle buffer
  initWeatherParticles();
};

// Interactive Compass Pointer (Rotates to follow mouse)
const compassPointer = document.getElementById('compassPointer');
if (compassPointer) {
  document.addEventListener('mousemove', (e) => {
    const compassRect = compassPointer.getBoundingClientRect();
    const compassCenterX = compassRect.left + compassRect.width / 2;
    const compassCenterY = compassRect.top + compassRect.height / 2;

    const angle = Math.atan2(e.clientY - compassCenterY, e.clientX - compassCenterX);
    const degree = angle * (180 / Math.PI) + 90; // offset so needle red tip points to mouse
    
    compassPointer.style.transform = `rotate(${degree}deg)`;
  });
}

// Camera Zoom and Navigation
function navigateTo(url, hotspotElement, e) {
  // Prevent click propagation in card button
  if (e) {
    e.stopPropagation();
    e.preventDefault();
  }

  const mapWrapper = document.getElementById('mapWrapper');
  if (!mapWrapper) return;
  
  // Calculate percentage coordinate offsets
  const leftPercent = parseFloat(hotspotElement.style.left);
  const topPercent = parseFloat(hotspotElement.style.top);

  // We want to center the screen on this hotspot coordinate.
  const zoomFactor = 2.5;
  const translateX = (50 - leftPercent) * 1.5; // Scale and shift multiplier
  const translateY = (50 - topPercent) * 1.5;

  // Zoom wrapper
  mapWrapper.style.setProperty('--map-zoom', zoomFactor);
  mapWrapper.style.setProperty('--map-x', `${translateX}%`);
  mapWrapper.style.setProperty('--map-y', `${translateY}%`);

  // Add screen black out overlay
  const blackout = document.createElement('div');
  blackout.style.position = 'fixed';
  blackout.style.inset = '0';
  blackout.style.background = '#030712';
  blackout.style.opacity = '0';
  blackout.style.transition = 'opacity 0.8s ease';
  blackout.style.zIndex = '9998';
  document.body.appendChild(blackout);

  setTimeout(() => {
    blackout.style.opacity = '1';
  }, 100);

  // Redirect after transition completes
  setTimeout(() => {
    window.location.href = url;
  }, 1000);
}

// Weather Particle Canvas Loop
const canvas = document.getElementById('weatherCanvas');
let ctx = null;
let animationId = null;
let weatherParticles = [];

function resizeCanvas() {
  if (canvas) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
}

function initWeatherParticles() {
  if (!canvas) return;
  ctx = canvas.getContext('2d');
  resizeCanvas();
  
  weatherParticles = [];
  const maxParticles = weatherType === 'thunderstorm' ? 180 : (weatherType === 'rain' ? 120 : 60);
  
  if (weatherType === 'rain' || weatherType === 'thunderstorm') {
    for (let i = 0; i < maxParticles; i++) {
      weatherParticles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height - canvas.height,
        vy: 10 + Math.random() * 8,
        vx: -1 - Math.random() * 2, // angle falling to left
        length: 12 + Math.random() * 10,
        opacity: 0.15 + Math.random() * 0.3
      });
    }
  } else if (weatherType === 'snow') {
    for (let i = 0; i < maxParticles; i++) {
      weatherParticles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vy: 0.8 + Math.random() * 1.2,
        vx: (Math.random() - 0.5) * 0.5,
        radius: 1.5 + Math.random() * 2.5,
        opacity: 0.2 + Math.random() * 0.6,
        angle: Math.random() * Math.PI * 2
      });
    }
  } else if (weatherType === 'fog' || weatherType === 'cloudy') {
    // Fog or Clouds: large puffy shapes moving slowly
    const count = weatherType === 'fog' ? 8 : 4;
    for (let i = 0; i < count; i++) {
      weatherParticles.push({
        x: Math.random() * (canvas.width + 400) - 200,
        y: Math.random() * canvas.height,
        radius: 150 + Math.random() * 150,
        vx: weatherType === 'fog' ? (Math.random() - 0.5) * 0.1 : 0.1 + Math.random() * 0.2,
        vy: (Math.random() - 0.5) * 0.05,
        opacity: weatherType === 'fog' ? 0.08 + Math.random() * 0.08 : 0.05 + Math.random() * 0.08
      });
    }
  }
}

let lastFlash = 0;
let flashActive = false;
let flashDuration = 0;

function drawWeather() {
  if (!canvas || !ctx) return;
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  if (weatherType === 'clear') {
    animationId = requestAnimationFrame(drawWeather);
    return;
  }
  
  // Render based on active type
  if (weatherType === 'rain' || weatherType === 'thunderstorm') {
    // Lightning Flash triggers
    if (weatherType === 'thunderstorm') {
      const now = Date.now();
      if (!flashActive && now - lastFlash > 5000 + Math.random() * 8000) {
        flashActive = true;
        flashDuration = 50 + Math.random() * 150;
        lastFlash = now;
      }
      
      if (flashActive) {
        const flashElapsed = now - lastFlash;
        if (flashElapsed < flashDuration) {
          ctx.fillStyle = `rgba(255, 255, 255, ${0.15 * Math.sin((flashElapsed / flashDuration) * Math.PI)})`;
          ctx.fillRect(0, 0, canvas.width, canvas.height);
        } else {
          flashActive = false;
        }
      }
    }
    
    ctx.strokeStyle = 'rgba(174, 219, 255, 0.4)';
    ctx.lineWidth = 1.2;
    ctx.lineCap = 'round';
    
    weatherParticles.forEach(p => {
      ctx.beginPath();
      ctx.moveTo(p.x, p.y);
      ctx.lineTo(p.x + p.vx * 0.8, p.y + p.length);
      ctx.strokeStyle = `rgba(174, 219, 255, ${p.opacity})`;
      ctx.stroke();
      
      p.x += p.vx;
      p.y += p.vy;
      
      if (p.y > canvas.height) {
        p.y = -p.length;
        p.x = Math.random() * canvas.width;
      }
      if (p.x < -20) {
        p.x = canvas.width + 10;
      }
    });
    
  } else if (weatherType === 'snow') {
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    
    weatherParticles.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${p.opacity})`;
      ctx.fill();
      
      p.y += p.vy;
      p.x += p.vx + Math.sin(p.angle) * 0.3;
      p.angle += 0.02;
      
      if (p.y > canvas.height) {
        p.y = -10;
        p.x = Math.random() * canvas.width;
      }
      if (p.x > canvas.width + 10 || p.x < -10) {
        p.x = Math.random() * canvas.width;
      }
    });
    
  } else if (weatherType === 'fog' || weatherType === 'cloudy') {
    weatherParticles.forEach(p => {
      const grad = ctx.createRadialGradient(p.x, p.y, 10, p.x, p.y, p.radius);
      grad.addColorStop(0, `rgba(240, 243, 248, ${p.opacity})`);
      grad.addColorStop(0.5, `rgba(240, 243, 248, ${p.opacity * 0.4})`);
      grad.addColorStop(1, 'rgba(240, 243, 248, 0)');
      
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();
      
      p.x += p.vx;
      p.y += p.vy;
      
      if (p.vx > 0 && p.x - p.radius > canvas.width) {
        p.x = -p.radius;
        p.y = Math.random() * canvas.height;
      } else if (p.vx < 0 && p.x + p.radius < 0) {
        p.x = canvas.width + p.radius;
        p.y = Math.random() * canvas.height;
      }
    });
  }
  
  animationId = requestAnimationFrame(drawWeather);
}



// Dynamic positioning for hotspot cards to prevent clipping
function initHotspotAdjuster() {
  const hotspots = document.querySelectorAll('.hotspot');
  
  hotspots.forEach(hotspot => {
    const location = hotspot.getAttribute('data-location');
    const card = hotspot.querySelector('.hotspot-card');
    if (!card) return;

    if (location === 'Industry & Port') {
      // Open card to the left side
      card.classList.add('card-left');
      card.classList.remove('card-below', 'card-right');
      card.style.bottom = 'auto';
      card.style.top = '50%';
      card.style.left = 'auto';
    } else if (location === 'Home') {
      // Open card to the right side (Diptarka Samanta card)
      card.classList.add('card-right');
      card.classList.remove('card-below', 'card-left');
      card.style.bottom = 'auto';
      card.style.top = '50%';
      card.style.left = '45px';
    } else if (location === 'Observatory' || location === 'Code Terminal' || location === 'Academy') {
      // Open card below the pin (down side)
      card.classList.add('card-below');
      card.classList.remove('card-left', 'card-right');
      card.style.bottom = 'auto';
      card.style.top = '45px';
      
      // Since it's centered, check if it needs horizontal shift
      const leftPercent = parseFloat(hotspot.style.left);
      let shiftX = 0;
      if (leftPercent < 20) {
        shiftX = 80;
      } else if (leftPercent > 80) {
        shiftX = -95;
      }
      card.style.setProperty('--shift-x', `${shiftX}px`);
      card.style.setProperty('--arrow-left', `${130 - shiftX}px`);
    } else {
      // Default behavior (above and centered)
      card.classList.remove('card-below', 'card-left', 'card-right');
      card.style.bottom = '45px';
      card.style.top = 'auto';
      card.style.left = '50%';
      
      const leftPercent = parseFloat(hotspot.style.left);
      let shiftX = 0;
      if (leftPercent < 20) {
        shiftX = 80;
      } else if (leftPercent > 80) {
        shiftX = -95;
      }
      card.style.setProperty('--shift-x', `${shiftX}px`);
      card.style.setProperty('--arrow-left', `${130 - shiftX}px`);
    }
  });
}
// Note: Soundtrack & Music player engine code has been outsourced to toolbox.js
