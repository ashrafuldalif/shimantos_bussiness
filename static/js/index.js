document.addEventListener("DOMContentLoaded", () => {
  const gallery = document.getElementById("gallery");
  const tiles = Array.from(gallery.children);

  // Clone after and before
  tiles.forEach(tile => {
    gallery.appendChild(tile.cloneNode(true));
  });
  [...tiles].reverse().forEach(tile => {
    gallery.insertBefore(tile.cloneNode(true), gallery.firstChild);
  });

  const totalTiles = tiles.length;
  const tileWidth = tiles[0].offsetWidth + 10;
  const middlePosition = totalTiles * tileWidth;

  gallery.scrollLeft = middlePosition;

  // Loop fix
  gallery.addEventListener("scroll", () => {
    if (gallery.scrollLeft <= tileWidth) {
      gallery.scrollLeft += totalTiles * tileWidth;
    } else if (gallery.scrollLeft >= gallery.scrollWidth - gallery.offsetWidth - tileWidth) {
      gallery.scrollLeft -= totalTiles * tileWidth;
    }
  });

  // Drag/touch handling
  let isDown = false;
  let startX;
  let scrollLeftStart;

  gallery.addEventListener("mousedown", (e) => {
    isDown = true;
    startX = e.pageX;
    scrollLeftStart = gallery.scrollLeft;
  });
  gallery.addEventListener("mouseleave", () => isDown = false);
  gallery.addEventListener("mouseup", () => isDown = false);
  gallery.addEventListener("mousemove", (e) => {
    if (!isDown) return;
    e.preventDefault();
    const walk = (e.pageX - startX) * 2;
    gallery.scrollLeft = scrollLeftStart - walk;
  });

  gallery.addEventListener("touchstart", (e) => {
    isDown = true;
    startX = e.touches[0].pageX;
    scrollLeftStart = gallery.scrollLeft;
  });
  gallery.addEventListener("touchend", () => isDown = false);
  gallery.addEventListener("touchmove", (e) => {
    if (!isDown) return;
    const walk = (e.touches[0].pageX - startX) * 2;
    gallery.scrollLeft = scrollLeftStart - walk;
  });

  // ✅ Auto-scroll (smooth, slow, infinite)
  let autoScroll;
  function startAutoScroll() {
    autoScroll = setInterval(() => {
      if (!isDown) {
        gallery.scrollLeft += 0.5; // Speed control
      }
      if (gallery.scrollLeft >= gallery.scrollWidth - gallery.offsetWidth - tileWidth) {
        gallery.scrollLeft -= totalTiles * tileWidth;
      }
    }, 16); // ~60fps
  }

  function stopAutoScroll() {
    clearInterval(autoScroll);
  }

  gallery.addEventListener("mouseenter", stopAutoScroll);
  gallery.addEventListener("mouseleave", startAutoScroll);
  gallery.addEventListener("mousedown", stopAutoScroll);
  gallery.addEventListener("mouseup", startAutoScroll);
  gallery.addEventListener("touchstart", stopAutoScroll);
  gallery.addEventListener("touchend", startAutoScroll);

  startAutoScroll(); // ✅ Start auto-scroll
});
