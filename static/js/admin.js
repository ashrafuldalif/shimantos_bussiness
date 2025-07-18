function showSection(sectionId) {
  document.querySelectorAll('.section').forEach(sec => {
    sec.classList.remove('active');
  });
  document.getElementById(sectionId).classList.add('active');
}

function toggleForm() {
  const form = document.getElementById('product-form');
  form.style.display = form.style.display === 'none' ? 'block' : 'none';
}
function editProduct(btn) {
  const bar = btn.parentElement;
  const inputs = bar.querySelectorAll('input');
  const imgContainer = bar.querySelector('.image-thumbnails');

  const isEditing = btn.innerText === 'Edit';

  inputs.forEach(inp => inp.disabled = !isEditing);
  btn.innerText = isEditing ? 'Save' : 'Edit';

  if (isEditing) {
    // Swap image thumbnails with file input
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.multiple = true;
    fileInput.className = 'image-input';

    imgContainer.innerHTML = '';
    imgContainer.appendChild(fileInput);
  } else {
    const fileInput = bar.querySelector('.image-input');

    // Replace file input with new image thumbnails
    if (fileInput && fileInput.files.length > 0) {
      imgContainer.innerHTML = '';
      [...fileInput.files].slice(0, 10).forEach(file => {
        const img = document.createElement('img');
        img.src = URL.createObjectURL(file);
        imgContainer.appendChild(img);
      });
    }
  }
}


function deleteProduct(btn) {
  if (confirm("Are you sure you want to delete this product?")) {
    const bar = btn.parentElement;
    bar.remove();
  }
}

// Add product dynamically
document.getElementById('product-form').addEventListener('submit', function(e) {
  e.preventDefault();

  const inputs = e.target.querySelectorAll('input, select');
  const name = inputs[0].value;
  const size = inputs[1].value;
  const files = inputs[2].files;
  const colors = inputs[3].value;
  const price = inputs[4].value;
  const availability = inputs[5].value;

  const bar = document.createElement('div');
  bar.className = 'product-bar';

  bar.innerHTML = `
    <input type="text" value="${name}" disabled>
    <input type="text" value="${size}" disabled>
    <input type="text" value="${colors}" disabled>
    <input type="text" value="${availability}" disabled>
    <div class="image-thumbnails">
      ${[...files].slice(0, 10).map(file => `<img src="${URL.createObjectURL(file)}" alt="">`).join('')}
    </div>
    <input type="number" value="${price}" disabled>
    <button onclick="editProduct(this)">Edit</button>
    <button onclick="deleteProduct(this)">Delete</button>
  `;

  document.getElementById('product-list').appendChild(bar);
  e.target.reset();
  e.target.style.display = 'none';
});
