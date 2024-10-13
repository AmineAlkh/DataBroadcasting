const socket = io();

// Event listener for errors
socket.on('error', function(data) {
    // To show error message!
    const message = document.createElement('div');
    message.textContent = JSON.stringify(data.message);
    const errors = document.getElementById('errors');
    // First clear the previous errors
    errors.replaceChildren();
    errors.append(message)
});


// Event listener for new arrays
socket.on('new_array', function(data) {
    // To insert new array at the beginning of list
    const pre = document.createElement('pre');
    pre.textContent = JSON.stringify(data.array);
    const div = document.getElementById('generated_arrays');
    div.prepend(pre);

    // Clear the previous errors
    const errors = document.getElementById('errors');
    errors.replaceChildren();
});



// Function to generate new array
function generateArray() {
    const size = document.getElementById('size').value || 10000;
    // Handle negative array size
    if (size <= 0) {            
        alert('Invalid input. Array size must be positive');
        return;
    }
    // TO DO: alphabetical size input passes as 10000 because of input type!
    // ADD: error handler
    socket.emit('generate_array', { size: size });
}
