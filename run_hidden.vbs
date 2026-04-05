Set WshShell = CreateObject("WScript.Shell")
' Executa o arquivo .bat sem mostrar a janela do terminal (o parâmetro 0 oculta a janela)
WshShell.Run chr(34) & "run_app.bat" & Chr(34), 0
Set WshShell = Nothing
