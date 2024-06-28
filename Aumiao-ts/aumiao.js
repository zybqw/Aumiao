#!/usr/bin/env node

import fs, { constants } from "fs/promises";
import { spawn } from "child_process";

!async function () {
  try {
    await fs.access('./dist/index.js', constants.R_OK | constants.W_OK);
  } catch (error) {
    await new Promise((resolve, reject) => {
      let install = spawn('node', ['./dist/index.js'], { shell: true, stdio: 'inherit' });
      install.on("close", (code) => {
        if (code === 0) {
          resolve();
        } else {
          reject();
        }
      });
    });
  }
  const args = process.argv.slice(2);
  const child = spawn('node', ['./dist/index.js', ...args], { shell: true, stdio: 'inherit' });
  child.on("close", (code) => {
    process.exit(code);
  });
}();
