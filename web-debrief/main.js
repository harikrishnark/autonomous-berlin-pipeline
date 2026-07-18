import './style.css'

// Glitch typing effect for the header
document.addEventListener('DOMContentLoaded', () => {
  const title = document.querySelector('h1');
  const originalText = title.getAttribute('data-text');
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*';
  
  let iterations = 0;
  
  const interval = setInterval(() => {
    title.innerText = title.innerText.split('')
      .map((letter, index) => {
        if(index < iterations) {
          return originalText[index];
        }
        return characters[Math.floor(Math.random() * 42)];
      })
      .join('');
    
    if(iterations >= originalText.length) {
      clearInterval(interval);
    }
    
    iterations += 1 / 3;
  }, 30);
});
