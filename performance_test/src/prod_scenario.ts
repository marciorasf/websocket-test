import { Trend } from 'k6/metrics'
import ws from 'k6/ws'

export const options = {
  vus: 1,
  duration: '30s',
}

const settings = {
  url: "ws://server",
  closeSocketAfterNMilliseconds: 5 * 1000,
}

const messageDelay = new Trend("message_delay", true)

export default function () {
  ws.connect(settings.url, function (socket) {
    socket.on("open", () => {
      socket.send(JSON.stringify({
        action: "subscribe",
        stream: "default"
      }))

      socket.send(JSON.stringify({
        action: "subscribe",
        stream: "even"
      }))

      socket.send(JSON.stringify({
        action: "subscribe",
        stream: "odd"
      }))
    })

    socket.on("message", (rawData) => {
      const data = parseMessage(rawData)
      const delay = Date.now() - (new Date(data.timestamp)).getTime()
      messageDelay.add(delay / 1000)
    })

    socket.on("close", () => {
    })

    socket.setTimeout(() => {
      socket.close()
    }, settings.closeSocketAfterNMilliseconds)
  })
}

type Message = {
  stream: string
  content: number
  timestamp: Date
}

function parseMessage(rawMessage: string): Message {
  return JSON.parse(rawMessage)
}
