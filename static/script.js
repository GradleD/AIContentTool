document.addEventListener('DOMContentLoaded', function () {
    const contentForm = document.getElementById('contentForm');
    const loader = document.getElementById('loader');
    const submitButton = document.getElementById('submitButton');

    contentForm.addEventListener('submit', function () {
        loader.style.display = 'block';
        submitButton.disabled = true;
    });
});
