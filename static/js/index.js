document.addEventListener("DOMContentLoaded", () => {
  const gallery = document.getElementById("gallery");
  const tiles = Array.from(gallery.children);

  // Clone after (normal order)
  tiles.forEach((tile) => {
    gallery.appendChild(tile.cloneNode(true));
  });

  // Clone before (reverse order)
  [...tiles].reverse().forEach((tile) => {
    gallery.insertBefore(tile.cloneNode(true), gallery.firstChild);
  });

  const totalTiles = tiles.length;
  const tileWidth = tiles[0].offsetWidth + 10;
  const middlePosition = totalTiles * tileWidth;

  gallery.scrollLeft = middlePosition;

  // Reset if too far left or right
  gallery.addEventListener("scroll", () => {
    if (gallery.scrollLeft <= tileWidth) {
      gallery.scrollLeft += totalTiles * tileWidth;
    } else if (
      gallery.scrollLeft >=
      gallery.scrollWidth - gallery.offsetWidth - tileWidth
    ) {
      gallery.scrollLeft -= totalTiles * tileWidth;
    }
  });

  // Drag and touch support (same as before)
  let isDown = false;
  let startX;
  let scrollLeftStart;

  gallery.addEventListener("mousedown", (e) => {
    isDown = true;
    startX = e.pageX;
    scrollLeftStart = gallery.scrollLeft;
  });
  gallery.addEventListener("mouseleave", () => (isDown = false));
  gallery.addEventListener("mouseup", () => (isDown = false));
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
  gallery.addEventListener("touchend", () => (isDown = false));
  gallery.addEventListener("touchmove", (e) => {
    if (!isDown) return;
    const walk = (e.touches[0].pageX - startX) * 2;
    gallery.scrollLeft = scrollLeftStart - walk;
  });
});

function toggleCart() {
  const cart = document.getElementById("myCart");
  cart.classList.toggle("open");
  document.body.classList.toggle("DScroll");
}

// Open cart when clicking the cart button
const cartBtn = document.getElementById("cartBtn");
cartBtn.addEventListener("click", toggleCart);

// Close cart when clicking outside OR on CloseCart button
document.addEventListener("click", function (event) {
  const cart = document.getElementById("myCart");
  const closeCart = document.getElementById("CloseCart");

  const isClickInsideCart = cart.contains(event.target);
  const isClickOnCartBtn =
    event.target === cartBtn || cartBtn.contains(event.target);
  const isClickOnCloseBtn =
    closeCart &&
    (event.target === closeCart || closeCart.contains(event.target));

  if ((!isClickInsideCart && !isClickOnCartBtn) || isClickOnCloseBtn) {
    if (cart.classList.contains("open")) {
      toggleCart(); // Close cart
    }
  }
});
const navItems = document.querySelectorAll(".nav_items");

navItems.forEach((item) => {
  item.addEventListener("click", (e) => {
    navItems.forEach((i) => i.classList.remove("select")); // remove from all
    e.currentTarget.classList.add("select"); // add to clicked
  });
});






document.addEventListener('DOMContentLoaded', function() {
  const nav = document.querySelector('.smart-nav');
  let lastScroll = 0;
  let startY;
  
  // Show nav by default at page top
  if (window.scrollY <= 10) {
    nav.classList.add('visible');
  }
  
  // Rest of your existing code...
  document.addEventListener('touchstart', function(e) {
    startY = e.touches[0].clientY;
  });
  
  document.addEventListener('touchmove', function(e) {
    const currentY = e.touches[0].clientY;
    const deltaY = startY - currentY;
    
    if (deltaY > 5 && window.scrollY > 10) {
      nav.classList.add('visible');
    }
  });
  
  window.addEventListener('scroll', function() {
    const currentScroll = window.scrollY;
    
    // Always show when at very top
    if (currentScroll <= 10) {
      nav.classList.add('visible');
    }
    // Rest of existing scroll logic
    else if (currentScroll > lastScroll && currentScroll > 50) {
      nav.classList.remove('visible');
    }
    else if (currentScroll < lastScroll) {
      nav.classList.add('visible');
    }
    
    lastScroll = currentScroll;
  });
});


function updateCartCount(count) {
  const badge = document.querySelector('.cart-badge');
  badge.textContent = count;
  badge.style.display = count > 0 ? 'flex' : 'none'; // Hide if count is 0
}
