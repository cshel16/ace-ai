import { useState } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")

  const sendMessage = async () => {
    // add user message to state
    // POST to your /chat endpoint
    // add assistant response to state
    setMessages(prev => [...prev, { role: "user", text: input }])
    setInput("")
    fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json'
      },
      body: JSON.stringify({message: input})
    })
      .then((response) => response.json())
      .then((data) => {
        setMessages(prev => [...prev, { role: "assistant", text: data }])
      })
      .catch((error) => {
        console.error('Error:', error);
        // Handle errors
      });
  }

  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i}>{msg.role}: {msg.text}</div>
      ))}
      <form onSubmit={(e) => { e.preventDefault(); sendMessage(); }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} />
        <button type="submit">Send</button>
      </form>
    </div>
  )
}

export default App
