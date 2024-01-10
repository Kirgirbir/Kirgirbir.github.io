<!DOCTYPE html>
<html>
<head>
    <title>Цена вещей!</title>
    <style>
        th, td {
            padding: 8px;
        }
    </style>
</head>
<body>

<?php
$showId = isset($_COOKIE['show_id']) ? $_COOKIE['show_id'] === '1' : true;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['toggle_id'])) {
        $showId = !$showId;
        setcookie('show_id', $showId ? '1' : '0', time() + 3600, '/');
    }
}
?>

<form method="post">
    <select name="selected_tag">
        <?php
        $db = new SQLite3('data.db');
        $query = "SELECT DISTINCT tag FROM Prices";
        $result = $db->query($query);

        while ($row = $result->fetchArray()) {
            $tag = $row['tag'];
            echo "<option value=\"$tag\"";
            if (isset($_POST['selected_tag']) && $_POST['selected_tag'] == $tag) {
                echo ' selected';
            }
            echo ">$tag</option>";
        }

        $db->close();
        ?>
    </select>
    <input type="submit" value="Filter">
</form>

<form method="post" style="margin-top: 10px;">
    <input type="hidden" name="toggle_id" value="1">
    <input type="submit" value="<?php echo $showId ? 'Hide' : 'Show'; ?> ID">
</form>

<table border="1">
    <tr>
        <?php
        echo "<th" . ($showId ? '' : ' style="display: none;"') . ">ID</th>";
        ?>
        <th>Товар</th>
        <th>Описание</th>
        <th>Цена</th>
    </tr>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $selectedTag = $_POST["selected_tag"];
        $db = new SQLite3('data.db');
        $query = "SELECT * FROM Prices WHERE tag = '$selectedTag'";
        $result = $db->query($query);

        while ($row = $result->fetchArray()) {
            echo "<tr>";
            if ($showId) {
                echo "<td>" . $row['id'] . "</td>";
            }
            echo "<td>" . $row['product'] . "</td>";
            echo "<td>" . $row['description'] . "</td>";
            echo "<td>" . $row['price'] . "</td>";
            echo "</tr>";
        }
        $db->close();
    }
    ?>
</table>
</body>
</html>
