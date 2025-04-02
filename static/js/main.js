// Basic goods tracking functionality
function deleteGood(index) {
    if (confirm('Are you sure you want to delete this item?')) {
        fetch('/delete/' + index, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if (response.ok) {
                window.location.reload();
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    }
}
