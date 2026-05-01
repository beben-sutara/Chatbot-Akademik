import React, { useState, useEffect, useRef } from 'react'
import { useAuth } from '../context/AuthContext'
import { GraduationCap, Send, Plus, Trash2, LogOut, BookOpen, Calendar, Star, HelpCircle, Menu, X } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import api from '../services/api'

const QUICK_ACTIONS = [
  { icon: BookOpen, label: 'Jadwal Kuliah', message: 'Tampilkan jadwal kuliah saya' },
  { icon: Star, label: 'Nilai Saya', message: 'Tampilkan nilai saya' },
  { icon: Calendar, label: 'Kalender Akademik', message: 'Tampilkan kalender akademik' },
  { icon: HelpCircle, label: 'Bantuan', message: 'Apa yang bisa kamu bantu?' },
]

function MessageBubble({ message }) {
  const isUser = message.role === 'user'
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center mr-2 shrink-0 mt-1">
          <GraduationCap className="h-4 w-4 text-white" />
        </div>
      )}
      <div
        className={`max-w-[75%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
          isUser
            ? 'bg-primary-600 text-white rounded-tr-sm'
            : 'bg-white border border-gray-200 text-gray-800 rounded-tl-sm shadow-sm'
        }`}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap">{message.content}</p>
        ) : (
          <ReactMarkdown
            components={{
              p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
              ul: ({ children }) => <ul className="list-disc list-inside mb-2">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal list-inside mb-2">{children}</ol>,
              strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
            }}
          >
            {message.content}
          </ReactMarkdown>
        )}
        <p className={`text-xs mt-1 ${isUser ? 'text-primary-200' : 'text-gray-400'}`}>
          {new Date(message.created_at).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>
    </div>
  )
}

function TypingIndicator() {
  return (
    <div className="flex items-start mb-4">
      <div className="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center mr-2 shrink-0">
        <GraduationCap className="h-4 w-4 text-white" />
      </div>
      <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm">
        <div className="flex gap-1">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
              style={{ animationDelay: `${i * 0.15}s` }}
            />
          ))}
        </div>
      </div>
    </div>
  )
}

export default function ChatPage() {
  const { user, logout } = useAuth()
  const [sessions, setSessions] = useState([])
  const [currentSession, setCurrentSession] = useState(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    fetchSessions()
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const fetchSessions = async () => {
    try {
      const res = await api.get('/api/v1/chat/sessions')
      setSessions(res.data)
    } catch (err) {
      console.error('Failed to fetch sessions', err)
    }
  }

  const loadSession = async (session) => {
    setCurrentSession(session)
    setSidebarOpen(false)
    try {
      const res = await api.get(`/api/v1/chat/sessions/${session.id}`)
      setMessages(res.data.messages || [])
    } catch (err) {
      console.error('Failed to load session', err)
    }
  }

  const newChat = () => {
    setCurrentSession(null)
    setMessages([])
    setSidebarOpen(false)
    inputRef.current?.focus()
  }

  const deleteSession = async (e, sessionId) => {
    e.stopPropagation()
    try {
      await api.delete(`/api/v1/chat/sessions/${sessionId}`)
      setSessions((prev) => prev.filter((s) => s.id !== sessionId))
      if (currentSession?.id === sessionId) newChat()
    } catch (err) {
      console.error('Failed to delete session', err)
    }
  }

  const sendMessage = async (text) => {
    const messageText = text || input.trim()
    if (!messageText || loading) return

    setInput('')
    const userMsg = { role: 'user', content: messageText, created_at: new Date().toISOString() }
    setMessages((prev) => [...prev, userMsg])
    setLoading(true)

    try {
      const res = await api.post('/api/v1/chat/', {
        message: messageText,
        session_id: currentSession?.id || null,
      })
      const { session_id, message: reply } = res.data
      const aiMsg = { role: 'assistant', content: reply, created_at: new Date().toISOString() }
      setMessages((prev) => [...prev, aiMsg])

      if (!currentSession) {
        await fetchSessions()
        setCurrentSession({ id: session_id })
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Maaf, terjadi kesalahan. Silakan coba lagi.',
          created_at: new Date().toISOString(),
        },
      ])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 bg-black/40 z-20 lg:hidden" onClick={() => setSidebarOpen(false)} />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:static inset-y-0 left-0 z-30 w-72 bg-primary-900 text-white flex flex-col transform transition-transform duration-300 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="p-4 border-b border-primary-700 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <GraduationCap className="h-6 w-6" />
            <span className="font-semibold">Chatbot Akademik</span>
          </div>
          <button onClick={() => setSidebarOpen(false)} className="lg:hidden p-1 hover:bg-primary-700 rounded">
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="p-3">
          <button
            onClick={newChat}
            className="w-full flex items-center gap-2 px-3 py-2.5 rounded-lg bg-primary-700 hover:bg-primary-600 transition-colors text-sm font-medium"
          >
            <Plus className="h-4 w-4" />
            Chat Baru
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-3 space-y-1">
          {sessions.map((session) => (
            <div
              key={session.id}
              onClick={() => loadSession(session)}
              className={`group flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer transition-colors text-sm ${
                currentSession?.id === session.id ? 'bg-primary-600' : 'hover:bg-primary-800'
              }`}
            >
              <span className="truncate flex-1">{session.title}</span>
              <button
                onClick={(e) => deleteSession(e, session.id)}
                className="shrink-0 p-1 rounded opacity-0 group-hover:opacity-100 hover:bg-primary-500 transition-opacity ml-1"
              >
                <Trash2 className="h-3.5 w-3.5" />
              </button>
            </div>
          ))}
        </div>

        <div className="p-4 border-t border-primary-700">
          <div className="flex items-center justify-between">
            <div className="min-w-0">
              <p className="text-sm font-medium truncate">{user?.full_name}</p>
              <p className="text-xs text-primary-300 truncate">{user?.nim_nip} • {user?.role}</p>
            </div>
            <button
              onClick={logout}
              className="shrink-0 p-2 rounded-lg hover:bg-primary-700 transition-colors ml-2"
              title="Logout"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main chat area */}
      <main className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center gap-3 shrink-0">
          <button
            onClick={() => setSidebarOpen(true)}
            className="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
          >
            <Menu className="h-5 w-5" />
          </button>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center">
              <GraduationCap className="h-4 w-4 text-white" />
            </div>
            <div>
              <p className="font-medium text-sm">Akad</p>
              <p className="text-xs text-green-500">● Online</p>
            </div>
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center px-4">
              <div className="bg-primary-100 p-5 rounded-full mb-4">
                <GraduationCap className="h-12 w-12 text-primary-600" />
              </div>
              <h2 className="text-xl font-semibold text-gray-800 mb-2">Halo, {user?.full_name}! 👋</h2>
              <p className="text-gray-500 mb-6 max-w-sm">Saya Akad, asisten akademik digital Anda. Apa yang bisa saya bantu hari ini?</p>
              <div className="grid grid-cols-2 gap-3 w-full max-w-sm">
                {QUICK_ACTIONS.map(({ icon: Icon, label, message }) => (
                  <button
                    key={label}
                    onClick={() => sendMessage(message)}
                    className="flex flex-col items-center gap-2 p-4 bg-white border border-gray-200 rounded-xl hover:border-primary-300 hover:bg-primary-50 transition-colors text-sm text-gray-700"
                  >
                    <Icon className="h-5 w-5 text-primary-600" />
                    {label}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <>
              {messages.map((msg, i) => (
                <MessageBubble key={msg.id ?? i} message={msg} />
              ))}
              {loading && <TypingIndicator />}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input */}
        <div className="bg-white border-t border-gray-200 p-4 shrink-0">
          <div className="flex items-end gap-3 max-w-4xl mx-auto">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ketik pesan Anda..."
              rows={1}
              className="flex-1 input-field resize-none max-h-32 overflow-y-auto"
              style={{ minHeight: '42px' }}
              disabled={loading}
            />
            <button
              onClick={() => sendMessage()}
              disabled={!input.trim() || loading}
              className="shrink-0 w-10 h-10 flex items-center justify-center bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 text-white rounded-xl transition-colors"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
          <p className="text-center text-xs text-gray-400 mt-2">
            Tekan Enter untuk kirim • Shift+Enter untuk baris baru
          </p>
        </div>
      </main>
    </div>
  )
}
