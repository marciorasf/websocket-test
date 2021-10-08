import ws from 'k6/ws'

export const options = {
  vus: 1,
  duration: '30s',
}

const settings = {
  url: "ws://server",
  close_socket_after_n_milliseconds: 5 * 1000,
}

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

    socket.on("message", () => {
    })

    socket.on("close", () => {
    })

    socket.setTimeout(() => {
      socket.close()
    }, settings.close_socket_after_n_milliseconds)
  })
}
