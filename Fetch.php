<?php
$servername = "den1.mysql5.gear.host";
$username = "plantdata1";
$password = "Of5uUh~77i4?";
$dbname = "plantdata1";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT * FROM   plantdata1.plaeddit_data ORDER  BY dateofcare DESC LIMIT  1;";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<h2>Most Recent Results: </h2><br>"
        . "<p id='temperature'>Temperature: " . $row["temperature"] . "</p><br>"
        . "<p id='humidity'>Humidity: " . $row["humidity"] . "</p><br>"
        . "<p id='moisture'>Moisture: " . $row["moisture"] . "</p><br>"
        . "<p id='time'>Time: " . $row["dateofcare"] . "</p><br>";
    }
} else {
    echo "0 results";
}
$conn->close();
?>
