import { CommandDefinition } from "./types/command.js"

const Commands: CommandDefinition[] = [
    {
        name: "hello",
        description: "Say hello",
        options: [
            {
                flags: "-n, --name <name>",
                description: "Your name",
                defaultValue: "World"
            }
        ]
    }
]

export default Commands;
