module.exports = {
    env: {
        node: true,
        es2023: true,
        browser: true
    },
    extends: "eslint:recommended",
    overrides: [
        {
            env: {
                node: true
            },
            files: [
                ".eslintrc.{js,cjs}"
            ],
            parserOptions: {
                sourceType: "script"
            }
        }
    ],
    rules: {
        indent: [
            "error",
            4
        ],
        "linebreak-style": [
            "error",
            "windows"
        ],
        quotes: [
            "error",
            "double"
        ],
        semi: [
            "error",
            "always"
        ]
    },
    parser: "@babel/eslint-parser",
    parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        requireConfigFile: false,
        babelOptions: {
            plugins: [
                "@babel/plugin-syntax-import-assertions"
            ]
        }
    }
};
