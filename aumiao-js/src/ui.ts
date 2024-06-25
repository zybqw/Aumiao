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
    let _inq: any, _chalk: any;
    return {
        async inquirer() {
            if (!_inq) {
                _inq = await moduleLoader(["inquirer"]);
            }
            return _inq;
        },
    }
})();

/**
 * Prompt for text input.
 * @param message - The message to display to the user.
 * @returns The user's input.
 */
export async function input(message: string): Promise<string> {
    const { answer } = await (await inq.inquirer()).prompt({
        type: "input",
        name: "answer",
        message
    });
    return answer;
}

/**
 * Prompt for a password input.
 * @param message - The message to display to the user.
 * @returns The user's input.
 */
export async function password(message: string): Promise<string> {
    const { answer } = await (await inq.inquirer()).prompt({
        type: "password",
        name: "answer",
        message,
        mask: "*"
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
 * @returns The result of the selected function.
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

export default {
    input,
    password,
    confirm,
    select,
    selectByObject,
    checkbox,
    hex,
    separator,
    Colors
};

export {
    Colors
}
