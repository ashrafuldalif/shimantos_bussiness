document.addEventListener('DOMContentLoaded', function() {
    const gallery = document.getElementById('gallery');
    const tiles = gallery.querySelectorAll('.tile');
    
    // Clone all tiles for seamless looping
    tiles.forEach(tile => {
      gallery.appendChild(tile.cloneNode(true));
    });
    console.log("hello")
    let isScrolling = false;
    let scrollTimeout;
  
    gallery.addEventListener('scroll', function() {
      if (!isScrolling) {
        isScrolling = true;
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => isScrolling = false, 100);
      }
  
      // Check if we've scrolled to the cloned set
      if (gallery.scrollLeft >= gallery.scrollWidth / 2) {
        gallery.scrollLeft -= gallery.scrollWidth / 2;
      } 
      // Check if we're scrolling backwards to beginning
      else if (gallery.scrollLeft <= 0) {
        gallery.scrollLeft += gallery.scrollWidth / 2;
      }
    });
  
    // Enable momentum scrolling for touch devices
    let startX, scrollLeft, isDown;
    let velocity = 0;
    let animationFrame;
    let lastTime = 0;
  
    gallery.addEventListener('mousedown', (e) => {
      isDown = true;
      startX = e.pageX - gallery.offsetLeft;
      scrollLeft = gallery.scrollLeft;
      cancelAnimationFrame(animationFrame);
    });
  
    gallery.addEventListener('mouseleave', () => {
      isDown = false;
    });
  
    gallery.addEventListener('mouseup', () => {
      isDown = false;
      if (Math.abs(velocity) > 1) {
        momentumScroll();
      }
    });
    console.log("hello");
    gallery.addEventListener('mousemove', (e) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - gallery.offsetLeft;
      const walk = (x - startX) * 2;
      gallery.scrollLeft = scrollLeft - walk;
      velocity = walk;
    });
  
    function momentumScroll() {
      velocity *= 0.95;
      gallery.scrollLeft -= velocity;
      
      if (Math.abs(velocity) > 0.5) {
        animationFrame = requestAnimationFrame(momentumScroll);
      }
    }
  });