import ws from 'k6/ws'
import { Counter, Trend } from 'k6/metrics'
import { parseMessage } from "./utils.js"
import { Options } from 'k6/options'

const settings = {
  url: "ws://server",
}

export const options: Options = {
  stages: [
    { duration: "30s", target: 100 },
    { duration: "1m", target: 100 },
    { duration: "10s", target: 0 },
  ],
  thresholds: {
    message_delay: ["p(99.99) < 1", "max < 10"]
  },
  tags: {
    name: "stream"
  }
}

const messageDelay = new Trend("message_delay", true)
const messageCounter = new Counter("message_counter")

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
      messageCounter.add(1, { stream: data.stream })
    })
  })
}
