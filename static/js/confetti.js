const button = document.querySelector('#button');
const canvas = document.querySelector('#confetti');

const jsConfetti = new JSConfetti();

button.addEventListener('click', () => {
    jsConfetti.addConfetti().then(() => jsConfetti.addConfetti())

    setTimeout(() => {
      window.location.href = "http://127.0.0.1:5500/Abacus-Website/index.html"; // Replace with your target URL
    }, 5600);
})