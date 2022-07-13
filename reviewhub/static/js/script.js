// form input
$(document).ready(function () {
  $('select').formSelect();
});

document.addEventListener('DOMContentLoaded', hideModal);

// Global variables
let modalDisplay = document.querySelector('.modal-container'); // outer modal container
let confirmDelete = document.querySelector('.confirm-delete'); // delete button

// hide modal on start up
function hideModal() {
  modalDisplay.classList.add('hide');
}

// event listener to trigger modal once delete is clicked
confirmDelete.addEventListener('click', showModal);

function showModal() {
  if (modalDisplay.classList.contains('hide')) {
    modalDisplay.classList.remove('hide');
  }
}