<?php
$domain = '{{ domain }}';
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo htmlspecialchars($domain); ?> aktif</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1f2937, #111827);
            color: #f9fafb;
            min-height: 100vh;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .card {
            max-width: 760px;
            margin: 24px;
            padding: 40px;
            border-radius: 22px;
            background: rgba(17, 24, 39, 0.94);
            box-shadow: 0 18px 45px rgba(0,0,0,.32);
        }
        .badge {
            display: inline-block;
            padding: 8px 14px;
            border-radius: 999px;
            background: #2563eb;
            color: white;
            font-weight: bold;
            margin-bottom: 18px;
        }
        h1 { font-size: 2.2rem; margin: 0 0 12px; }
        p { line-height: 1.7; color: #d1d5db; }
        code {
            background: #0b1220;
            padding: 2px 8px;
            border-radius: 8px;
            color: #93c5fd;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="badge">Website PHP Aktif</div>
        <h1><?php echo htmlspecialchars($domain); ?> telah aktif</h1>
        <p>Website PHP untuk domain <code><?php echo htmlspecialchars($domain); ?></code> sudah aktif di VPS ini.</p>
        <p>Halaman ini dibuat otomatis oleh <strong>VPS Website Manager</strong>. Silakan ganti file <code>index.php</code> dengan project kamu.</p>
        <p>Waktu server: <strong><?php echo date('Y-m-d H:i:s'); ?></strong></p>
    </div>
</body>
</html>
