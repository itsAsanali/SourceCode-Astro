#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

const args = process.argv.slice(2);

if (args.length === 0 || args.includes('-h') || args.includes('--help')) {
  console.log("Astro Language CLI v1.0.0");
  console.log("Usage: astro <file.ast | file.astro> [-o output.js]");
  process.exit(0);
}

const cliPyPath = path.join(__dirname, 'cli.py');

const pythonProcess = spawn('python', [cliPyPath, ...args], {
  stdio: 'inherit'
});

pythonProcess.on('error', (err) => {
  console.error('Ошибка запуска Python:', err.message);
});

pythonProcess.on('exit', (code) => {
  process.exit(code);
});