import inquirer from "inquirer";
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

/**
 * Prompt for text input.
 * @param message - The message to display to the user.
 * @returns The user's input.
 */
export async function input(message: string): Promise<string> {
    const { answer } = await inquirer.prompt({
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
    const { answer } = await inquirer.prompt({
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
    const { answer } = await inquirer.prompt({
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
    const { answer } = await inquirer.prompt({
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
    const { answer } = await inquirer.prompt({
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
    const { answer } = await inquirer.prompt({
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

export function separator() {
    return new inquirer.Separator();
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
