<?php

// Check if the request method is POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Retrieve the values of x and y from the POST data
    $x = isset($_POST['x']) ? $_POST['x'] : 0;
    $y = isset($_POST['y']) ? $_POST['y'] : 0;

    // Calculate the sum of x and y
    $z = $x + $y;

    // Display the result
    echo "$x + $y = $z";

    // Return the sum as a JSON response
    echo json_encode(['result' => $z]);
} else {
    // Return an error response for unsupported request methods
    http_response_code(405);
    echo 'Method Not Allowed';
}

?>
