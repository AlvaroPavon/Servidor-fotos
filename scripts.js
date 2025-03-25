let multiSelectActive = false;

function openModal(src) {
  if (!multiSelectActive) {
    document.getElementById('myModal').style.display = "block";
    document.getElementById('modalImage').src = src;
    document.getElementById('modalImage').style.maxHeight = "80vh";
    document.getElementById('downloadLink').href = src;
  }
}

function closeModal() {
  document.getElementById('myModal').style.display = "none";
}

function toggleSelect(img) {
  img.classList.toggle('selected');
  updateCounter();
}

function downloadSelected() {
  const selectedImages = document.querySelectorAll('.gallery img.selected');
  selectedImages.forEach(img => {
    const link = document.createElement('a');
    link.href = img.src;
    link.download = img.alt;
    link.click();
  });
}

function toggleMultiSelect() {
  multiSelectActive = !multiSelectActive;
  document.querySelector('.multi-select-btn').textContent = multiSelectActive ?
    'Desactivar Selección Múltiple' : 'Activar Selección Múltiple';
  document.querySelectorAll('.gallery img').forEach(img => {
    img.onclick = multiSelectActive ? () => toggleSelect(img) : () => openModal(img.src);
  });
  document.querySelector('.counter').style.display = multiSelectActive ? 'flex' : 'none';
  if (!multiSelectActive) {
    document.querySelectorAll('.gallery img.selected').forEach(img => img.classList.remove('selected'));
  }
  updateCounter();
}

function updateCounter() {
  const count = document.querySelectorAll('.gallery img.selected').length;
  document.querySelector('.counter .counter-number').textContent = count;
  const selectBtn = document.querySelector('.counter .select-btn');
  if (multiSelectActive) {
    if (!selectBtn) {
      const btn = document.createElement('button');
      btn.className = 'select-btn';
      btn.textContent = '⬇️';
      btn.onclick = downloadSelected;
      document.querySelector('.counter').appendChild(btn);
    }
  } else if (selectBtn) {
    selectBtn.remove();
  }
}

document.addEventListener('contextmenu', event => event.preventDefault());
