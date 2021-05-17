ECHO OFF
::ECHO
if exist package.json (
    ECHO Building node package && npm install && npm run build && serve -s build
) else (
    ECHO No package.json found! Place this bat in project folder.
)
PAUSE