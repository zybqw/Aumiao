

!async function (){
    let _import = async function (t) {
        try {
            return (await import(t)).default;
        } catch {
            return require(t);
        }
    };
    let child_process = await _import('child_process');
    let exec = (t) => new Promise((resolve, reject) => {
        child_process.exec(t, (err, stdout, stderr) => {
            if (err) {
                console.log(err);
                process.exit(1);
            } else {
                resolve(stdout);
            }
        });
    });
    console.log('installing...');
    await exec('npm install');
    console.log('install success\n');

    console.log('installing tsc globally...');
    await exec('npm install -g typescript');
    console.log('install success\n');

    console.log('compiling...');
    await exec('npm run compile');
    console.log('compile success\n');

    console.log('\n\nwhat\'s next?\ntype in "node ./dist/index.js" and enjoy :)');
    process.exit();
}();

