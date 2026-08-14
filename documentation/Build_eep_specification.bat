@echo off

echo Building EEP Specification...

pandoc EEP_Specification_v1.2.md ^
  --pdf-engine=xelatex ^
  -o EEP_Specification_v1.2.pdf

if errorlevel 1 (
    echo.
    echo Build FAILED.
    pause
    exit /b 1
)

pandoc EEP_Specification_v1.2.md ^
  -o EEP_Specification_v1.2.docx

echo.
echo Build completed successfully.