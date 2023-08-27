<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Калькулятор стоимости жилья</title>
    <style>
        .circle-container {
            width: 600px; /* Adjust the width for proper alignment */
            height: 300px;
            position: relative;
            display: flex;
            align-items: center;
        }

        .circle {
            position: absolute;
            border-radius: 50%;
            cursor: pointer;
        }

        .circle.green {
            background-color: green;
        }

        .circle.green-highlight {
            background-color: #004d00; /* Slightly darker green */
            transition: background-color 0.3s ease;
        }

        .circle.yellow {
            background-color: yellow;
        }

        .circle.yellow-highlight {
            background-color: #b3b300; /* Slightly darker yellow */
            transition: background-color 0.3s ease;
        }

        .circle.red {
            background-color: red;
        }

        .circle.red-highlight {
            background-color: #660000; /* Slightly darker red */
            transition: background-color 0.3s ease;
        }

        .square {
            position: absolute;
            width: 300px;
            height: 300px;
            background-color: darkblue;
            opacity: 0.5; /* Adjust the opacity to your preference */
            cursor: pointer;
        }

        .square-highlight {
            background-color: #000033; /* Slightly darker blue */
            transition: background-color 0.3s ease;
        }

        #circleText {
            margin-left: 20px;
            width: 300px;
        }

        #calculator {
            margin-left: 20px;
            width: 300px;
            display: flex;
            flex-direction: column;
        }
    </style>
</head>
<body>
    <h1>Выбери расположение дома! (цена только на готовое жильё)</h1>
    
    <div id="circleText"></div>

    <div class="circle-container">
        <div class="square" onclick="showCircleText('Самый дешёвый вариант жизни - вне города.'); setCoefficient(0.75);" onmouseover="highlightSquare(this)" onmouseout="removeSquareHighlight(this)"></div>

        <?php
        $radius = 50; // base radius value
        $radius2 = 2 * $radius;
        $radius3 = 3 * $radius;
        
        $center = $radius3; // Center of the shapes
        
        echo '<div class="circle green" style="width: ' . (2 * $radius3) . 'px; height: ' . (2 * $radius3) . 'px; top: 0; left: 0;" onclick="showCircleText(\'Внешний район, дешёвый вариант жизни в городе.\'); setCoefficient(0.95);" onmouseover="highlightCircle(this)" onmouseout="removeCircleHighlight(this)"></div>';
        echo '<div class="circle yellow" style="width: ' . (2 * $radius2) . 'px; height: ' . (2 * $radius2) . 'px; top: ' . ($center - $radius2) . 'px; left: ' . ($center - $radius2) . 'px;" onclick="showCircleText(\'Средний район - чуть дороже.\'); setCoefficient(1.5);" onmouseover="highlightCircle(this)" onmouseout="removeCircleHighlight(this)"></div>';
        echo '<div class="circle red" style="width: ' . (2 * $radius) . 'px; height: ' . (2 * $radius) . 'px; top: ' . ($center - $radius) . 'px; left: ' . ($center - $radius) . 'px;" onclick="showCircleText(\'Внутренний район - район элиты.\'); setCoefficient(3.5);" onmouseover="highlightCircle(this)" onmouseout="removeCircleHighlight(this)"></div>';
        ?>
    </div>

    <div id="calculator">
        <h2>Калькулятор цены</h2>
        <label for="inputValue">Введите значение: </label>
        <input type="number" id="inputValue" onchange="calculatePrice()" />
        <p id="outputValue">Цена: </p>
    </div>

    <script>
        let coefficient = 0;

        function showCircleText(text) {
            document.getElementById('circleText').textContent = text;
        }

        function highlightCircle(circle) {
            circle.classList.add(`${circle.classList[1]}-highlight`);
        }

        function removeCircleHighlight(circle) {
            circle.classList.remove(`${circle.classList[1]}-highlight`);
        }

        function highlightSquare(square) {
            square.classList.add('square-highlight');
        }

        function removeSquareHighlight(square) {
            square.classList.remove('square-highlight');
        }

        function setCoefficient(value) {
            coefficient = value;
            calculatePrice();
        }

        function calculatePrice() {
            const inputValue = parseFloat(document.getElementById('inputValue').value);
            const calculatedPrice = Math.round(inputValue * coefficient);
            document.getElementById('outputValue').textContent = `Цена: ${calculatedPrice}`;
        }
    </script>
</body>
</html>
