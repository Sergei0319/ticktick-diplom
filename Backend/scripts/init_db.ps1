# Пересоздание БД TickTick через Docker (PostgreSQL + schema + Alembic)
# Из корня диплома: powershell -File Backend\scripts\init_db.ps1

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $root

Write-Host "Останавливаем контейнеры и удаляем volume БД (все данные сотрутся)..."
docker compose -p ticktick down -v

Write-Host "Собираем и поднимаем db + api..."
docker compose -p ticktick up -d --build db api

Write-Host "Ждём готовности PostgreSQL..."
$ok = $false
foreach ($i in 1..30) {
    Start-Sleep -Seconds 2
    docker compose -p ticktick exec -T db pg_isready -U ticktick_user -d ticktick_db 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { $ok = $true; break }
}
if (-not $ok) {
    Write-Error "PostgreSQL не поднялся. Смотри: docker compose logs db"
}

Write-Host "Таблицы в ticktick_db:"
docker compose -p ticktick exec -T db psql -U ticktick_user -d ticktick_db -c "\dt"

Write-Host ""
Write-Host "Готово. API: http://localhost:8000/docs"
Write-Host "Локально: Backend\.env указывает на localhost:5432"