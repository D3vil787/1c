# Вызов экспортной функции общего модуля тестовой сборки по COM; результат пишется в файл.
# Запускать 32-разрядным PowerShell, если платформа 32-разрядная:
#   %SystemRoot%\SysWOW64\WindowsPowerShell\v1.0\powershell.exe -NoProfile -ExecutionPolicy Bypass -File com_call.ps1 -BaseDir D:\work\test_base -Module СкладПланшетТест -Function ТестКомплект -Out result.txt
# Логин/пароль: переменные окружения IBUSER / IBPWD. Файл сохранять в UTF-8 с BOM.
param(
  [string]$BaseDir = "test_base",
  [string]$Module = "СкладПланшетТест",
  [string]$Function = "Тест",
  [string]$Out = "com_result.txt"
)
$bf = [System.Reflection.BindingFlags]
$res = ""
try {
  $t = [Type]::GetTypeFromProgID("V83.COMConnector")
  $c = [Activator]::CreateInstance($t)
  $cs = "File=""$BaseDir"";Usr=""$($env:IBUSER)"";Pwd=""$($env:IBPWD)"""
  $conn = $t.InvokeMember("Connect", $bf::InvokeMethod, $null, $c, @($cs))
  $mt = $conn.GetType().InvokeMember($Module, $bf::GetProperty, $null, $conn, $null)
  $res = [string]$mt.GetType().InvokeMember($Function, $bf::InvokeMethod, $null, $mt, $null)
  [System.IO.File]::WriteAllText($Out, $res, (New-Object System.Text.UTF8Encoding($true)))
} catch {
  [System.IO.File]::WriteAllText($Out, $res + "`r`nERROR: " + $_.Exception.ToString(), (New-Object System.Text.UTF8Encoding($true)))
}
