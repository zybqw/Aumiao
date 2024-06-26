import { moduleLoader } from "./utils.js";
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

const inq = (function (){
    let _inq: any;
    return {
        async inquirer() {
            if (!_inq) {
                _inq = (await moduleLoader(["inquirer"]))[0];
            }
            return _inq.default;
        },
    }
})();

/**
 * Prompt for text input.
 * @param message - The message to display to the user.
 * @param prefix - Optional. Customize the prefix symbol in the prompt.
 * @returns The user's input.
 */
export async function input(message: string, prefix?: string): Promise<string> {
    const promptOptions = {
        type: "input",
        name: "answer",
        message,
        ...(prefix && { prefix }),
    };
    const { answer } = await (await inq.inquirer()).prompt(promptOptions);
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
