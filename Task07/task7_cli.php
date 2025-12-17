#!/usr/bin/env php
<?php
// Проверяем существование файла базы данных
if (!file_exists('university.db')) {
    die("Ошибка: Файл базы данных 'university.db' не найден.\n" .
        "Сначала выполните: sqlite3 university.db < create_database.sql\n");
}

// Подключаемся к базе данных
try {
    $db = new PDO('sqlite:university.db');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Ошибка подключения к базе данных: " . $e->getMessage() . "\n");
}

// Получаем текущий год
$currentYear = date('Y');

// Получаем все действующие группы
try {
    $stmt = $db->prepare("
        SELECT DISTINCT number 
        FROM groups 
        WHERE graduation_year >= :year 
        ORDER BY number
    ");
    $stmt->execute([':year' => $currentYear]);
    $groups = $stmt->fetchAll(PDO::FETCH_COLUMN);
} catch (PDOException $e) {
    die("Ошибка при получении групп: " . $e->getMessage() . "\n");
}

// Вывод заголовка
echo "================================================\n";
echo "             СПИСОК СТУДЕНТОВ\n";
echo "================================================\n\n";

// Если нет групп
if (empty($groups)) {
    echo "Нет действующих групп.\n";
    exit(0);
}

// Показываем доступные группы
echo "ДОСТУПНЫЕ ГРУППЫ: " . implode(', ', $groups) . "\n\n";

// Запрашиваем ввод
echo "Введите номер группы или нажмите Enter для всех групп: ";
$input = trim(fgets(STDIN));

// Проверка ввода
$selectedGroup = null;
if ($input !== '') {
    if (!is_numeric($input)) {
        echo "Ошибка: номер группы должен быть числом!\n";
        exit(1);
    }
    
    $groupNumber = (int)$input;
    if (!in_array($groupNumber, $groups)) {
        echo "Ошибка: группы №{$groupNumber} не существует!\n";
        exit(1);
    }
    $selectedGroup = $groupNumber;
}

// Получаем студентов
try {
    $sql = "
        SELECT 
            g.number as group_number,
            g.direction as direction,
            s.last_name || ' ' || s.first_name || ' ' || COALESCE(s.middle_name, '') as full_name,
            s.gender,
            s.birth_date,
            s.student_id
        FROM students s
        JOIN groups g ON s.group_id = g.id
        WHERE g.graduation_year >= :year
    ";
    
    $params = [':year' => $currentYear];
    
    if ($selectedGroup !== null) {
        $sql .= " AND g.number = :group";
        $params[':group'] = $selectedGroup;
    }
    
    $sql .= " ORDER BY g.number, s.last_name, s.first_name";
    
    $stmt = $db->prepare($sql);
    $stmt->execute($params);
    $students = $stmt->fetchAll();
} catch (PDOException $e) {
    die("Ошибка при получении студентов: " . $e->getMessage() . "\n");
}

// Если нет студентов
if (empty($students)) {
    echo "\nСтудентов не найдено.\n";
    exit(0);
}

// Выводим таблицу с псевдографикой
echo "\n";
drawTable($students);

/**
 * Рисует таблицу с псевдографикой
 */
function drawTable($students) {
    // Определяем максимальные ширины для каждой колонки
    $maxGroup = 6;
    $maxDirection = 8;
    $maxName = 4;
    
    foreach ($students as $student) {
        $maxGroup = max($maxGroup, strlen($student['group_number']));
        $maxDirection = max($maxDirection, mb_strlen($student['direction']));
        $maxName = max($maxName, mb_strlen($student['full_name']));
    }
    
    // Добавляем отступы
    $colGroup = $maxGroup + 2;
    $colDirection = $maxDirection + 2;
    $colName = $maxName + 2;
    $colGender = 8;
    $colBirth = 14;
    $colStudentId = 17;
    
    // Верхняя граница
    echo "+" . str_repeat('-', $colGroup) . 
         "+" . str_repeat('-', $colDirection) . 
         "+" . str_repeat('-', $colName) . 
         "+" . str_repeat('-', $colGender) . 
         "+" . str_repeat('-', $colBirth) . 
         "+" . str_repeat('-', $colStudentId) . "+\n";
    
    // Заголовок таблицы
    printf("| %-{$maxGroup}s | %-{$maxDirection}s | %-{$maxName}s | %-6s | %-12s | %-15s |\n",
        "Группа", "Направление", "ФИО", "Пол", "Дата рожд.", "№ билета");
    
    // Разделитель
    echo "+" . str_repeat('-', $colGroup) . 
         "+" . str_repeat('-', $colDirection) . 
         "+" . str_repeat('-', $colName) . 
         "+" . str_repeat('-', $colGender) . 
         "+" . str_repeat('-', $colBirth) . 
         "+" . str_repeat('-', $colStudentId) . "+\n";
    
    // Данные студентов
    foreach ($students as $student) {
        $birthDate = date('d.m.Y', strtotime($student['birth_date']));
        
        printf("| %-{$maxGroup}s | %-{$maxDirection}s | %-{$maxName}s | %-6s | %-12s | %-15s |\n",
            $student['group_number'],
            mb_strimwidth($student['direction'], 0, $maxDirection, '...'),
            mb_strimwidth($student['full_name'], 0, $maxName, '...'),
            $student['gender'],
            $birthDate,
            $student['student_id']);
    }
    
    // Нижняя граница
    echo "+" . str_repeat('-', $colGroup) . 
         "+" . str_repeat('-', $colDirection) . 
         "+" . str_repeat('-', $colName) . 
         "+" . str_repeat('-', $colGender) . 
         "+" . str_repeat('-', $colBirth) . 
         "+" . str_repeat('-', $colStudentId) . "+\n";
    
    // Итог
    echo "\nВсего студентов: " . count($students) . "\n";
}