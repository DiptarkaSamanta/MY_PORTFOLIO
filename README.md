# 🏝️ Aethelgard — Sovereign Interactive Island Portfolio 🪄

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![CSS3](https://img.shields.io/badge/CSS3_Vanilla-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Python](https://img.shields.io/badge/Python_Server-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![NVIDIA Llama 3.1](https://img.shields.io/badge/NVIDIA_Llama_3.1-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://build.nvidia.com/)
[![Scanimation Studio](https://img.shields.io/badge/Scanimation_Studio-0EA5E9?style=for-the-badge&logo=render&logoColor=white)](https://scanimation.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> **Step into Aethelgard!** An immersive, glassmorphic interactive digital island portfolio created for Artificial Intelligence & Machine Learning Engineer **Diptarka Samanta**. Featuring dynamic time-of-day lighting, atmospheric weather particles, procedural Web Audio soundscapes, real-time barrier-grid optical kinegrams, an AI Mayor chatbot powered by NVIDIA Llama 3.1, and 9 interactive island sectors.

---

## ✨ Features Overview

- 🗺️ **Interactive Island Hotspots**: Navigate 9 custom island sectors with smooth glassmorphism UI, interactive hover cards, compass pointer navigation, and animated pin pulses.
- 🌆 **Dynamic Time-of-Day Engine**: Auto-synchronizing or manual lighting engine switching between **Dawn**, **Day**, **Dusk**, and **Night** with custom ambient map artwork.
- 🌧️ **Atmospheric Canvas Particles**: Real-time 2D Canvas weather system rendering **Rain**, **Snow**, **Thunderstorm**, **Fog**, **Cloudy**, and **Clear** weather over the map.
- 🤖 **Mayor AI Chatbot (NVIDIA Llama 3.1)**: Interactive digital island mayor powered by NVIDIA Llama 3.1 8B Instruct model with streaming token generation, collapsible reasoning accordions, and Markdown links.
- 🎞️ **Scanimation Live Studio**: Embedded optical kinegram barrier-grid demo featuring live HD video (`cheetahscanimation.mp4`), time scrubber controls, and direct launch link to [Scanimation Studio](https://scanimation.onrender.com).
- 🎵 **Neumorphic City Toolbox & Audio Synthesizer**: Floating dashboard with real-time analog/digital clock, calendar dropdown, chiptune soundtrack player, vinyl record animation, and audio visualizer.
- 💻 **Core Terminal CLI**: Interactive command-line terminal allowing visitors to inspect Diptarka's AI/ML skills, tech stack tools, system metrics, and dev workflow.

---

## 🗺️ Island Sectors & Landmarks

| Landmark | Sector Page | Description |
| :--- | :--- | :--- |
| 🔭 **Stellar Observatory** | [`observatory.html`](observatory.html) | Featured technical builds, AI/ML repositories, live demos (including Scanimation Studio), and system architectures. |
| 🎓 **Grand Academy** | [`academy.html`](academy.html) | Educational history, academic degrees, research certifications, and machine learning credentials. |
| ⌛ **Chronos Clock Tower** | [`clock_tower.html`](clock_tower.html) | Professional career timeline, work experience history, milestones, and engineering achievements. |
| 💻 **Core Terminal** | [`code_terminal.html`](code_terminal.html) | Interactive terminal shell analyzing programming languages, deep learning frameworks, and dev toolkits. |
| 🏰 **Home Manor** | [`home.html`](home.html) | Personal quarters of Diptarka Samanta featuring biography, core engineering values, goals, and downloadable resume. |
| 📚 **Grand Library** | [`library.html`](library.html) | Technical publications, research blog posts, book notes, and AI/NLP academic documentation. |
| 🎮 **Luna Park (Sandbox)** | [`playground.html`](playground.html) | Creative sandbox featuring the Scanimation Live Video Demo & Mayor AI Tic-Tac-Toe Challenge side-by-side. |
| 🏪 **Port Market** | [`social_market.html`](social_market.html) | Social network booth containing GitHub, LeetCode, and LinkedIn links plus an interactive messaging form. |
| ⚓ **Iron Wharf** | [`industry_port.html`](industry_port.html) | Engineering consultancy details, freelancing options, rate cards, and technical solutions packages. |

---

## 🎞️ Scanimation (Barrier-Grid Optical Illusion)

Aethelgard features an embedded live demo of **Scanimation** (Barrier-Grid Optical Kinegram) technology created by Diptarka Samanta.

- **Optical Physics**: Interlaces $N$ sequential animation frames into vertical column stripes and glides a transparent black-bar grating sheet horizontally over the print to reveal fluid continuous motion.
- **Live Demo App**: Try the full full-featured app at [https://scanimation.onrender.com](https://scanimation.onrender.com) (powered by Google Gemini AI, React 19, TypeScript, and Vite).

---

## 🛠️ Technical Architecture

| Layer | Technology |
| :--- | :--- |
| **Frontend Core** | HTML5, JavaScript (ES6+), Vanilla CSS (Custom Design System & HSL Tokens) |
| **Graphics & FX** | HTML5 Canvas 2D API, Glassmorphism Backdrop Blur, CSS Animations |
| **Audio Processing** | Web Audio API (procedural sine wave beep synthesis & visualizer bars) |
| **Backend Server** | Python 3 (`server.py` using multi-threaded `ThreadingHTTPServer`) |
| **AI LLM API** | NVIDIA Llama 3.1 8B Instruct (`meta/llama-3.1-8b-instruct`) with Server-Sent Events (SSE) streaming |
| **Video Assets** | Standard H.264 MP4 (`images/cheetahscanimation.mp4`) |

---

## 🚀 Quick Start & Running Locally

### Prerequisites
- [Python 3.x](https://www.python.org/) installed on your machine.
- Any modern web browser (Chrome, Edge, Firefox, Safari).

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/DiptarkaSamanta/MY_PORTFOLIO.git
   cd MY_PORTFOLIO
   ```

2. **Launch the Server**:
   - **On Windows**: Double-click `run_portfolio.bat` or run:
     ```cmd
     python server.py
     ```
   - **On macOS / Linux**:
     ```bash
     python3 server.py
     ```

3. **Open in Browser**:
   Open [http://localhost:8080](http://localhost:8080) to explore Aethelgard!

---

## 👤 Author

**Diptarka Samanta**  
*Artificial Intelligence & Machine Learning Engineer*

- 🌐 **Portfolio**: [Aethelgard Digital Island](http://localhost:8080)
- 🚀 **Featured App**: [Scanimation Studio](https://scanimation.onrender.com)
- 🐙 **GitHub**: [@DiptarkaSamanta](https://github.com/DiptarkaSamanta)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE) — see the [LICENSE](LICENSE) file for details.
