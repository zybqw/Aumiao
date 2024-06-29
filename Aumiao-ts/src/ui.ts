import { App } from "./app.js";
import { FallTask, moduleLoader } from "./utils.js";
import chalk from "chalk";

enum Colors {
    Red = "#FF5733",
    Green = "#33FF57",
    Blue = "#3366FF",
    Yellow = "#FFFF33",
    Purple = "#FF33FF",
    Cyan = "#33FFFF",
    White = "#FFFFFF",
    Black = "#000000",
    Gray = "#808080",
    Navy = "#000080"
}

const inq = (function () {
    let _inq: any, _tableInput: any;
    return {
        async inquirer(): Promise<typeof import("inquirer").default> {
            if (!_inq) {
                _inq = (await moduleLoader(["inquirer"]))[0];
                if (!_tableInput) _tableInput = (await moduleLoader(["inquirer-table-input"]))[0];
                _inq.default.registerPrompt("table-input", _tableInput);
            }
            return _inq.default;
        },

        // @ts-ignore
        async TableInput(): Promise<typeof import("inquirer-table-input").default> {
            if (!_tableInput) {
                _tableInput = (await moduleLoader(["inquirer-table-input"]))[0];
            }
            return _tableInput;
        }
    }
})();

/**
 * Prompt for text input.
 * @param message - The message to display to the user.
 * @param prefix - Optional. Customize the prefix symbol in the prompt.
 * @returns The user's input.
 */
export async function input(message: string, prefix?: string, options?: import("inquirer").InputQuestionOptions): Promise<string> {
    const promptOptions = {
        type: "input",
        name: "answer",
        message,
        ...(prefix && { prefix }),
        ...(options && { options })
    };
    const { answer } = await (await inq.inquirer()).prompt(promptOptions as any);
    return answer;
}

/**
 * Prompt for a password input.
 * @param message - The message to display to the user.
 * @returns The user's input.
 */
export async function password(message: string, prefix?: string): Promise<string> {
    const { answer } = await (await inq.inquirer()).prompt({
        type: "password",
        name: "answer",
        message,
        mask: "*",
        ...(prefix && { prefix })
    });
    return answer;
}

/**
 * Prompt for a confirmation.
 * @param message - The message to display to the user.
 * @returns The user's confirmation.
 */
export async function confirm(message: string): Promise<boolean> {
    const { answer } = await (await inq.inquirer()).prompt({
        type: "confirm",
        name: "answer",
        message
    });
    return answer;
}

/**
 * Prompt for a single selection from a list.
 * @param message - The message to display to the user.
 * @param choices - The list of choices.
 * @returns The user's selection.
 */
export async function select(message: string, choices: string[]): Promise<string> {
    const { answer } = await (await inq.inquirer()).prompt({
        type: "list",
        name: "answer",
        message,
        choices
    });
    return answer;
}

/**
 * Prompt for a single selection from a list of objects.
 * @param message - The message to display to the user.
 * @param choiceObj - The list of choices.
 * @returns The result of the selected value.
 * @example selectByObject("Select a color", { "Red": Colors.Red, "Green": Colors.Green });
 */
export async function selectByObject(message: string, choiceObj: { [key: string]: any }): Promise<any> {
    const { answer } = await (await inq.inquirer()).prompt({
        type: "list",
        name: "answer",
        message,
        choices: Object.keys(choiceObj)
    });
    return choiceObj[answer];
}

/**
 * Prompt for multiple selections from a list.
 * @param message - The message to display to the user.
 * @param choices - The list of choices.
 * @returns The user's selections.
 */
export async function checkbox(message: string, choices: string[]): Promise<string[]> {
    const { answer } = await (await inq.inquirer()).prompt({
        type: "checkbox",
        name: "answer",
        message,
        choices
    });
    return answer;
}

export async function tableInput<T extends any[]>(
    name: string,
    message: string,
    headers: {
        name: string,
        value: string,
        editable: "number" | "text" | "decimal"
    }[],
    rows: T[],
    options?: Record<string, any>
): Promise<{
    [key: string]: {
        state: boolean
        result: Record<string, unknown>[]
    }
}> {
    return (await inq.inquirer()).prompt([
        {
            type: "table-input",
            name,
            message,
            infoMessage: `Navigate and Edit`,
            hideInfoWhenKeyPressed: true,
            freezeColumns: 1,
            decimalPoint: ".",
            decimalPlaces: 2,
            selectedColor: chalk.yellow,
            editableColor: chalk.bgYellow.bold,
            editingColor: chalk.bgGreen.bold,
            columns: headers,
            rows,
            validate: () => false,
            ...(options && { options })
        }
    ])
}

export async function paginate<T extends {
    preview: string;
    content: string;
}>(
    app: App,
    provider: (page: number) => Promise<T[]> | T[],
    pageSize: number,
    options?: import("inquirer").InputQuestionOptions
) {
    const inquirer: typeof import("inquirer").default = await inq.inquirer();

    async function showContent(item: T) {
        const { answer } = await inquirer.prompt({
            type: "list",
            name: "answer",
            message: item.content,
            choices: [new inquirer.Separator(), "返回", "结束"],
            prefix: "📄",
        });
        return answer;
    }

    let items: T[] = [], page = 0, exited = false;
    let fall = new FallTask(app);
    while (!exited) {
        if (items.length / pageSize <= page) {
            const newItems = await fall.waitForLoading<T[]>(async (resolve, reject) => {
                const newItems = await provider(page);
                resolve("");
                return newItems;
            }, "加载中");
            items = items.slice(0, page * pageSize).concat(newItems);
        }
        const { answer } = await inquirer.prompt({
            type: "list",
            name: "answer",
            message: `第 ${page + 1} 页`,
            choices: [
                ...items.slice(page * pageSize, (page + 1) * pageSize).map(item => item.preview),
                new inquirer.Separator(),
                ...[
                    page > 0 ? "上一页" : "",
                    "下一页"
                ].filter(Boolean),
            ],
            ...(options && { options })
        });
        if (answer === "上一页") {
            page--;
        } else if (answer === "下一页") {
            page++;
        } else {
            const item = items.find(item => item.preview === answer)!;
            const result = await showContent(item);
            if (result === "返回") {
                continue;
            } else if (result === "结束") {
                exited = true;
            }
        }
    }
}

export function hex(color: string) {
    return chalk.hex(color);
}

export async function separator() {
    return new (await inq.inquirer()).Separator();
}

export const color = {
    red: (v: string) => chalk.hex(Colors.Red)(v),
    green: (v: string) => chalk.hex(Colors.Green)(v),
    blue: (v: string) => chalk.hex(Colors.Blue)(v),
    yellow: (v: string) => chalk.hex(Colors.Yellow)(v),
    purple: (v: string) => chalk.hex(Colors.Purple)(v),
    cyan: (v: string) => chalk.hex(Colors.Cyan)(v),
    white: (v: string) => chalk.hex(Colors.White)(v),
    black: (v: string) => chalk.hex(Colors.Black)(v),
    gray: (v: string) => chalk.hex(Colors.Gray)(v),
    navy: (v: string) => chalk.hex(Colors.Navy)(v)
}

export default {
    input,
    password,
    confirm,
    select,
    selectByObject,
    checkbox,
    hex,
    separator,
    Colors,
    color
};

export {
    Colors
}
