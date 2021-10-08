import ws from 'k6/ws'

export let options = {
  vus: 1,
  duration: '30s',
}

export default function () {
  const url = "ws://server"

  ws.connect(url, function (socket) {
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

    socket.on("message", (data) => {
    })

    socket.on("close", () => {
    })
  })
}
