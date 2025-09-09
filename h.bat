@echo off
REM Install Node.js dependencies for Vite-React-TypeScript-Tailwind starter
REM Ensure Node.js is installed before running

REM Init npm if node_modules missing
IF NOT EXIST "package-lock.json" (
    npm init -y
)

REM Install all libraries from package.json
npm install

REM Optional: Install VS Code extensions for best experience
REM For ESLint extension
code --install-extension dbaeumer.vscode-eslint
REM For Tailwind CSS IntelliSense
code --install-extension bradlc.vscode-tailwindcss
REM For Prettier extension
code --install-extension esbenp.prettier-vscode
REM For React TypeScript snippets
code --install-extension ms-vscode.vscode-typescript-next

REM Done
echo Project setup complete! You can start coding in VS Code now.
pause
