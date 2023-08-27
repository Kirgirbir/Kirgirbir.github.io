<!DOCTYPE html>
<html>
<head>
    <title>Data Table</title>
</head>
<body>

<form method="post">
    <select name="selected_tag">
 	<option value="еда" <?php if(isset($_POST['selected_tag']) && $_POST['selected_tag'] == 'еда') echo 'selected'; ?>>Еда</option>
        <option value="холодное оружие" <?php if(isset($_POST['selected_tag']) && $_POST['selected_tag'] == 'холодное оружие') echo 'selected'; ?>>Холодное оружие</option>
    </select>
    </select>
    <input type="submit" value="Filter">
</form>

<table border="1">
    <tr>
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