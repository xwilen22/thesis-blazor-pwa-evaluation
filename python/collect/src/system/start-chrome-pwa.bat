ECHO OFF
::ECHO
::   Message for user | Where chrome_proxy is located                         |                      | PWA Specific commands, check properties of generated shortcut for PWA
ECHO starting pwa... && cd C:/Program Files/Google/Chrome/Application/ && start chrome_proxy.exe --profile-directory=Default --app-id=%1
exit 0