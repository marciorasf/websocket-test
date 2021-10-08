export type Message = {
  stream: string
  content: number
  timestamp: Date
}

export function parseMessage(rawMessage: string): Message {
  return JSON.parse(rawMessage)
}
