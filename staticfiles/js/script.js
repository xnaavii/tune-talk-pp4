setTimeout(function() {
    document.querySelectorAll('.alert').forEach(alert => {
        alert.classList.add('fade');
        alert.classList.add('show');
        setTimeout(function() {
            alert.remove(); // Remove the alert from DOM
        }, 3000); // Adjust this timeout as needed for fade duration
    });
}, 1500);